"""선별된 문체부 파일데이터 다운로드 클라이언트입니다."""

from __future__ import annotations

import asyncio
import csv
from collections.abc import Iterator
from pathlib import Path
from types import TracebackType
from typing import Any

from ._http import AsyncHttpClient, AsyncSessionLike, HttpClient, SessionLike
from .catalog import ALL_DATASETS, CatalogEntry, DatasetKind, get_dataset
from .exceptions import McstRequestError


class FileDataClient:
    """선별된 파일데이터를 다운로드하고 읽습니다."""

    def __init__(
        self,
        *,
        timeout: float = 20.0,
        retries: int = 3,
        session: SessionLike | None = None,
    ) -> None:
        self._http = HttpClient(timeout=timeout, retries=retries, session=session)
        self.closed = False

    def __enter__(self) -> FileDataClient:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    def close(self) -> None:
        self._http.close()
        self.closed = True

    def datasets(self) -> tuple[CatalogEntry, ...]:
        """다운로드 또는 연결 URL이 있는 항목을 반환합니다."""

        return tuple(entry for entry in ALL_DATASETS.values() if entry.file_url)

    def download(self, dataset: str | CatalogEntry) -> bytes:
        """선별된 파일데이터 또는 연결 원천 URL을 다운로드합니다."""

        entry = _resolve_download(dataset)
        if not entry.file_url:
            raise McstRequestError(f"{entry.slug} does not have a file URL")
        return self._http.get_bytes(entry.file_url)

    def save(
        self,
        dataset: str | CatalogEntry,
        path: str | Path,
        *,
        overwrite: bool = False,
    ) -> Path:
        """데이터셋을 `path`로 다운로드합니다."""

        target = Path(path)
        if target.exists() and not overwrite:
            raise FileExistsError(str(target))
        data = self.download(dataset)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        return target

    def save_rustfs(
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
        """데이터셋을 로컬 `path`에 다운로드하고 동시에 S3 호환 RustFS에도 저장합니다.

        boto3 라이브러리가 런타임에 설치되어 있어야 합니다.
        접속 정보가 생략된 경우 환경변수에서 조회합니다.
        (우선순위: MCST_RUSTFS_* -> KRTOUR_MAP_OBJECT_STORE_* -> AWS_*)
        """
        target = Path(path)
        if target.exists() and not overwrite:
            raise FileExistsError(str(target))

        creds = _resolve_rustfs_credentials(
            bucket=bucket,
            endpoint_url=endpoint_url,
            region_name=region_name,
            access_key_id=access_key_id,
            secret_access_key=secret_access_key,
        )
        s3_client = _get_boto3_s3_client(creds)

        # 1. 다운로드
        data = self.download(dataset)

        # 2. 로컬 저장
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)

        # 3. RustFS (S3) 저장
        key = object_key or target.name
        try:
            s3_client.put_object(
                Bucket=creds["bucket"],
                Key=key,
                Body=data,
                ContentType="text/csv" if key.endswith(".csv") else "application/octet-stream",
            )
        except Exception as exc:
            raise RuntimeError(
                f"RustFS 업로드 실패: bucket={creds['bucket']!r}, key={key!r}"
            ) from exc

        return target

    def read_csv(
        self,
        dataset: str | CatalogEntry,
        *,
        encoding: str | None = None,
    ) -> list[dict[str, str]]:
        """CSV 파일을 다운로드해 딕셔너리 목록으로 파싱합니다."""

        return list(self.iter_csv(dataset, encoding=encoding))

    def iter_csv(
        self,
        dataset: str | CatalogEntry,
        *,
        encoding: str | None = None,
    ) -> Iterator[dict[str, str]]:
        """다운로드한 CSV 파일의 행을 순회합니다."""

        entry = _resolve_download(dataset)
        if entry.kind == DatasetKind.LINK:
            raise McstRequestError(f"{entry.slug} is a link entry, not a direct CSV")
        raw = self.download(entry)
        text = _decode_csv_bytes(raw, encoding)
        reader = csv.DictReader(text.splitlines())
        for row in reader:
            yield dict(row)


class AsyncFileDataClient:
    """선별된 파일데이터를 비동기로 다운로드하고 읽습니다."""

    def __init__(
        self,
        *,
        timeout: float = 20.0,
        retries: int = 3,
        session: AsyncSessionLike | None = None,
        max_rps: float = 5.0,
    ) -> None:
        self._http = AsyncHttpClient(
            timeout=timeout,
            retries=retries,
            session=session,
            max_rps=max_rps,
        )
        self.closed = False

    async def __aenter__(self) -> AsyncFileDataClient:
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

        return tuple(entry for entry in ALL_DATASETS.values() if entry.file_url)

    async def download(self, dataset: str | CatalogEntry) -> bytes:
        """선별된 파일데이터 또는 연결 원천 URL을 비동기로 다운로드합니다."""

        entry = _resolve_download(dataset)
        if not entry.file_url:
            raise McstRequestError(f"{entry.slug} does not have a file URL")
        return await self._http.get_bytes(entry.file_url)

    async def save(
        self,
        dataset: str | CatalogEntry,
        path: str | Path,
        *,
        overwrite: bool = False,
    ) -> Path:
        """데이터셋을 `path`로 비동기 다운로드합니다."""

        target = Path(path)
        if target.exists() and not overwrite:
            raise FileExistsError(str(target))
        data = await self.download(dataset)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
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

        boto3 라이브러리가 런타임에 설치되어 있어야 합니다.
        접속 정보가 생략된 경우 환경변수에서 조회합니다.
        (우선순위: MCST_RUSTFS_* -> KRTOUR_MAP_OBJECT_STORE_* -> AWS_*)
        """
        target = Path(path)
        if target.exists() and not overwrite:
            raise FileExistsError(str(target))

        creds = _resolve_rustfs_credentials(
            bucket=bucket,
            endpoint_url=endpoint_url,
            region_name=region_name,
            access_key_id=access_key_id,
            secret_access_key=secret_access_key,
        )
        s3_client = _get_boto3_s3_client(creds)

        # 1. 다운로드
        data = await self.download(dataset)

        # 2. 로컬 저장
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)

        # 3. RustFS (S3) 저장
        key = object_key or target.name
        try:
            await asyncio.to_thread(
                s3_client.put_object,
                Bucket=creds["bucket"],
                Key=key,
                Body=data,
                ContentType="text/csv" if key.endswith(".csv") else "application/octet-stream",
            )
        except Exception as exc:
            raise RuntimeError(
                f"RustFS 업로드 실패: bucket={creds['bucket']!r}, key={key!r}"
            ) from exc

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
        text = _decode_csv_bytes(raw, encoding)
        return [dict(row) for row in csv.DictReader(text.splitlines())]


def _resolve_download(dataset: str | CatalogEntry) -> CatalogEntry:
    if isinstance(dataset, CatalogEntry):
        return dataset
    return get_dataset(dataset)


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
        raise last_error
    return data.decode()


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


def _get_boto3_s3_client(creds: dict[str, Any]) -> Any:
    """접속 설정에 기초하여 boto3 S3 클라이언트를 생성합니다."""
    import importlib

    try:
        boto3 = importlib.import_module("boto3")
        botocore_config = importlib.import_module("botocore.config")
    except ImportError as exc:
        raise ImportError(
            "rustfs 저장 기능을 사용하려면 boto3 및 botocore 라이브러리가 필요합니다. "
            "pip install boto3를 실행해 설치하십시오."
        ) from exc

    client_kwargs: dict[str, Any] = {
        "region_name": creds["region_name"],
        "config": botocore_config.Config(signature_version="s3v4"),
    }
    if creds["endpoint_url"]:
        client_kwargs["endpoint_url"] = creds["endpoint_url"]
    if creds["aws_access_key_id"] and creds["aws_secret_access_key"]:
        client_kwargs["aws_access_key_id"] = creds["aws_access_key_id"]
        client_kwargs["aws_secret_access_key"] = creds["aws_secret_access_key"]

    return boto3.client("s3", **client_kwargs)
