"""data.go.kr 자동변환 파일 API 클라이언트입니다."""

from __future__ import annotations

import os
from collections.abc import Mapping
from typing import Any

from ._http import OdcloudHttp, SessionLike
from .catalog import FILE_DATASETS, CatalogEntry, DatasetKind, get_dataset
from .exceptions import McstRequestError
from .models import Page, RawRecord

DEFAULT_ENV_NAMES = (
    "TRIPMATE_DATA_GO_SERVICE_KEY",
    "DATA_GO_SERVICE_KEY",
    "MCST_SERVICE_KEY",
)


class DataGoFileApiClient:
    """파일데이터에서 생성된 data.go.kr ODCloud API 클라이언트입니다."""

    def __init__(
        self,
        service_key: str | None = None,
        *,
        timeout: float = 10.0,
        retries: int = 3,
        session: SessionLike | None = None,
    ) -> None:
        self.service_key = service_key or _first_env(DEFAULT_ENV_NAMES)
        self._http = OdcloudHttp(
            service_key=self.service_key,
            timeout=timeout,
            retries=retries,
            session=session,
        )

    @classmethod
    def from_env(cls, **kwargs: Any) -> DataGoFileApiClient:
        return cls(**kwargs)

    def datasets(self) -> tuple[CatalogEntry, ...]:
        """ODCloud API 식별자를 가진 파일데이터 항목을 반환합니다."""

        return tuple(
            entry
            for entry in FILE_DATASETS.values()
            if entry.public_data_pk and entry.public_data_detail_pk
        )

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
        payload = self._http.get_page(
            entry.public_data_pk,
            entry.public_data_detail_pk,
            page_no=page_no,
            per_page=per_page,
            params=params,
        )
        return Page(
            items=payload.items,
            page_no=payload.page_no,
            num_of_rows=payload.num_of_rows,
            total_count=payload.total_count,
            raw=payload.raw,
            endpoint=f"{entry.public_data_pk}/{entry.public_data_detail_pk}",
        )

    def leisure_activity_facilities(self, **kwargs: Any) -> Page[RawRecord]:
        return self.request("leisure_activity_facilities_csv", **kwargs)

    def leisure_camping_facilities(self, **kwargs: Any) -> Page[RawRecord]:
        return self.request("leisure_camping_facilities_csv", **kwargs)

    def leisure_classes(self, **kwargs: Any) -> Page[RawRecord]:
        return self.request("leisure_classes_csv", **kwargs)

    def public_libraries(self, **kwargs: Any) -> Page[RawRecord]:
        return self.request("public_libraries", **kwargs)

    def small_libraries(self, **kwargs: Any) -> Page[RawRecord]:
        return self.request("small_libraries", **kwargs)


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
        value = os.getenv(name)
        if value:
            return value.strip().strip('"').strip("'")
    return None


def _validate_page(*, page_no: int, per_page: int) -> None:
    if page_no < 1:
        raise ValueError("page_no must be >= 1")
    if not 1 <= per_page <= 1000:
        raise ValueError("per_page must be between 1 and 1000")
