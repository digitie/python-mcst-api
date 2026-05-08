"""KCISA, data.go.kr, ODCloud 계열 API용 HTTP 도우미입니다."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Protocol, cast
from urllib.parse import urlparse
from xml.etree import ElementTree

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ._convert import to_int_or_none, without_none
from .exceptions import (
    McstAuthError,
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


TRANSIENT_STATUSES = {429, 500, 502, 503, 504}
DEFAULT_USER_AGENT = "Mozilla/5.0 (compatible; pymcst/0.1; +https://github.com/digitie/pymcst)"


@dataclass(frozen=True, slots=True)
class NormalizedPayload:
    items: tuple[dict[str, Any], ...]
    page_no: int
    num_of_rows: int
    total_count: int | None
    raw: Any


def build_session(retries: int = 3) -> SessionLike:
    """보수적인 GET 재시도를 적용한 requests 세션을 만듭니다."""

    session = requests.Session()
    session.headers.update({"User-Agent": DEFAULT_USER_AGENT})
    if retries <= 0:
        return cast(SessionLike, session)

    retry = Retry(
        total=retries,
        connect=retries,
        read=retries,
        status=retries,
        backoff_factor=0.3,
        status_forcelist=tuple(sorted(TRANSIENT_STATUSES)),
        allowed_methods=frozenset({"GET"}),
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return cast(SessionLike, session)


class HttpClient:
    """공통 오류 처리를 포함한 GET 호출 래퍼입니다."""

    def __init__(
        self,
        *,
        service_key: str | None = None,
        session: SessionLike | None = None,
        timeout: float = 10.0,
        retries: int = 3,
    ) -> None:
        self.service_key = service_key
        self.session = session or build_session(retries)
        self.timeout = timeout

    def get_response(self, url: str, params: Mapping[str, Any] | None = None) -> ResponseLike:
        response = self.session.get(url, params=without_none(params or {}), timeout=self.timeout)
        _raise_for_status(response, endpoint=url, service_key=self.service_key)
        return response

    def get_bytes(self, url: str, params: Mapping[str, Any] | None = None) -> bytes:
        return self.get_response(url, params).content

    def get_json(self, url: str, params: Mapping[str, Any] | None = None) -> Any:
        response = self.get_response(url, params)
        try:
            return response.json()
        except ValueError as exc:
            text = _redact(response.text[:300], self.service_key)
            raise McstParseError(
                f"response was not valid JSON: {text}",
                endpoint=url,
                failure_kind="parse",
            ) from exc


class KcisaHttp(HttpClient):
    """culture.go.kr/KCISA OpenAPI 엔드포인트용 HTTP 클라이언트입니다."""

    def get_page(
        self,
        endpoint_url: str,
        *,
        page_no: int,
        num_of_rows: int,
        keyword: str | None = None,
        params: Mapping[str, Any] | None = None,
    ) -> NormalizedPayload:
        if not self.service_key:
            raise McstAuthError(
                "service_key is required. Pass service_key=... or set "
                "TRIPMATE_DATA_GO_SERVICE_KEY.",
                endpoint=endpoint_url,
                failure_kind="auth",
            )
        query: dict[str, Any] = {
            "serviceKey": self.service_key,
            "numOfRows": num_of_rows,
            "pageNo": page_no,
            "keyword": keyword,
        }
        if params:
            query.update(params)
        response = self.get_response(endpoint_url, query)
        payload = _decode_payload(response)
        normalized = _normalize_payload(payload, page_no=page_no, num_of_rows=num_of_rows)
        _raise_for_payload_error(normalized.raw, endpoint_url, service_key=self.service_key)
        return normalized


class OdcloudHttp(HttpClient):
    """data.go.kr 자동변환 파일 API용 HTTP 클라이언트입니다."""

    base_url = "https://api.odcloud.kr/api"

    def get_page(
        self,
        public_data_pk: str,
        public_data_detail_pk: str,
        *,
        page_no: int,
        per_page: int,
        params: Mapping[str, Any] | None = None,
    ) -> NormalizedPayload:
        if not self.service_key:
            raise McstAuthError(
                "service_key is required. Pass service_key=... or set "
                "TRIPMATE_DATA_GO_SERVICE_KEY.",
                endpoint=public_data_pk,
                failure_kind="auth",
            )
        url = f"{self.base_url}/{public_data_pk}/v1/{public_data_detail_pk}"
        query: dict[str, Any] = {
            "page": page_no,
            "perPage": per_page,
            "serviceKey": self.service_key,
        }
        if params:
            query.update(params)
        payload = self.get_json(url, query)
        _raise_for_payload_error(payload, url, service_key=self.service_key)
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
        try:
            return response.json()
        except ValueError as exc:
            raise McstParseError("response was not valid JSON", failure_kind="parse") from exc
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
    if not secret:
        return text
    return text.replace(secret, "[redacted]")
