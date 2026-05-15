"""culture.go.kr/KCISA OpenAPI 데이터셋 클라이언트입니다."""

from __future__ import annotations

import os
from collections.abc import Iterator, Mapping
from typing import Any

from ._http import KcisaHttp, SessionLike
from .catalog import CULTURE_OPEN_APIS, CatalogEntry, DatasetKind, get_dataset
from .debug import DebugRun, error_to_dict, processed_page
from .exceptions import McstAuthError, McstRequestError
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
        service_keys: Mapping[str, str] | None = None,
        timeout: float = 10.0,
        retries: int = 3,
        session: SessionLike | None = None,
    ) -> None:
        self.service_key = _clean_service_key(service_key) or _first_env(DEFAULT_ENV_NAMES)
        self.service_keys = _clean_service_keys(service_keys)
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
        service_key = _clean_service_key(os.getenv(name)) or _first_env(fallback_names)
        return cls(service_key=service_key, **kwargs)

    def datasets(self) -> tuple[CatalogEntry, ...]:
        """지원하는 KCISA OpenAPI 카탈로그 항목을 반환합니다."""

        return tuple(CULTURE_OPEN_APIS.values())

    def service_key_for(self, dataset: str | CatalogEntry) -> str | None:
        """데이터셋/API별 서비스키를 반환합니다.

        `service_keys`에 slug별 키가 있으면 우선 사용하고, 없으면 기존 단일
        `service_key` 값을 fallback으로 사용합니다.
        """

        entry = _resolve_open_api(dataset)
        return self.service_keys.get(entry.slug) or self.service_key

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
        service_key = self._require_service_key(entry)
        payload = self._http.get_page(
            entry.endpoint_url,
            page_no=page_no,
            num_of_rows=num_of_rows,
            keyword=keyword,
            params=params,
            service_key=service_key,
        )
        return Page(
            items=tuple(CultureRecord.from_row(row) for row in payload.items),
            page_no=payload.page_no,
            num_of_rows=payload.num_of_rows,
            total_count=payload.total_count,
            raw=payload.raw,
            endpoint=entry.endpoint_url,
        )

    def debug_request(
        self,
        dataset: str | CatalogEntry,
        *,
        keyword: str | None = None,
        page_no: int = 1,
        num_of_rows: int = 10,
        params: Mapping[str, Any] | None = None,
    ) -> DebugRun:
        """UI fixture 생성에 사용할 KCISA 디버그 실행 결과를 반환합니다."""

        dataset_name = dataset.slug if isinstance(dataset, CatalogEntry) else dataset
        input_data: dict[str, Any] = {
            "dataset": dataset_name,
            "keyword": keyword,
            "page_no": page_no,
            "num_of_rows": num_of_rows,
            "params": dict(params or {}),
        }
        function_name = f"culture.{dataset_name}"
        trace = ["KCISA 카탈로그 항목 확인", "요청 파라미터 구성", "응답 파싱 및 Page 모델 생성"]
        try:
            entry = _resolve_open_api(dataset)
            function_name = f"culture.{entry.slug}"
            if not entry.endpoint_url:
                raise McstRequestError(f"{entry.slug} does not have an endpoint URL")
            _validate_page(page_no=page_no, num_of_rows=num_of_rows)
            service_key = self._require_service_key(entry)
            payload, request_data, response_data = self._http.get_debug_page(
                entry.endpoint_url,
                page_no=page_no,
                num_of_rows=num_of_rows,
                keyword=keyword,
                params=params,
                service_key=service_key,
            )
            page: Page[CultureRecord] = Page(
                items=tuple(CultureRecord.from_row(row) for row in payload.items),
                page_no=payload.page_no,
                num_of_rows=payload.num_of_rows,
                total_count=payload.total_count,
                raw=payload.raw,
                endpoint=entry.endpoint_url,
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

    def _require_service_key(self, entry: CatalogEntry) -> str:
        service_key = self.service_key_for(entry)
        if service_key:
            return service_key
        raise McstAuthError(
            f"service_key is required for dataset {entry.slug!r}. "
            "Pass service_key=... for a default key, or "
            f"service_keys={{{entry.slug!r}: '...'}} for an API-specific key.",
            endpoint=entry.endpoint_url,
            failure_kind="auth",
        )


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


def _validate_page(*, page_no: int, num_of_rows: int) -> None:
    if page_no < 1:
        raise ValueError("page_no must be >= 1")
    if not 1 <= num_of_rows <= 1000:
        raise ValueError("num_of_rows must be between 1 and 1000")
