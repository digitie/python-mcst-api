"""상위 편의 클라이언트입니다."""

from __future__ import annotations

from collections.abc import Mapping
from types import TracebackType
from typing import Any

from ._http import AsyncSessionLike, SessionLike
from .culture import AsyncCultureOpenApiClient, CultureOpenApiClient
from .data_go import AsyncDataGoFileApiClient, DataGoFileApiClient
from .file_data import AsyncFileDataClient, FileDataClient


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

    @classmethod
    def from_env(cls, **kwargs: Any) -> AsyncMcstClient:
        """지원 환경 변수에서 인증키를 읽어 비동기 클라이언트를 생성합니다."""

        return cls(**kwargs)
