"""상위 편의 클라이언트입니다."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .culture import CultureOpenApiClient
from .data_go import DataGoFileApiClient
from .file_data import FileDataClient


class McstClient:
    """지원하는 문체부 데이터 접근면을 묶는 편의 진입점입니다."""

    def __init__(
        self,
        service_key: str | None = None,
        *,
        service_keys: Mapping[str, str] | None = None,
        timeout: float = 10.0,
        retries: int = 3,
        session: Any | None = None,
    ) -> None:
        self.culture = CultureOpenApiClient(
            service_key=service_key,
            service_keys=service_keys,
            timeout=timeout,
            retries=retries,
            session=session,
        )
        self.data_go = DataGoFileApiClient(
            service_key=service_key,
            service_keys=service_keys,
            timeout=timeout,
            retries=retries,
            session=session,
        )
        self.file_data = FileDataClient(
            timeout=max(timeout, 20.0),
            retries=retries,
            session=session,
        )

    @classmethod
    def from_env(cls, **kwargs: Any) -> McstClient:
        """지원 환경 변수에서 인증키를 읽어 클라이언트를 생성합니다."""

        return cls(**kwargs)
