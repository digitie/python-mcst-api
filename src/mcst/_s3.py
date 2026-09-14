"""기존 Mois의 SigV4 로직을 사용하는 비동기 RustFS 송신용 서명 함수."""

from __future__ import annotations

import hashlib
import hmac
from datetime import UTC, datetime
from typing import Any
from urllib.parse import quote

import httpx

_SERVICE = "s3"
_AWS4_REQUEST = "aws4_request"


def _canonical_header_value(value: str) -> str:
    return " ".join(value.split())


def canonical_query_string(query: dict[str, str]) -> str:
    pairs = []
    for key, value in sorted(query.items()):
        pairs.append(f"{quote(key, safe='-_.~')}={quote(value, safe='-_.~')}")
    return "&".join(pairs)


def _signing_key(secret_key: str, date_stamp: str, region: str) -> bytes:
    date_key = hmac.new(
        f"AWS4{secret_key}".encode(),
        date_stamp.encode(),
        hashlib.sha256,
    ).digest()
    region_key = hmac.new(date_key, region.encode(), hashlib.sha256).digest()
    service_key = hmac.new(region_key, _SERVICE.encode(), hashlib.sha256).digest()
    return hmac.new(service_key, _AWS4_REQUEST.encode(), hashlib.sha256).digest()


def _canonical_uri(*, bucket: str | None, key: str | None) -> str:
    parts: list[str] = []
    if bucket:
        parts.append(quote(bucket, safe="-_.~"))
    if key:
        parts.extend(quote(part, safe="-_.~") for part in key.split("/"))
    return "/" + "/".join(parts)


def _signed_request_helper(
    method: str,
    endpoint_url: str,
    parsed_endpoint: Any,
    bucket: str | None,
    key: str | None,
    query: dict[str, str] | None,
    headers: dict[str, str] | None,
    payload_hash: str,
    region: str,
    access_key: str | None = None,
    secret_key: str | None = None,
) -> tuple[str, dict[str, str]]:
    method = method.upper()
    request_time = datetime.now(UTC)
    amz_date = request_time.strftime("%Y%m%dT%H%M%SZ")
    date_stamp = request_time.strftime("%Y%m%d")
    prefix = httpx.URL(endpoint_url).raw_path.decode("ascii").rstrip("/")
    canonical_uri = prefix + _canonical_uri(bucket=bucket, key=key)
    canonical_query = canonical_query_string(query or {})
    url = f"{parsed_endpoint.scheme}://{parsed_endpoint.netloc}{canonical_uri}"
    if canonical_query:
        url = f"{url}?{canonical_query}"

    request_headers: dict[str, str] = {
        "host": parsed_endpoint.netloc,
        "x-amz-content-sha256": payload_hash,
        "x-amz-date": amz_date,
    }
    for name, value in (headers or {}).items():
        request_headers[name.lower()] = value.strip()

    canonical_headers = "".join(
        f"{name}:{_canonical_header_value(value)}\n"
        for name, value in sorted(request_headers.items())
    )
    signed_headers = ";".join(sorted(request_headers))
    canonical_request = "\n".join(
        [
            method,
            canonical_uri,
            canonical_query,
            canonical_headers,
            signed_headers,
            payload_hash,
        ]
    )
    credential_scope = f"{date_stamp}/{region}/{_SERVICE}/{_AWS4_REQUEST}"
    string_to_sign = "\n".join(
        [
            "AWS4-HMAC-SHA256",
            amz_date,
            credential_scope,
            hashlib.sha256(canonical_request.encode("utf-8")).hexdigest(),
        ]
    )
    signing_key = _signing_key(secret_key or "", date_stamp, region)
    signature = hmac.new(
        signing_key,
        string_to_sign.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    request_headers["authorization"] = (
        "AWS4-HMAC-SHA256 "
        f"Credential={access_key}/{credential_scope}, "
        f"SignedHeaders={signed_headers}, "
        f"Signature={signature}"
    )
    return url, request_headers
