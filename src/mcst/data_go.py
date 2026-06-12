"""data.go.kr 자동변환 파일 API 클라이언트입니다.

2026-06-11 재편(#7) 이후 culture/도서관 CSV 데이터셋의 주요 경로는
`mcst.file_data`의 파일 다운로드(서비스키 불필요)입니다. 이 클라이언트는
ODCloud 식별자(`public_data_pk`)가 있는 항목에만 사용하며 서비스키가
필요합니다.
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from types import TracebackType
from typing import Any

from ._http import AsyncOdcloudHttp, AsyncSessionLike, OdcloudHttp, SessionLike
from .catalog import ALL_DATASETS, CatalogEntry, DatasetKind, get_dataset
from .debug import DebugRun, error_to_dict, processed_page
from .exceptions import McstAuthError, McstRequestError
from .models import Page, RawRecord

DEFAULT_ENV_NAMES = (
    "DATA_GO_KR_SERVICE_KEY",
)


class DataGoFileApiClient:
    """파일데이터에서 생성된 data.go.kr ODCloud API 클라이언트입니다."""

    def __init__(
        self,
        service_key: str | None = None,
        *,
        service_keys: Mapping[str, str] | None = None,
        timeout: float = 10.0,
        retries: int = 3,
        session: SessionLike | None = None,
        max_rps: float = 5.0,
    ) -> None:
        self.service_key = _clean_service_key(service_key) or _first_env(DEFAULT_ENV_NAMES)
        self.service_keys = _clean_service_keys(service_keys)
        self._http = OdcloudHttp(
            service_key=self.service_key,
            timeout=timeout,
            retries=retries,
            session=session,
        )
        self.max_rps = max_rps
        self.closed = False

    def __enter__(self) -> DataGoFileApiClient:
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

    @classmethod
    def aio(
        cls,
        service_key: str | None = None,
        *,
        service_keys: Mapping[str, str] | None = None,
        timeout: float = 10.0,
        retries: int = 3,
        session: AsyncSessionLike | None = None,
        max_rps: float = 5.0,
    ) -> AsyncDataGoFileApiClient:
        return AsyncDataGoFileApiClient(
            service_key=service_key,
            service_keys=service_keys,
            timeout=timeout,
            retries=retries,
            session=session,
            max_rps=max_rps,
        )

    @classmethod
    def from_env(cls, **kwargs: Any) -> DataGoFileApiClient:
        return cls(**kwargs)

    def datasets(self) -> tuple[CatalogEntry, ...]:
        """ODCloud API 식별자를 가진 파일데이터 항목을 반환합니다."""

        return tuple(
            entry
            for entry in ALL_DATASETS.values()
            if entry.kind != DatasetKind.LINK
            and entry.public_data_pk
            and entry.public_data_detail_pk
        )

    def service_key_for(self, dataset: str | CatalogEntry) -> str | None:
        """데이터셋/API별 서비스키를 반환합니다."""

        entry = _resolve_odcloud(dataset)
        return self.service_keys.get(entry.slug) or self.service_key

    def request(
        self,
        dataset: str | CatalogEntry,
        *,
        page_no: int = 1,
        per_page: int = 10,
        params: Mapping[str, Any] | None = None,
    ) -> Page[RawRecord]:
        """파일데이터의 data.go.kr 자동변환 API를 호출합니다."""

        entry = _resolve_odcloud(dataset)
        if not entry.public_data_pk or not entry.public_data_detail_pk:
            raise McstRequestError(f"{entry.slug} does not have ODCloud identifiers")
        _validate_page(page_no=page_no, per_page=per_page)
        service_key = self._require_service_key(entry)
        payload = self._http.get_page(
            entry.public_data_pk,
            entry.public_data_detail_pk,
            page_no=page_no,
            per_page=per_page,
            params=params,
            service_key=service_key,
        )
        return Page(
            items=payload.items,
            page_no=payload.page_no,
            num_of_rows=payload.num_of_rows,
            total_count=payload.total_count,
            raw=payload.raw,
            endpoint=f"{entry.public_data_pk}/{entry.public_data_detail_pk}",
        )

    def debug_request(
        self,
        dataset: str | CatalogEntry,
        *,
        page_no: int = 1,
        per_page: int = 10,
        params: Mapping[str, Any] | None = None,
    ) -> DebugRun:
        """UI fixture 생성에 사용할 ODCloud 디버그 실행 결과를 반환합니다."""

        dataset_name = dataset.slug if isinstance(dataset, CatalogEntry) else dataset
        input_data: dict[str, Any] = {
            "dataset": dataset_name,
            "page_no": page_no,
            "per_page": per_page,
            "params": dict(params or {}),
        }
        function_name = f"data_go.{dataset_name}"
        trace = ["ODCloud 카탈로그 항목 확인", "요청 파라미터 구성", "응답 파싱 및 Page 모델 생성"]
        try:
            entry = _resolve_odcloud(dataset)
            function_name = f"data_go.{entry.slug}"
            if not entry.public_data_pk or not entry.public_data_detail_pk:
                raise McstRequestError(f"{entry.slug} does not have ODCloud identifiers")
            _validate_page(page_no=page_no, per_page=per_page)
            service_key = self._require_service_key(entry)
            payload, request_data, response_data = self._http.get_debug_page(
                entry.public_data_pk,
                entry.public_data_detail_pk,
                page_no=page_no,
                per_page=per_page,
                params=params,
                service_key=service_key,
            )
            page: Page[RawRecord] = Page(
                items=payload.items,
                page_no=payload.page_no,
                num_of_rows=payload.num_of_rows,
                total_count=payload.total_count,
                raw=payload.raw,
                endpoint=f"{entry.public_data_pk}/{entry.public_data_detail_pk}",
            )
            return DebugRun(
                function=function_name,
                input=input_data,
                request=request_data,
                response=response_data,
                parsed=page,
                processed=processed_page(page),
                trace=tuple(trace),
            )
        except Exception as exc:
            return DebugRun(
                function=function_name,
                input=input_data,
                request={},
                response={},
                parsed=None,
                processed=None,
                trace=tuple(trace),
                error=error_to_dict(exc),
            )

    def public_libraries(self, **kwargs: Any) -> Page[RawRecord]:
        return self.request("public_libraries", **kwargs)

    def _require_service_key(self, entry: CatalogEntry) -> str:
        service_key = self.service_key_for(entry)
        if service_key:
            return service_key
        raise McstAuthError(
            f"service_key is required for dataset {entry.slug!r}. "
            "Pass service_key=... for a default key, or "
            f"service_keys={{{entry.slug!r}: '...'}} for an API-specific key.",
            endpoint=entry.public_data_pk,
            failure_kind="auth",
        )


class AsyncDataGoFileApiClient:
    """data.go.kr 자동변환 파일 API 비동기 클라이언트입니다."""

    def __init__(
        self,
        service_key: str | None = None,
        *,
        service_keys: Mapping[str, str] | None = None,
        timeout: float = 10.0,
        retries: int = 3,
        session: AsyncSessionLike | None = None,
        max_rps: float = 5.0,
    ) -> None:
        self.service_key = _clean_service_key(service_key) or _first_env(DEFAULT_ENV_NAMES)
        self.service_keys = _clean_service_keys(service_keys)
        self._http = AsyncOdcloudHttp(
            service_key=self.service_key,
            timeout=timeout,
            retries=retries,
            session=session,
            max_rps=max_rps,
        )
        self.closed = False

    async def __aenter__(self) -> AsyncDataGoFileApiClient:
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

    @classmethod
    def from_env(cls, **kwargs: Any) -> AsyncDataGoFileApiClient:
        return cls(**kwargs)

    def datasets(self) -> tuple[CatalogEntry, ...]:
        """ODCloud API 식별자를 가진 파일데이터 항목을 반환합니다."""

        return tuple(
            entry
            for entry in ALL_DATASETS.values()
            if entry.kind != DatasetKind.LINK
            and entry.public_data_pk
            and entry.public_data_detail_pk
        )

    def service_key_for(self, dataset: str | CatalogEntry) -> str | None:
        """데이터셋/API별 서비스키를 반환합니다."""

        entry = _resolve_odcloud(dataset)
        return self.service_keys.get(entry.slug) or self.service_key

    async def request(
        self,
        dataset: str | CatalogEntry,
        *,
        page_no: int = 1,
        per_page: int = 10,
        params: Mapping[str, Any] | None = None,
    ) -> Page[RawRecord]:
        """파일데이터의 data.go.kr 자동변환 API를 비동기로 호출합니다."""

        entry = _resolve_odcloud(dataset)
        if not entry.public_data_pk or not entry.public_data_detail_pk:
            raise McstRequestError(f"{entry.slug} does not have ODCloud identifiers")
        _validate_page(page_no=page_no, per_page=per_page)
        service_key = self._require_service_key(entry)
        payload = await self._http.get_page(
            entry.public_data_pk,
            entry.public_data_detail_pk,
            page_no=page_no,
            per_page=per_page,
            params=params,
            service_key=service_key,
        )
        return Page(
            items=payload.items,
            page_no=payload.page_no,
            num_of_rows=payload.num_of_rows,
            total_count=payload.total_count,
            raw=payload.raw,
            endpoint=f"{entry.public_data_pk}/{entry.public_data_detail_pk}",
        )

    async def debug_request(
        self,
        dataset: str | CatalogEntry,
        *,
        page_no: int = 1,
        per_page: int = 10,
        params: Mapping[str, Any] | None = None,
    ) -> DebugRun:
        """UI fixture 생성에 사용할 ODCloud 비동기 디버그 실행 결과를 반환합니다."""

        dataset_name = dataset.slug if isinstance(dataset, CatalogEntry) else dataset
        input_data: dict[str, Any] = {
            "dataset": dataset_name,
            "page_no": page_no,
            "per_page": per_page,
            "params": dict(params or {}),
        }
        function_name = f"data_go.{dataset_name}"
        trace = ["ODCloud 카탈로그 항목 확인", "요청 파라미터 구성", "응답 파싱 및 Page 모델 생성"]
        try:
            entry = _resolve_odcloud(dataset)
            function_name = f"data_go.{entry.slug}"
            if not entry.public_data_pk or not entry.public_data_detail_pk:
                raise McstRequestError(f"{entry.slug} does not have ODCloud identifiers")
            _validate_page(page_no=page_no, per_page=per_page)
            service_key = self._require_service_key(entry)
            payload, request_data, response_data = await self._http.get_debug_page(
                entry.public_data_pk,
                entry.public_data_detail_pk,
                page_no=page_no,
                per_page=per_page,
                params=params,
                service_key=service_key,
            )
            page: Page[RawRecord] = Page(
                items=payload.items,
                page_no=payload.page_no,
                num_of_rows=payload.num_of_rows,
                total_count=payload.total_count,
                raw=payload.raw,
                endpoint=f"{entry.public_data_pk}/{entry.public_data_detail_pk}",
            )
            return DebugRun(
                function=function_name,
                input=input_data,
                request=request_data,
                response=response_data,
                parsed=page,
                processed=processed_page(page),
                trace=tuple(trace),
            )
        except Exception as exc:
            return DebugRun(
                function=function_name,
                input=input_data,
                request={},
                response={},
                parsed=None,
                processed=None,
                trace=tuple(trace),
                error=error_to_dict(exc),
            )

    async def public_libraries(self, **kwargs: Any) -> Page[RawRecord]:
        return await self.request("public_libraries", **kwargs)

    def _require_service_key(self, entry: CatalogEntry) -> str:
        service_key = self.service_key_for(entry)
        if service_key:
            return service_key
        raise McstAuthError(
            f"service_key is required for dataset {entry.slug!r}. "
            "Pass service_key=... for a default key, or "
            f"service_keys={{{entry.slug!r}: '...'}} for an API-specific key.",
            endpoint=entry.public_data_pk,
            failure_kind="auth",
        )


def _resolve_odcloud(dataset: str | CatalogEntry) -> CatalogEntry:
    if isinstance(dataset, CatalogEntry):
        entry = dataset
    else:
        entry = get_dataset(dataset)
    if entry.kind not in {DatasetKind.DATA_GO_FILE_API, DatasetKind.FILE_DOWNLOAD}:
        raise McstRequestError(f"{entry.slug} is not a data.go.kr file API dataset")
    return entry


def _first_env(names: tuple[str, ...]) -> str | None:
    for name in names:
        value = _clean_service_key(os.getenv(name))
        if value:
            return value
    return None


def _clean_service_key(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip().strip('"').strip("'").strip()
    return cleaned or None


def _clean_service_keys(values: Mapping[str, str] | None) -> dict[str, str]:
    if not values:
        return {}
    result: dict[str, str] = {}
    for dataset, service_key in values.items():
        cleaned = _clean_service_key(service_key)
        if cleaned:
            result[str(dataset)] = cleaned
    return result


def _validate_page(*, page_no: int, per_page: int) -> None:
    if page_no < 1:
        raise ValueError("page_no must be >= 1")
    if not 1 <= per_page <= 1000:
        raise ValueError("per_page must be between 1 and 1000")
