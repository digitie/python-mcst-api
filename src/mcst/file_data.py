"""선별된 문체부 파일데이터 다운로드 클라이언트입니다.

CSV 파일 이름에는 업로드 일시가 박혀 있어(`API_CIA_089_20260530182204.csv`
형태) 다운로드 URL을 하드코딩할 수 없습니다. 이 모듈은 다운로드 시점에
카탈로그 항목의 파일 다운로드 페이지(`detail_url`)를 스크레이핑해 현재
CSV 링크를 얻은 뒤 받습니다. 서비스키는 필요 없습니다.

- culture.go.kr `filedatDtl.do`: "파일 다운로드" 버튼의
  `onclick="fnFileDwld('https://big.kcisa.kr/common/bbsAtchFileDownload.do?...')"`
  에서 추출합니다.
- data.go.kr `fileData.do`: 페이지에 박힌 JSON-LD `contentUrl`
  (`https://www.data.go.kr/cmm/cmm/fileDownload.do?atchFileId=...`)에서
  추출합니다.
"""

from __future__ import annotations

import csv
import hashlib
import html as html_module
import io
import re
import zipfile
from collections.abc import AsyncIterator
from pathlib import Path
from types import TracebackType
from typing import Any
from urllib.parse import unquote, urljoin, urlsplit

import httpx

from ._file_io import run_file_io
from ._http import HttpClient, SessionLike
from ._ratelimit import AsyncTokenBucket
from ._s3 import _signed_request_helper
from .catalog import ALL_DATASETS, CatalogEntry, DatasetKind, get_dataset
from .exceptions import McstParseError, McstRequestError

_DOWNLOADABLE_KINDS = frozenset({DatasetKind.FILE_DOWNLOAD, DatasetKind.DATA_GO_FILE_API})
_CULTURE_FILE_URL_RE = re.compile(r"https://big\.kcisa\.kr/common/bbsAtchFileDownload\.do[^'\"<>]*")
_DATA_GO_FILE_URL_RE = re.compile(
    r"(?:https://www\.data\.go\.kr)?/cmm/cmm/fileDownload\.do\?[^'\"<>]*"
)


def extract_download_url(page_html: str, page_url: str) -> str | None:
    """파일 다운로드 페이지 HTML에서 현재 CSV 다운로드 링크를 추출합니다.

    링크를 찾지 못하면 None을 반환합니다. 추출된 링크의 한글/공백 query
    값은 percent-encoding으로 정규화합니다.
    """

    if "filedatDtl.do" in page_url:
        match = _CULTURE_FILE_URL_RE.search(page_html)
    elif "fileData.do" in page_url:
        match = _DATA_GO_FILE_URL_RE.search(page_html)
    else:
        return None
    if match is None:
        return None
    raw = html_module.unescape(match.group(0))
    try:
        return str(httpx.URL(urljoin(page_url, raw)))
    except httpx.InvalidURL as exc:
        raise McstParseError(
            f"could not parse extracted download link {raw!r} from {page_url}",
            endpoint=page_url,
            failure_kind="parse",
        ) from exc


class FileDataClient:
    """선별된 파일데이터를 비동기로 다운로드하고 읽습니다."""

    def __init__(
        self,
        *,
        timeout: float = 20.0,
        retries: int = 3,
        session: SessionLike | None = None,
        max_rps: float = 5.0,
        rate_limiter: AsyncTokenBucket | None = None,
    ) -> None:
        self.rate_limiter = rate_limiter if rate_limiter is not None else AsyncTokenBucket(max_rps)
        self._http = HttpClient(
            timeout=timeout,
            retries=retries,
            session=session,
            max_rps=max_rps,
            rate_limiter=self.rate_limiter,
        )
        self.closed = False

    async def __aenter__(self) -> FileDataClient:
        if self.closed:
            raise RuntimeError("client is closed")
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        await self._http.aclose()
        self.closed = True

    def datasets(self) -> tuple[CatalogEntry, ...]:
        """다운로드 또는 연결 URL이 있는 항목을 반환합니다."""

        return tuple(
            entry
            for entry in ALL_DATASETS.values()
            if entry.kind != DatasetKind.LINK
            and (entry.kind in _DOWNLOADABLE_KINDS or entry.file_url)
        )

    async def resolve_file_url(self, dataset: str | CatalogEntry) -> str:
        """파일 다운로드 페이지를 스크레이핑해 현재 CSV 링크를 반환합니다.

        파일 다운로드 데이터셋이 아니면 카탈로그의 고정 `file_url`을
        반환합니다.
        """

        entry = _resolve_download(dataset)
        if entry.kind == DatasetKind.LINK:
            raise McstRequestError(f"{entry.slug} is a link entry, not a downloadable file")
        if entry.kind in _DOWNLOADABLE_KINDS:
            page = await self._http.get_response(entry.detail_url)
            url = extract_download_url(page.text, entry.detail_url)
            if url:
                return url
            return _fallback_file_url(entry)
        if entry.file_url:
            return entry.file_url
        raise McstRequestError(f"{entry.slug} does not have a file URL")

    async def download(self, dataset: str | CatalogEntry) -> bytes:
        """선별된 파일데이터 또는 연결 원천 URL을 비동기로 다운로드합니다."""

        entry = _resolve_download(dataset)
        return await self._http.get_bytes(await self.resolve_file_url(entry))

    async def save(
        self,
        dataset: str | CatalogEntry,
        path: str | Path,
        *,
        overwrite: bool = False,
    ) -> Path:
        """데이터셋을 `path`로 비동기 다운로드합니다."""

        target = Path(path)
        if not overwrite and await run_file_io(target.exists):
            raise FileExistsError(str(target))
        data = await self.download(dataset)
        await run_file_io(_write_file, target, data, overwrite=overwrite)
        return target

    async def save_rustfs(
        self,
        dataset: str | CatalogEntry,
        path: str | Path,
        *,
        bucket: str | None = None,
        object_key: str | None = None,
        overwrite: bool = False,
        endpoint_url: str | None = None,
        region_name: str | None = None,
        access_key_id: str | None = None,
        secret_access_key: str | None = None,
    ) -> Path:
        """데이터셋을 로컬 `path`에 비동기로 다운로드하고 동시에 S3 호환 RustFS에도 저장합니다.

        HTTPX로 SigV4 PUT을 송신하며 파일 다운로드와 같은 TPS 버킷을 사용합니다.
        접속 정보가 생략된 경우 환경변수에서 조회합니다.
        (우선순위: MCST_RUSTFS_* -> KRTOUR_MAP_OBJECT_STORE_* -> AWS_*)
        """
        target = Path(path)
        if not overwrite and await run_file_io(target.exists):
            raise FileExistsError(str(target))

        creds = _resolve_rustfs_credentials(
            bucket=bucket,
            endpoint_url=endpoint_url,
            region_name=region_name,
            access_key_id=access_key_id,
            secret_access_key=secret_access_key,
        )
        _validate_rustfs_credentials(creds)
        key = object_key or target.name
        if any(part in {".", ".."} for part in key.split("/")):
            raise ValueError("RustFS object_key에 독립된 . 또는 .. 경로 조각을 사용할 수 없습니다")
        if not isinstance(self._http.session, httpx.AsyncClient):
            raise TypeError("RustFS requires an httpx.AsyncClient session")

        # 1. 다운로드
        data = await self.download(dataset)

        # 2. 로컬 저장
        await run_file_io(_write_file, target, data, overwrite=overwrite)

        # 3. RustFS (S3) 저장
        digest = await run_file_io(lambda: hashlib.sha256(data).hexdigest())
        await self.rate_limiter.acquire()
        session = self._http.session
        if not isinstance(session, httpx.AsyncClient):
            raise TypeError("RustFS requires an httpx.AsyncClient session")
        endpoint = str(creds["endpoint_url"]).rstrip("/")
        url, headers = _signed_request_helper(
            "PUT",
            endpoint,
            urlsplit(endpoint),
            str(creds["bucket"]),
            key,
            None,
            {"content-type": "text/csv" if key.endswith(".csv") else "application/octet-stream"},
            digest,
            str(creds["region_name"]),
            creds["aws_access_key_id"],
            creds["aws_secret_access_key"],
        )
        try:
            request = httpx.Request(
                "PUT",
                url,
                headers=headers,
                content=data,
                extensions={"timeout": httpx.Timeout(self._http.timeout).as_dict()},
            )
            response = await session.send(request, auth=None, follow_redirects=False)
        except httpx.HTTPError:
            raise RuntimeError("RustFS 업로드 연결 실패") from None
        try:
            if not 200 <= response.status_code < 300:
                raise RuntimeError(f"RustFS 업로드 실패: HTTP {response.status_code}")
        finally:
            await response.aclose()

        return target

    async def read_csv(
        self,
        dataset: str | CatalogEntry,
        *,
        encoding: str | None = None,
    ) -> list[dict[str, str]]:
        """CSV 파일을 비동기로 다운로드해 딕셔너리 목록으로 파싱합니다."""

        entry = _resolve_download(dataset)
        if entry.kind == DatasetKind.LINK:
            raise McstRequestError(f"{entry.slug} is a link entry, not a direct CSV")
        raw = await self.download(entry)
        return await run_file_io(_parse_csv_rows, raw, entry.slug, encoding)

    async def iter_csv(
        self,
        dataset: str | CatalogEntry,
        *,
        encoding: str | None = None,
    ) -> AsyncIterator[dict[str, str]]:
        """CSV를 다운로드·파싱한 후 행을 비동기로 순회합니다."""
        for row in await self.read_csv(dataset, encoding=encoding):
            yield row


def _parse_csv_rows(raw: bytes, slug: str, encoding: str | None) -> list[dict[str, str]]:
    raw = _extract_csv_bytes(raw, slug)
    text = _decode_csv_bytes(raw, encoding)
    return [dict(row) for row in csv.DictReader(text.splitlines())]


def _validate_rustfs_credentials(creds: dict[str, Any]) -> None:
    if not creds["aws_access_key_id"] or not creds["aws_secret_access_key"]:
        raise ValueError("RustFS access key와 secret key를 지정해야 합니다")
    endpoint = urlsplit(str(creds["endpoint_url"]))
    if any(part in {".", ".."} for part in unquote(endpoint.path).split("/")):
        raise ValueError("RustFS endpoint에 독립된 . 또는 .. 경로 조각을 사용할 수 없습니다")
    if (
        endpoint.scheme not in {"http", "https"}
        or not endpoint.netloc
        or endpoint.username
        or endpoint.password
        or endpoint.query
        or endpoint.fragment
    ):
        raise ValueError("RustFS endpoint URL 형식이 올바르지 않습니다")


def _resolve_download(dataset: str | CatalogEntry) -> CatalogEntry:
    if isinstance(dataset, CatalogEntry):
        return dataset
    return get_dataset(dataset)


def _fallback_file_url(entry: CatalogEntry) -> str:
    if entry.file_url:
        return entry.file_url
    raise McstParseError(
        f"could not find a CSV download link on {entry.detail_url}",
        endpoint=entry.detail_url,
        failure_kind="parse",
    )


_ZIP_MAGIC = b"PK\x03\x04"


def _extract_csv_bytes(data: bytes, slug: str) -> bytes:
    if not data.startswith(_ZIP_MAGIC):
        return data
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            csv_names = [name for name in archive.namelist() if name.lower().endswith(".csv")]
            if not csv_names:
                raise McstParseError(
                    f"{slug}: downloaded zip archive has no CSV member",
                    failure_kind="parse",
                )
            return archive.read(csv_names[0])
    except zipfile.BadZipFile as exc:
        raise McstParseError(
            f"{slug}: downloaded file looked like a zip archive but could not be read",
            failure_kind="parse",
        ) from exc


def _decode_csv_bytes(data: bytes, encoding: str | None) -> str:
    encodings = (encoding,) if encoding else ("utf-8-sig", "utf-8", "cp949", "euc-kr")
    last_error: UnicodeDecodeError | None = None
    for candidate in encodings:
        if candidate is None:
            continue
        try:
            return data.decode(candidate)
        except UnicodeDecodeError as exc:
            last_error = exc
    if last_error is not None:
        raise McstParseError(
            f"could not decode CSV bytes with any of {encodings}",
            failure_kind="parse",
        ) from last_error
    return data.decode()


def _write_file(target: Path, data: bytes, *, overwrite: bool = False) -> None:
    """`target`의 부모 디렉터리를 만들고 `data`를 씁니다.

    동기 블로킹 파일시스템 호출이므로, 비동기 호출부는 이벤트 루프를 막지
    않도록 반드시 `run_file_io(_write_file, ...)`로 감싼다.
    """
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("wb" if overwrite else "xb") as handle:
        handle.write(data)


def _resolve_rustfs_credentials(
    bucket: str | None = None,
    endpoint_url: str | None = None,
    region_name: str | None = None,
    access_key_id: str | None = None,
    secret_access_key: str | None = None,
) -> dict[str, Any]:
    """환경변수 및 명시적 매개변수로부터 RustFS(S3 호환) 접속 정보를 로딩합니다."""
    import os

    res_endpoint = (
        endpoint_url
        or os.getenv("MCST_RUSTFS_ENDPOINT_URL")
        or os.getenv("RUSTFS_ENDPOINT")
        or os.getenv("KRTOUR_MAP_OBJECT_STORE_ENDPOINT_URL")
        or "http://127.0.0.1:9003"
    )
    res_bucket = (
        bucket
        or os.getenv("MCST_RUSTFS_BUCKET")
        or os.getenv("RUSTFS_BUCKET")
        or os.getenv("KRTOUR_MAP_OBJECT_STORE_BUCKET")
        or "krtour-map"
    )
    res_region = (
        region_name
        or os.getenv("MCST_RUSTFS_REGION")
        or os.getenv("RUSTFS_REGION")
        or os.getenv("KRTOUR_MAP_OBJECT_STORE_REGION")
        or os.getenv("AWS_DEFAULT_REGION")
        or "us-east-1"
    )

    res_access_key = (
        access_key_id
        or os.getenv("MCST_RUSTFS_ACCESS_KEY_ID")
        or os.getenv("RUSTFS_ACCESS_KEY")
        or os.getenv("KRTOUR_MAP_OBJECT_STORE_ACCESS_KEY_ID")
        or os.getenv("AWS_ACCESS_KEY_ID")
    )
    res_secret_key = (
        secret_access_key
        or os.getenv("MCST_RUSTFS_SECRET_ACCESS_KEY")
        or os.getenv("RUSTFS_SECRET_KEY")
        or os.getenv("KRTOUR_MAP_OBJECT_STORE_SECRET_ACCESS_KEY")
        or os.getenv("AWS_SECRET_ACCESS_KEY")
    )

    return {
        "endpoint_url": res_endpoint,
        "bucket": res_bucket,
        "region_name": res_region,
        "aws_access_key_id": res_access_key,
        "aws_secret_access_key": res_secret_key,
    }
