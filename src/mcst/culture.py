"""culture.go.kr/KCISA OpenAPI 데이터셋 클라이언트입니다."""

from __future__ import annotations

import os
from collections.abc import Iterator, Mapping
from typing import Any

from ._http import KcisaHttp, SessionLike
from .catalog import CULTURE_OPEN_APIS, CatalogEntry, DatasetKind, get_dataset
from .exceptions import McstRequestError
from .models import CultureRecord, Page

DEFAULT_ENV_NAMES = (
    "TRIPMATE_DATA_GO_SERVICE_KEY",
    "MCST_SERVICE_KEY",
    "KCISA_SERVICE_KEY",
    "DATA_GO_SERVICE_KEY",
)


class CultureOpenApiClient:
    """culture.go.kr의 선별된 KCISA OpenAPI 엔드포인트 클라이언트입니다."""

    def __init__(
        self,
        service_key: str | None = None,
        *,
        timeout: float = 10.0,
        retries: int = 3,
        session: SessionLike | None = None,
    ) -> None:
        self.service_key = service_key or _first_env(DEFAULT_ENV_NAMES)
        self._http = KcisaHttp(
            service_key=self.service_key,
            timeout=timeout,
            retries=retries,
            session=session,
        )

    @classmethod
    def from_env(
        cls,
        name: str = "TRIPMATE_DATA_GO_SERVICE_KEY",
        *,
        fallback_names: tuple[str, ...] = (
            "MCST_SERVICE_KEY",
            "KCISA_SERVICE_KEY",
            "DATA_GO_SERVICE_KEY",
        ),
        **kwargs: Any,
    ) -> CultureOpenApiClient:
        service_key = os.getenv(name) or _first_env(fallback_names)
        return cls(service_key=service_key, **kwargs)

    def datasets(self) -> tuple[CatalogEntry, ...]:
        """지원하는 KCISA OpenAPI 카탈로그 항목을 반환합니다."""

        return tuple(CULTURE_OPEN_APIS.values())

    def request(
        self,
        dataset: str | CatalogEntry,
        *,
        keyword: str | None = None,
        page_no: int = 1,
        num_of_rows: int = 10,
        params: Mapping[str, Any] | None = None,
    ) -> Page[CultureRecord]:
        """선별된 KCISA OpenAPI 데이터셋을 호출합니다."""

        entry = _resolve_open_api(dataset)
        if not entry.endpoint_url:
            raise McstRequestError(f"{entry.slug} does not have an endpoint URL")
        _validate_page(page_no=page_no, num_of_rows=num_of_rows)
        payload = self._http.get_page(
            entry.endpoint_url,
            page_no=page_no,
            num_of_rows=num_of_rows,
            keyword=keyword,
            params=params,
        )
        return Page(
            items=tuple(CultureRecord.from_row(row) for row in payload.items),
            page_no=payload.page_no,
            num_of_rows=payload.num_of_rows,
            total_count=payload.total_count,
            raw=payload.raw,
            endpoint=entry.endpoint_url,
        )

    def iter_items(
        self,
        dataset: str | CatalogEntry,
        *,
        keyword: str | None = None,
        page_no: int = 1,
        num_of_rows: int = 100,
        max_pages: int | None = None,
        max_items: int | None = None,
        params: Mapping[str, Any] | None = None,
    ) -> Iterator[CultureRecord]:
        """여러 페이지의 레코드를 순회합니다."""

        yielded = 0
        current_page = page_no
        seen_pages = 0
        while True:
            page = self.request(
                dataset,
                keyword=keyword,
                page_no=current_page,
                num_of_rows=num_of_rows,
                params=params,
            )
            if not page.items:
                return
            for item in page.items:
                yield item
                yielded += 1
                if max_items is not None and yielded >= max_items:
                    return
            seen_pages += 1
            if max_pages is not None and seen_pages >= max_pages:
                return
            if page.total_count is not None and yielded >= page.total_count:
                return
            current_page += 1

    def media_famous_places(self, **kwargs: Any) -> Page[CultureRecord]:
        return self.request("media_famous_places", **kwargs)

    def barrier_free_places(self, **kwargs: Any) -> Page[CultureRecord]:
        return self.request("barrier_free_places", **kwargs)

    def pet_friendly_culture_facilities(self, **kwargs: Any) -> Page[CultureRecord]:
        return self.request("pet_friendly_culture_facilities", **kwargs)

    def leisure_activity_facilities(self, **kwargs: Any) -> Page[CultureRecord]:
        return self.request("leisure_activity_facilities", **kwargs)

    def leisure_camping_facilities(self, **kwargs: Any) -> Page[CultureRecord]:
        return self.request("leisure_camping_facilities", **kwargs)

    def family_infant_culture_facilities(self, **kwargs: Any) -> Page[CultureRecord]:
        return self.request("family_infant_culture_facilities", **kwargs)

    def multilingual_guide_culture_facilities(self, **kwargs: Any) -> Page[CultureRecord]:
        return self.request("multilingual_guide_culture_facilities", **kwargs)

    def world_restaurants(self, **kwargs: Any) -> Page[CultureRecord]:
        return self.request("world_restaurants", **kwargs)

    def small_theaters(self, **kwargs: Any) -> Page[CultureRecord]:
        return self.request("small_theaters", **kwargs)

    def meeting_seminar_facilities(self, **kwargs: Any) -> Page[CultureRecord]:
        return self.request("meeting_seminar_facilities", **kwargs)

    def independent_bookstores(self, **kwargs: Any) -> Page[CultureRecord]:
        return self.request("independent_bookstores", **kwargs)

    def cafe_bookstores(self, **kwargs: Any) -> Page[CultureRecord]:
        return self.request("cafe_bookstores", **kwargs)


def _resolve_open_api(dataset: str | CatalogEntry) -> CatalogEntry:
    if isinstance(dataset, CatalogEntry):
        entry = dataset
    else:
        entry = get_dataset(dataset)
    if entry.kind != DatasetKind.KCISA_OPEN_API:
        raise McstRequestError(f"{entry.slug} is not a KCISA OpenAPI dataset")
    return entry


def _first_env(names: tuple[str, ...]) -> str | None:
    for name in names:
        value = os.getenv(name)
        if value:
            return value.strip().strip('"').strip("'")
    return None


def _validate_page(*, page_no: int, num_of_rows: int) -> None:
    if page_no < 1:
        raise ValueError("page_no must be >= 1")
    if not 1 <= num_of_rows <= 1000:
        raise ValueError("num_of_rows must be between 1 and 1000")
