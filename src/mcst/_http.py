"""KCISA, data.go.kr, ODCloud 계열 API용 httpx transport입니다."""

from __future__ import annotations

import asyncio
import inspect
import logging
import math
import random
import re
import time
from collections import defaultdict
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Any, Protocol, cast
from urllib.parse import parse_qsl, urlparse, urlsplit
from xml.etree import ElementTree

import httpx

from ._convert import to_int_or_none, without_none
from ._httpx import send_after_token
from ._ratelimit import AsyncTokenBucket
from ._redact import credential_values, redact_exception, redact_secret
from .debug import redact_sensitive
from .exceptions import (
    McstAuthError,
    McstError,
    McstNetworkError,
    McstParseError,
    McstRateLimitError,
    McstRequestError,
    McstServerError,
)


class ResponseLike(Protocol):
    status_code: int
    text: str
    content: bytes
    headers: Mapping[str, str]

    def json(self) -> Any: ...


class SessionLike(Protocol):
    async def get(
        self,
        url: str,
        *,
        params: Mapping[str, Any] | None = None,
        timeout: float,
    ) -> ResponseLike: ...


TRANSIENT_STATUSES = {429, 500, 502, 503, 504}
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (compatible; mcst/0.1; +https://github.com/digitie/python-mcst-api)"
)
SENSITIVE_QUERY_RE = re.compile(
    r"(?i)(serviceKey|service_key|api_key|apikey|access_token|refresh_token)=([^&\s)]+)"
)


@dataclass(frozen=True, slots=True)
class NormalizedPayload:
    items: tuple[dict[str, Any], ...]
    page_no: int
    num_of_rows: int
    total_count: int | None
    raw: Any


def build_session() -> SessionLike:
    """기본 헤더를 적용한 httpx 비동기 클라이언트를 만듭니다."""

    return cast(
        SessionLike,
        httpx.AsyncClient(
            headers={"User-Agent": DEFAULT_USER_AGENT},
            follow_redirects=True,
        ),
    )


class HttpClient:
    """공통 오류 처리, 재시도, rate limit을 포함한 비동기 GET 호출 래퍼입니다."""

    def __init__(
        self,
        *,
        service_key: str | None = None,
        session: SessionLike | None = None,
        timeout: float = 10.0,
        retries: int = 3,
        max_rps: float = 5.0,
        rate_limiter: AsyncTokenBucket | None = None,
    ) -> None:
        self.service_key = service_key
        self.rate_limiter = rate_limiter if rate_limiter is not None else AsyncTokenBucket(max_rps)
        self._session = session
        self.closed = False
        self._validate_session(session)
        self.timeout = timeout
        self.retries = max(0, retries)
        self._owns_session = session is None

    @staticmethod
    def _validate_session(session: SessionLike | None) -> None:
        if session is not None and not inspect.iscoroutinefunction(getattr(session, "get", None)):
            raise TypeError("session.get must be async")
        if isinstance(session, httpx.AsyncClient):
            if session.auth is not None and type(session.auth) not in {httpx.Auth, httpx.BasicAuth}:
                raise TypeError("Digest/custom Auth may send unmetered requests")

    def _ready(self) -> SessionLike:
        if self.closed:
            raise RuntimeError("client is closed")
        if self._session is None:
            self._session = build_session()
        self._validate_session(self._session)
        return self._session

    def _before_send(self) -> None:
        self._ready()

    @property
    def session(self) -> SessionLike:
        return self._ready()

    async def aclose(self) -> None:
        if not self.closed:
            self.closed = True
            close = getattr(self._session, "aclose", None)
            if self._owns_session and callable(close):
                await close()

    async def get_response(
        self,
        url: str,
        params: Mapping[str, Any] | None = None,
        *,
        service_key: str | None = None,
        timeout: float | None = None,
    ) -> ResponseLike:
        try:
            active_service_key = service_key or self.service_key
            active_timeout = timeout if timeout is not None else self.timeout
            query = without_none(params or {})
            self._ready()
            for attempt in range(self.retries + 1):
                await self.rate_limiter.acquire()
                session = self._ready()
                try:
                    if isinstance(session, httpx.AsyncClient):
                        request = session.build_request(
                            "GET", url, params=query or None, timeout=active_timeout
                        )
                        response = await send_after_token(
                            session, request, self.rate_limiter, before_send=self._before_send
                        )
                    elif query:
                        response = await session.get(url, params=query, timeout=active_timeout)
                    else:
                        response = await session.get(url, timeout=active_timeout)
                except httpx.TooManyRedirects as exc:
                    raise _network_error(url, exc, active_service_key) from None
                except httpx.HTTPError as exc:
                    if attempt >= self.retries:
                        raise _network_error(url, exc, active_service_key) from None
                    await _sleep_before_retry(attempt)
                    continue
                if response.status_code in TRANSIENT_STATUSES and attempt < self.retries:
                    retry_after = _retry_after_seconds(response)
                    await close_response(response)
                    await _sleep_before_retry(attempt, retry_after)
                    continue
                _raise_for_status(response, endpoint=url, service_key=active_service_key)
                return response
            raise AssertionError("unreachable")

        except McstError as exc:
            redact_exception(
                exc,
                service_key or "",
                self.service_key or "",
                *credential_values(params),
                *credential_values(dict(parse_qsl(urlsplit(url).query))),
            )
            raise exc from None

    async def get_debug_response(
        self,
        url: str,
        params: Mapping[str, Any] | None = None,
        *,
        service_key: str | None = None,
        timeout: float | None = None,
    ) -> tuple[ResponseLike, dict[str, Any], dict[str, Any]]:
        """디버그 UI가 저장할 수 있는 요청/응답 외피와 함께 GET을 수행합니다."""

        query = without_none(params or {})
        active_service_key = service_key or self.service_key
        started_at = time.perf_counter()
        response = await self.get_response(
            url, query, service_key=active_service_key, timeout=timeout
        )
        elapsed_ms = round((time.perf_counter() - started_at) * 1000, 1)
        return (
            response,
            _request_data(url, query),
            _response_data(response, active_service_key, elapsed_ms=elapsed_ms),
        )

    async def get_bytes(
        self,
        url: str,
        params: Mapping[str, Any] | None = None,
        *,
        timeout: float | None = None,
    ) -> bytes:
        return (await self.get_response(url, params, timeout=timeout)).content

    async def get_json(
        self,
        url: str,
        params: Mapping[str, Any] | None = None,
        *,
        service_key: str | None = None,
        timeout: float | None = None,
    ) -> Any:
        active_service_key = service_key or self.service_key
        response = await self.get_response(
            url, params, service_key=active_service_key, timeout=timeout
        )
        try:
            return response.json()
        except ValueError:
            text = _redact(response.text, active_service_key)[:300]
            raise McstParseError(
                f"response was not valid JSON: {text}",
                endpoint=url,
                failure_kind="parse",
            ) from None


class KcisaHttp(HttpClient):
    """culture.go.kr/KCISA OpenAPI 엔드포인트용 비동기 HTTP 클라이언트입니다."""

    async def get_page(
        self,
        endpoint_url: str,
        *,
        page_no: int,
        num_of_rows: int,
        keyword: str | None = None,
        params: Mapping[str, Any] | None = None,
        service_key: str | None = None,
        timeout: float | None = None,
    ) -> NormalizedPayload:
        active_service_key = _require_key(service_key or self.service_key, endpoint_url)
        query = _kcisa_query(active_service_key, page_no, num_of_rows, keyword, params)
        response = await self.get_response(
            endpoint_url, query, service_key=active_service_key, timeout=timeout
        )
        return _normalized_response(
            response,
            endpoint_url,
            active_service_key,
            page_no,
            num_of_rows,
        )

    async def get_debug_page(
        self,
        endpoint_url: str,
        *,
        page_no: int,
        num_of_rows: int,
        keyword: str | None = None,
        params: Mapping[str, Any] | None = None,
        service_key: str | None = None,
        timeout: float | None = None,
    ) -> tuple[NormalizedPayload, dict[str, Any], dict[str, Any]]:
        """KCISA 응답과 fixture 저장용 요청/응답 정보를 함께 반환합니다."""

        active_service_key = _require_key(service_key or self.service_key, endpoint_url)
        query = _kcisa_query(active_service_key, page_no, num_of_rows, keyword, params)
        response, request_data, response_data = await self.get_debug_response(
            endpoint_url,
            query,
            service_key=active_service_key,
            timeout=timeout,
        )
        payload = _decode_payload(response, endpoint_url, active_service_key)
        response_data["body"] = redact_sensitive(payload)
        normalized = _normalize_payload(payload, page_no=page_no, num_of_rows=num_of_rows)
        _raise_for_payload_error(normalized.raw, endpoint_url, service_key=active_service_key)
        return normalized, request_data, response_data


class OdcloudHttp(HttpClient):
    """data.go.kr 자동변환 파일 API용 비동기 HTTP 클라이언트입니다."""

    base_url = "https://api.odcloud.kr/api"

    async def get_page(
        self,
        public_data_pk: str,
        public_data_detail_pk: str,
        *,
        page_no: int,
        per_page: int,
        params: Mapping[str, Any] | None = None,
        service_key: str | None = None,
        timeout: float | None = None,
    ) -> NormalizedPayload:
        active_service_key = _require_key(service_key or self.service_key, public_data_pk)
        url, query = _odcloud_url_query(
            self.base_url,
            public_data_pk,
            public_data_detail_pk,
            page_no,
            per_page,
            active_service_key,
            params,
        )
        payload = await self.get_json(url, query, service_key=active_service_key, timeout=timeout)
        return _normalized_odcloud_payload(payload, url, page_no, per_page, active_service_key)

    async def get_debug_page(
        self,
        public_data_pk: str,
        public_data_detail_pk: str,
        *,
        page_no: int,
        per_page: int,
        params: Mapping[str, Any] | None = None,
        service_key: str | None = None,
        timeout: float | None = None,
    ) -> tuple[NormalizedPayload, dict[str, Any], dict[str, Any]]:
        """ODCloud 응답과 fixture 저장용 요청/응답 정보를 함께 반환합니다."""

        active_service_key = _require_key(service_key or self.service_key, public_data_pk)
        url, query = _odcloud_url_query(
            self.base_url,
            public_data_pk,
            public_data_detail_pk,
            page_no,
            per_page,
            active_service_key,
            params,
        )
        response, request_data, response_data = await self.get_debug_response(
            url,
            query,
            service_key=active_service_key,
            timeout=timeout,
        )
        payload = _json_payload(response, url, active_service_key)
        response_data["body"] = redact_sensitive(payload)
        normalized = _normalized_odcloud_payload(
            payload,
            url,
            page_no,
            per_page,
            active_service_key,
        )
        return normalized, request_data, response_data


def _request_data(url: str, query: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "method": "GET",
        "url": url,
        "query": redact_sensitive(dict(query)),
    }


def _response_data(
    response: ResponseLike,
    service_key: str | None = None,
    *,
    elapsed_ms: float | None = None,
) -> dict[str, Any]:
    return {
        "status_code": response.status_code,
        "headers": {key: _redact(value, service_key) for key, value in response.headers.items()},
        "elapsed_ms": elapsed_ms,
        "body": None,
    }


def _kcisa_query(
    service_key: str,
    page_no: int,
    num_of_rows: int,
    keyword: str | None,
    params: Mapping[str, Any] | None,
) -> dict[str, Any]:
    query: dict[str, Any] = {
        "serviceKey": service_key,
        "numOfRows": num_of_rows,
        "pageNo": page_no,
        "keyword": keyword,
    }
    if params:
        query.update(params)
    return query


def _odcloud_url_query(
    base_url: str,
    public_data_pk: str,
    public_data_detail_pk: str,
    page_no: int,
    per_page: int,
    service_key: str,
    params: Mapping[str, Any] | None,
) -> tuple[str, dict[str, Any]]:
    url = f"{base_url}/{public_data_pk}/v1/{public_data_detail_pk}"
    query: dict[str, Any] = {
        "page": page_no,
        "perPage": per_page,
        "serviceKey": service_key,
    }
    if params:
        query.update(params)
    return url, query


def _normalized_response(
    response: ResponseLike,
    endpoint_url: str,
    service_key: str,
    page_no: int,
    num_of_rows: int,
) -> NormalizedPayload:
    payload = _decode_payload(response, endpoint_url, service_key)
    normalized = _normalize_payload(payload, page_no=page_no, num_of_rows=num_of_rows)
    _raise_for_payload_error(normalized.raw, endpoint_url, service_key=service_key)
    return normalized


def _normalized_odcloud_payload(
    payload: Any,
    url: str,
    page_no: int,
    per_page: int,
    service_key: str,
) -> NormalizedPayload:
    _raise_for_payload_error(payload, url, service_key=service_key)
    if not isinstance(payload, Mapping):
        raise McstParseError("ODCloud response root was not an object", endpoint=url)
    rows = payload.get("data") or payload.get("items") or []
    items = _rows_to_tuple(rows, endpoint=url)
    return NormalizedPayload(
        items=items,
        page_no=page_no,
        num_of_rows=per_page,
        total_count=to_int_or_none(payload.get("totalCount")),
        raw=payload,
    )


def _require_key(service_key: str | None, endpoint: str) -> str:
    if service_key:
        return service_key
    raise McstAuthError(
        "service_key is required. Pass service_key=... or set DATA_GO_KR_SERVICE_KEY.",
        endpoint=endpoint,
        failure_kind="auth",
    )


def _retry_after_seconds(response: ResponseLike) -> float | None:
    value = response.headers.get("Retry-After")
    if not value:
        return None
    value = value.strip()
    try:
        seconds = float(value)
        return max(seconds, 0.0) if math.isfinite(seconds) else None
    except ValueError:
        pass
    try:
        parsed = parsedate_to_datetime(value)
    except (TypeError, ValueError, IndexError):
        return None
    if parsed is None:
        return None
    now = datetime.now(parsed.tzinfo) if parsed.tzinfo else datetime.now()
    return max((parsed - now).total_seconds(), 0.0)


async def _sleep_before_retry(attempt: int, retry_after: float | None = None) -> None:
    backoff = 0.3 * (2**attempt)
    jitter = random.uniform(0, 0.1 * backoff)
    delay = min(backoff + jitter, 4.0)
    if retry_after is not None:
        delay = max(delay, min(retry_after, 60.0))
    await asyncio.sleep(delay)


def _raise_for_status(
    response: ResponseLike,
    *,
    endpoint: str,
    service_key: str | None,
) -> None:
    status = response.status_code
    text = _redact(response.text, service_key)[:300]
    if status in {401, 403}:
        raise McstAuthError(
            f"HTTP {status}: {text}",
            status_code=status,
            endpoint=endpoint,
            failure_kind="auth",
        )
    if status == 429:
        raise McstRateLimitError(
            f"HTTP {status}: {text}",
            status_code=status,
            endpoint=endpoint,
            failure_kind="rate_limit",
        )
    if 400 <= status < 500:
        _raise_for_status_payload_error(response, endpoint=endpoint, service_key=service_key)
        raise McstRequestError(
            f"HTTP {status}: {text}",
            status_code=status,
            endpoint=endpoint,
            failure_kind="request",
        )
    if 500 <= status < 600:
        raise McstServerError(
            f"HTTP {status}: {text}",
            status_code=status,
            endpoint=endpoint,
            failure_kind="server",
        )


def _raise_for_status_payload_error(
    response: ResponseLike,
    *,
    endpoint: str,
    service_key: str | None,
) -> None:
    try:
        payload = _decode_payload(response, endpoint, service_key)
    except McstParseError:
        return
    if not isinstance(payload, Mapping):
        return
    code, message = _payload_code_and_message(payload)
    text = _redact(f"HTTP {response.status_code}: {code}: {message}", service_key)
    upper = f"{code}: {message}".upper()
    if code in {"-4", "-401", "20", "30", "31"} or (
        code != "22" and ("SERVICE" in upper or "인증" in message)
    ):
        raise McstAuthError(
            text,
            status_code=response.status_code,
            result_code=code,
            endpoint=endpoint,
            failure_kind="auth",
        )
    if code in {"22"} or "LIMIT" in upper or "QUOTA" in upper:
        raise McstRateLimitError(
            text,
            status_code=response.status_code,
            result_code=code,
            endpoint=endpoint,
            failure_kind="rate_limit",
        )


def _decode_payload(
    response: ResponseLike, endpoint: str = "", service_key: str | None = None
) -> Any:
    content_type = response.headers.get("Content-Type", "").casefold()
    text = response.text.strip()
    if "json" in content_type or text.startswith("{") or text.startswith("["):
        return _json_payload(response, endpoint, service_key)
    if text.startswith("<"):
        try:
            root = ElementTree.fromstring(text)
        except ElementTree.ParseError:
            raise McstParseError("response was not valid XML", failure_kind="parse") from None
        return _element_to_data(root)
    raise McstParseError(
        f"unsupported response body from {urlparse(endpoint).netloc}",
        failure_kind="parse",
    )


def _json_payload(response: ResponseLike, endpoint: str, service_key: str | None) -> Any:
    try:
        return response.json()
    except ValueError:
        text = _redact(response.text, service_key)[:300]
        raise McstParseError(
            f"response was not valid JSON: {text}",
            endpoint=endpoint,
            failure_kind="parse",
        ) from None


_MAX_XML_DEPTH = 50


def _element_to_data(element: ElementTree.Element, *, depth: int = 0) -> Any:
    if depth > _MAX_XML_DEPTH:
        raise McstParseError("XML response nested too deeply", failure_kind="parse")
    children = list(element)
    text = (element.text or "").strip()
    if not children:
        return text

    grouped: dict[str, list[Any]] = defaultdict(list)
    for child in children:
        tag = child.tag.rsplit("}", 1)[-1]
        grouped[tag].append(_element_to_data(child, depth=depth + 1))
    data: dict[str, Any] = {}
    for tag, values in grouped.items():
        data[tag] = values[0] if len(values) == 1 else values
    if text:
        data["_text"] = text
    return data


def _first_int(*candidates: Any) -> int | None:
    for candidate in candidates:
        value = to_int_or_none(candidate)
        if value is not None:
            return value
    return None


def _normalize_payload(payload: Any, *, page_no: int, num_of_rows: int) -> NormalizedPayload:
    if not isinstance(payload, Mapping):
        raise McstParseError("response root was not an object", failure_kind="parse")
    root = payload.get("response", payload)
    if not isinstance(root, Mapping):
        raise McstParseError("response was not an object", failure_kind="parse")
    body = root.get("body", root)
    if not isinstance(body, Mapping):
        raise McstParseError("response body was not an object", failure_kind="parse")

    items_obj = body.get("items", body.get("item", body.get("data", [])))
    if isinstance(items_obj, Mapping) and "item" in items_obj:
        items_obj = items_obj["item"]
    items = _rows_to_tuple(items_obj, endpoint="")
    return NormalizedPayload(
        items=items,
        page_no=page_no,
        num_of_rows=num_of_rows,
        total_count=_first_int(body.get("totalCount"), body.get("totalCnt")),
        raw=payload,
    )


def _rows_to_tuple(rows: Any, *, endpoint: str) -> tuple[dict[str, Any], ...]:
    if rows in (None, "", []):
        return ()
    if isinstance(rows, Mapping):
        return (dict(rows),)
    if isinstance(rows, list) and all(isinstance(row, Mapping) for row in rows):
        return tuple(dict(row) for row in rows)
    raise McstParseError(
        "response items were not an object or list of objects",
        endpoint=endpoint,
        failure_kind="parse",
    )


def _payload_code_and_message(payload: Mapping[str, Any]) -> tuple[str, str]:
    code = str(
        payload.get("code")
        or payload.get("resultCode")
        or _nested(payload, "response", "header", "resultCode")
        or _nested(payload, "header", "resultCode")
        or ""
    ).strip()
    message = str(
        payload.get("msg")
        or payload.get("message")
        or payload.get("resultMsg")
        or _nested(payload, "response", "header", "resultMsg")
        or _nested(payload, "header", "resultMsg")
        or ""
    ).strip()
    return code, message


def _raise_for_payload_error(payload: Any, endpoint: str, *, service_key: str | None) -> None:
    if not isinstance(payload, Mapping):
        return
    code, message = _payload_code_and_message(payload)
    if not code or code in {"0", "00", "0000", "NORMAL_CODE", "INFO-000"}:
        return
    text = _redact(f"{code}: {message}", service_key)
    upper = f"{code}: {message}".upper()
    if code in {"-4", "-401", "20", "30", "31"} or (
        code != "22" and ("SERVICE" in upper or "인증" in message)
    ):
        raise McstAuthError(text, result_code=code, endpoint=endpoint, failure_kind="auth")
    if code in {"03", "INFO-200"} or "NO DATA" in upper:
        return
    if code in {"22"} or "LIMIT" in upper or "QUOTA" in upper:
        raise McstRateLimitError(
            text,
            result_code=code,
            endpoint=endpoint,
            failure_kind="rate_limit",
        )
    raise McstRequestError(text, result_code=code, endpoint=endpoint, failure_kind="request")


def _nested(data: Mapping[str, Any], *keys: str) -> Any:
    current: Any = data
    for key in keys:
        if not isinstance(current, Mapping):
            return None
        current = current.get(key)
    return current


def _redact(text: str, secret: str | None) -> str:
    redacted = SENSITIVE_QUERY_RE.sub(lambda match: f"{match.group(1)}=[redacted]", text)
    if not secret:
        return redacted
    return str(redact_secret(redacted, secret, secret.strip().strip('"').strip("'")))


def _network_error(url: str, exc: httpx.HTTPError, service_key: str | None) -> McstNetworkError:
    message = _redact(str(exc), service_key)
    lowered = message.casefold()
    dns_tokens = ("failed to resolve", "nameresolutionerror", "getaddrinfo")
    if any(token in lowered for token in dns_tokens):
        prefix = "DNS lookup failed for upstream host"
    elif "timed out" in lowered or "timeout" in lowered:
        prefix = "network request timed out"
    else:
        prefix = "network request failed"
    return McstNetworkError(
        f"{prefix}: {message}",
        endpoint=url,
        failure_kind="network",
    )


async def close_response(response: ResponseLike) -> None:
    close = getattr(response, "aclose", None)
    if callable(close):
        await close()


class _KeyLogFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = SENSITIVE_QUERY_RE.sub(
            lambda match: f"{match.group(1)}=[redacted]", record.getMessage()
        )
        record.args = ()
        return True


logging.getLogger("httpx").addFilter(_KeyLogFilter())
