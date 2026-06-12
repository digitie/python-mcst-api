"""KCISA, data.go.kr, ODCloud 계열 API용 httpx transport입니다."""

from __future__ import annotations

import asyncio
import random
import re
import time
from collections import defaultdict
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any, Protocol, cast
from urllib.parse import urlparse
from xml.etree import ElementTree

import httpx

from ._convert import to_int_or_none, without_none
from .debug import redact_sensitive
from .exceptions import (
    McstAuthError,
    McstNetworkError,
    McstNoDataError,
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
    def get(
        self,
        url: str,
        *,
        params: Mapping[str, Any] | None = None,
        timeout: float,
    ) -> ResponseLike: ...


class AsyncSessionLike(Protocol):
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


@dataclass(slots=True)
class TokenBucket:
    """Async token bucket rate limiter."""

    max_rps: float = 5.0
    capacity: float | None = None
    _tokens: float = field(init=False)
    _updated_at: float = field(init=False)
    _lock: asyncio.Lock = field(default_factory=asyncio.Lock, init=False)

    def __post_init__(self) -> None:
        if self.max_rps <= 0:
            raise ValueError("max_rps must be greater than 0")
        self.capacity = self.capacity or self.max_rps
        self._tokens = self.capacity
        self._updated_at = time.monotonic()

    async def acquire(self) -> None:
        while True:
            async with self._lock:
                self._refill()
                if self._tokens >= 1:
                    self._tokens -= 1
                    return
                wait_for = (1 - self._tokens) / self.max_rps
            await asyncio.sleep(wait_for)

    def _refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self._updated_at
        self._updated_at = now
        assert self.capacity is not None
        self._tokens = min(self.capacity, self._tokens + elapsed * self.max_rps)


def build_session() -> SessionLike:
    """기본 헤더를 적용한 httpx 동기 클라이언트를 만듭니다."""

    return cast(
        SessionLike,
        httpx.Client(
            headers={"User-Agent": DEFAULT_USER_AGENT},
            follow_redirects=True,
        ),
    )


def build_async_session() -> AsyncSessionLike:
    """기본 헤더를 적용한 httpx 비동기 클라이언트를 만듭니다."""

    return cast(
        AsyncSessionLike,
        httpx.AsyncClient(
            headers={"User-Agent": DEFAULT_USER_AGENT},
            follow_redirects=True,
        ),
    )


class HttpClient:
    """공통 오류 처리와 재시도를 포함한 동기 GET 호출 래퍼입니다."""

    def __init__(
        self,
        *,
        service_key: str | None = None,
        session: SessionLike | None = None,
        timeout: float = 10.0,
        retries: int = 3,
    ) -> None:
        self.service_key = service_key
        self.session = session or build_session()
        self.timeout = timeout
        self.retries = retries
        self._owns_session = session is None

    def close(self) -> None:
        close = getattr(self.session, "close", None)
        if self._owns_session and callable(close):
            close()

    def get_response(
        self,
        url: str,
        params: Mapping[str, Any] | None = None,
        *,
        service_key: str | None = None,
        timeout: float | None = None,
    ) -> ResponseLike:
        active_service_key = service_key or self.service_key
        active_timeout = timeout if timeout is not None else self.timeout
        query = without_none(params or {})
        for attempt in range(self.retries + 1):
            try:
                # httpx는 params를 명시하면(빈 dict 포함) URL 자체의 query를
                # 통째로 대체한다 — 파일 다운로드 페이지처럼 query가 URL에
                # 박힌 호출(#9)에서 detail이 빈 셸로 렌더되는 원인. 비어 있으면
                # params를 아예 전달하지 않는다.
                if query:
                    response = self.session.get(url, params=query, timeout=active_timeout)
                else:
                    response = self.session.get(url, timeout=active_timeout)
            except httpx.HTTPError as exc:
                if attempt >= self.retries:
                    raise _network_error(url, exc, active_service_key) from exc
                _sleep_before_retry(attempt)
                continue
            if response.status_code in TRANSIENT_STATUSES and attempt < self.retries:
                _sleep_before_retry(attempt)
                continue
            _raise_for_status(response, endpoint=url, service_key=active_service_key)
            return response
        raise AssertionError("unreachable")

    def get_debug_response(
        self,
        url: str,
        params: Mapping[str, Any] | None = None,
        *,
        service_key: str | None = None,
        timeout: float | None = None,
    ) -> tuple[ResponseLike, dict[str, Any], dict[str, Any]]:
        """디버그 UI가 저장할 수 있는 요청/응답 외피와 함께 GET을 수행합니다."""

        query = without_none(params or {})
        response = self.get_response(url, query, service_key=service_key, timeout=timeout)
        return response, _request_data(url, query), _response_data(response)

    def get_bytes(
        self,
        url: str,
        params: Mapping[str, Any] | None = None,
        *,
        timeout: float | None = None,
    ) -> bytes:
        return self.get_response(url, params, timeout=timeout).content

    def get_json(
        self,
        url: str,
        params: Mapping[str, Any] | None = None,
        *,
        service_key: str | None = None,
        timeout: float | None = None,
    ) -> Any:
        active_service_key = service_key or self.service_key
        response = self.get_response(url, params, service_key=active_service_key, timeout=timeout)
        try:
            return response.json()
        except ValueError as exc:
            text = _redact(response.text[:300], active_service_key)
            raise McstParseError(
                f"response was not valid JSON: {text}",
                endpoint=url,
                failure_kind="parse",
            ) from exc


class AsyncHttpClient:
    """공통 오류 처리, 재시도, rate limit을 포함한 비동기 GET 호출 래퍼입니다."""

    def __init__(
        self,
        *,
        service_key: str | None = None,
        session: AsyncSessionLike | None = None,
        timeout: float = 10.0,
        retries: int = 3,
        max_rps: float = 5.0,
    ) -> None:
        self.service_key = service_key
        self.session = session or build_async_session()
        self.timeout = timeout
        self.retries = retries
        self._bucket = TokenBucket(max_rps=max_rps)
        self._owns_session = session is None

    async def aclose(self) -> None:
        close = getattr(self.session, "aclose", None)
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
        active_service_key = service_key or self.service_key
        active_timeout = timeout if timeout is not None else self.timeout
        query = without_none(params or {})
        for attempt in range(self.retries + 1):
            await self._bucket.acquire()
            try:
                # 동기 클라이언트와 동일(#9): 빈 params는 URL query를 대체하므로
                # 비어 있으면 전달하지 않는다.
                if query:
                    response = await self.session.get(
                        url, params=query, timeout=active_timeout
                    )
                else:
                    response = await self.session.get(url, timeout=active_timeout)
            except httpx.HTTPError as exc:
                if attempt >= self.retries:
                    raise _network_error(url, exc, active_service_key) from exc
                await _async_sleep_before_retry(attempt)
                continue
            if response.status_code in TRANSIENT_STATUSES and attempt < self.retries:
                await _async_sleep_before_retry(attempt)
                continue
            _raise_for_status(response, endpoint=url, service_key=active_service_key)
            return response
        raise AssertionError("unreachable")

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
        response = await self.get_response(url, query, service_key=service_key, timeout=timeout)
        return response, _request_data(url, query), _response_data(response)

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
        except ValueError as exc:
            text = _redact(response.text[:300], active_service_key)
            raise McstParseError(
                f"response was not valid JSON: {text}",
                endpoint=url,
                failure_kind="parse",
            ) from exc


class KcisaHttp(HttpClient):
    """culture.go.kr/KCISA OpenAPI 엔드포인트용 동기 HTTP 클라이언트입니다."""

    def get_page(
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
        response = self.get_response(
            endpoint_url, query, service_key=active_service_key, timeout=timeout
        )
        return _normalized_response(
            response,
            endpoint_url,
            active_service_key,
            page_no,
            num_of_rows,
        )

    def get_debug_page(
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
        response, request_data, response_data = self.get_debug_response(
            endpoint_url,
            query,
            service_key=active_service_key,
            timeout=timeout,
        )
        payload = _decode_payload(response)
        response_data["body"] = redact_sensitive(payload)
        normalized = _normalize_payload(payload, page_no=page_no, num_of_rows=num_of_rows)
        _raise_for_payload_error(normalized.raw, endpoint_url, service_key=active_service_key)
        return normalized, request_data, response_data


class AsyncKcisaHttp(AsyncHttpClient):
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
        payload = _decode_payload(response)
        response_data["body"] = redact_sensitive(payload)
        normalized = _normalize_payload(payload, page_no=page_no, num_of_rows=num_of_rows)
        _raise_for_payload_error(normalized.raw, endpoint_url, service_key=active_service_key)
        return normalized, request_data, response_data


class OdcloudHttp(HttpClient):
    """data.go.kr 자동변환 파일 API용 동기 HTTP 클라이언트입니다."""

    base_url = "https://api.odcloud.kr/api"

    def get_page(
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
        payload = self.get_json(url, query, service_key=active_service_key, timeout=timeout)
        return _normalized_odcloud_payload(payload, url, page_no, per_page, active_service_key)

    def get_debug_page(
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
        response, request_data, response_data = self.get_debug_response(
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


class AsyncOdcloudHttp(AsyncHttpClient):
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


def _response_data(response: ResponseLike) -> dict[str, Any]:
    return {
        "status_code": response.status_code,
        "headers": dict(response.headers),
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
    payload = _decode_payload(response)
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
        page_no=to_int_or_none(payload.get("page")) or page_no,
        num_of_rows=to_int_or_none(payload.get("perPage")) or per_page,
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


def _sleep_before_retry(attempt: int) -> None:
    backoff = 0.3 * (2**attempt)
    jitter = random.uniform(0, 0.1 * backoff)
    time.sleep(min(backoff + jitter, 4.0))


async def _async_sleep_before_retry(attempt: int) -> None:
    backoff = 0.3 * (2**attempt)
    jitter = random.uniform(0, 0.1 * backoff)
    await asyncio.sleep(min(backoff + jitter, 4.0))


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
        payload = response.json()
    except ValueError:
        return
    if not isinstance(payload, Mapping):
        return
    code = str(payload.get("code") or payload.get("resultCode") or "").strip()
    message = str(payload.get("msg") or payload.get("message") or payload.get("resultMsg") or "")
    text = _redact(f"HTTP {response.status_code}: {code}: {message}", service_key)
    upper = text.upper()
    if code in {"-4", "-401", "20", "30", "31"} or "SERVICE" in upper or "인증" in text:
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


def _decode_payload(response: ResponseLike) -> Any:
    content_type = response.headers.get("Content-Type", "").casefold()
    text = response.text.strip()
    if "json" in content_type or text.startswith("{") or text.startswith("["):
        return _json_payload(response, "", None)
    if text.startswith("<"):
        try:
            root = ElementTree.fromstring(text)
        except ElementTree.ParseError as exc:
            raise McstParseError("response was not valid XML", failure_kind="parse") from exc
        return _element_to_data(root)
    raise McstParseError(
        f"unsupported response body from {urlparse(str(response)).netloc}",
        failure_kind="parse",
    )


def _json_payload(response: ResponseLike, endpoint: str, service_key: str | None) -> Any:
    try:
        return response.json()
    except ValueError as exc:
        text = _redact(response.text[:300], service_key)
        raise McstParseError(
            f"response was not valid JSON: {text}",
            endpoint=endpoint,
            failure_kind="parse",
        ) from exc


def _element_to_data(element: ElementTree.Element) -> Any:
    children = list(element)
    text = (element.text or "").strip()
    if not children:
        return text

    grouped: dict[str, list[Any]] = defaultdict(list)
    for child in children:
        tag = child.tag.rsplit("}", 1)[-1]
        grouped[tag].append(_element_to_data(child))
    data: dict[str, Any] = {}
    for tag, values in grouped.items():
        data[tag] = values[0] if len(values) == 1 else values
    if text:
        data["_text"] = text
    return data


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
        page_no=to_int_or_none(body.get("pageNo") or body.get("page")) or page_no,
        num_of_rows=to_int_or_none(body.get("numOfRows") or body.get("perPage")) or num_of_rows,
        total_count=to_int_or_none(body.get("totalCount") or body.get("totalCnt")),
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


def _raise_for_payload_error(payload: Any, endpoint: str, *, service_key: str | None) -> None:
    if not isinstance(payload, Mapping):
        return
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
    if not code or code in {"0", "00", "0000", "NORMAL_CODE", "INFO-000"}:
        return
    text = _redact(f"{code}: {message}", service_key)
    upper = text.upper()
    if code in {"-4", "-401", "20", "30", "31"} or "SERVICE" in upper or "인증" in text:
        raise McstAuthError(text, result_code=code, endpoint=endpoint, failure_kind="auth")
    if code in {"03", "INFO-200"} or "NO DATA" in upper:
        raise McstNoDataError(text, result_code=code, endpoint=endpoint, failure_kind="no_data")
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
    cleaned = secret.strip().strip('"').strip("'")
    for candidate in {secret, cleaned}:
        if candidate:
            redacted = redacted.replace(candidate, "[redacted]")
    return redacted


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
