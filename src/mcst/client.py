"""상위 편의 클라이언트입니다."""

from __future__ import annotations

from collections.abc import Mapping
from types import TracebackType
from typing import Any

from ._http import AsyncSessionLike, SessionLike
from .catalog import CatalogEntry, DatasetKind, get_dataset
from .culture import AsyncCultureOpenApiClient, CultureOpenApiClient
from .data_go import AsyncDataGoFileApiClient, DataGoFileApiClient
from .debug import DebugRun, error_to_dict
from .exceptions import McstRequestError
from .file_data import AsyncFileDataClient, FileDataClient

_DEBUG_FETCH_KINDS = (DatasetKind.KCISA_OPEN_API, DatasetKind.DATA_GO_FILE_API)


class McstClient:
    """지원하는 문체부 데이터 접근면을 묶는 편의 진입점입니다."""

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
        self.culture = CultureOpenApiClient(
            service_key=service_key,
            service_keys=service_keys,
            timeout=timeout,
            retries=retries,
            session=session,
            max_rps=max_rps,
        )
        self.data_go = DataGoFileApiClient(
            service_key=service_key,
            service_keys=service_keys,
            timeout=timeout,
            retries=retries,
            session=session,
            max_rps=max_rps,
        )
        self.file_data = FileDataClient(
            timeout=max(timeout, 20.0),
            retries=retries,
            session=session,
        )
        self.closed = False

    def __enter__(self) -> McstClient:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    def close(self) -> None:
        self.culture.close()
        self.data_go.close()
        self.file_data.close()
        self.closed = True

    def debug_fetch(
        self,
        dataset: str | CatalogEntry,
        *,
        params: Mapping[str, Any] | None = None,
        keyword: str | None = None,
        page_no: int = 1,
        num_of_rows: int = 10,
        timeout: float | None = None,
    ) -> DebugRun:
        """카탈로그 kind로 알맞은 하위 클라이언트에 라우팅하는 제네릭 디버그 실행입니다.

        데이터셋별 `if function_name == ...` 분기 대신 `CatalogEntry.kind`만 보고
        `self.culture`/`self.data_go` 중 하나로 위임합니다. Streamlit 디버그 UI가
        모든 데이터셋에 대해 이 메서드 하나만 호출하도록 설계했습니다.
        """

        entry = dataset if isinstance(dataset, CatalogEntry) else get_dataset(dataset)
        if entry.kind == DatasetKind.KCISA_OPEN_API:
            return self.culture.debug_request(
                entry,
                keyword=keyword,
                page_no=page_no,
                num_of_rows=num_of_rows,
                params=params,
                timeout=timeout,
            )
        if entry.kind == DatasetKind.DATA_GO_FILE_API:
            return self.data_go.debug_request(
                entry,
                page_no=page_no,
                per_page=num_of_rows,
                params=params,
            )
        return _unsupported_kind_run(
            entry, params=params, keyword=keyword, page_no=page_no, num_of_rows=num_of_rows
        )

    @classmethod
    def from_env(cls, **kwargs: Any) -> McstClient:
        """지원 환경 변수에서 인증키를 읽어 클라이언트를 생성합니다."""

        return cls(**kwargs)

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
    ) -> AsyncMcstClient:
        return AsyncMcstClient(
            service_key=service_key,
            service_keys=service_keys,
            timeout=timeout,
            retries=retries,
            session=session,
            max_rps=max_rps,
        )


class AsyncMcstClient:
    """지원하는 문체부 데이터 접근면을 묶는 비동기 편의 진입점입니다."""

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
        self.culture = AsyncCultureOpenApiClient(
            service_key=service_key,
            service_keys=service_keys,
            timeout=timeout,
            retries=retries,
            session=session,
            max_rps=max_rps,
        )
        self.data_go = AsyncDataGoFileApiClient(
            service_key=service_key,
            service_keys=service_keys,
            timeout=timeout,
            retries=retries,
            session=session,
            max_rps=max_rps,
        )
        self.file_data = AsyncFileDataClient(
            timeout=max(timeout, 20.0),
            retries=retries,
            session=session,
            max_rps=max_rps,
        )
        self.closed = False

    async def __aenter__(self) -> AsyncMcstClient:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        await self.culture.aclose()
        await self.data_go.aclose()
        await self.file_data.aclose()
        self.closed = True

    async def adebug_fetch(
        self,
        dataset: str | CatalogEntry,
        *,
        params: Mapping[str, Any] | None = None,
        keyword: str | None = None,
        page_no: int = 1,
        num_of_rows: int = 10,
        timeout: float | None = None,
    ) -> DebugRun:
        """`McstClient.debug_fetch()`의 비동기 버전입니다. 카탈로그 kind로만 라우팅합니다."""

        entry = dataset if isinstance(dataset, CatalogEntry) else get_dataset(dataset)
        if entry.kind == DatasetKind.KCISA_OPEN_API:
            return await self.culture.debug_request(
                entry,
                keyword=keyword,
                page_no=page_no,
                num_of_rows=num_of_rows,
                params=params,
                timeout=timeout,
            )
        if entry.kind == DatasetKind.DATA_GO_FILE_API:
            return await self.data_go.debug_request(
                entry,
                page_no=page_no,
                per_page=num_of_rows,
                params=params,
            )
        return _unsupported_kind_run(
            entry, params=params, keyword=keyword, page_no=page_no, num_of_rows=num_of_rows
        )

    @classmethod
    def from_env(cls, **kwargs: Any) -> AsyncMcstClient:
        """지원 환경 변수에서 인증키를 읽어 비동기 클라이언트를 생성합니다."""

        return cls(**kwargs)


def _unsupported_kind_run(
    entry: CatalogEntry,
    *,
    params: Mapping[str, Any] | None,
    keyword: str | None,
    page_no: int,
    num_of_rows: int,
) -> DebugRun:
    """`debug_fetch()`가 실시간 조회를 지원하지 않는 kind를 만났을 때 쓰는 DebugRun입니다.

    `FILE_DOWNLOAD`(csv 스크레이핑, 별도 파라미터 없음)와 `LINK`(외부 링크만 존재,
    호출 가능한 클라이언트 없음)는 이 메서드로 조회할 수 없습니다. 예외를 올리는
    대신 `error`가 채워진 `DebugRun`을 돌려주어 Streamlit UI가 그대로
    Validation Errors 탭에 표시할 수 있게 합니다.
    """

    supported = ", ".join(kind.value for kind in _DEBUG_FETCH_KINDS)
    exc = McstRequestError(
        f"{entry.slug} (kind={entry.kind.value}) does not support debug_fetch; "
        f"supported kinds: {supported}",
        failure_kind="unsupported_kind",
    )
    return DebugRun(
        function=f"mcst.{entry.slug}",
        input={
            "dataset": entry.slug,
            "keyword": keyword,
            "page_no": page_no,
            "num_of_rows": num_of_rows,
            "params": dict(params or {}),
        },
        request={},
        response={},
        parsed=None,
        processed=None,
        trace=(f"{entry.slug}: kind={entry.kind.value}는 debug_fetch에서 지원하지 않습니다.",),
        error=error_to_dict(exc),
    )
