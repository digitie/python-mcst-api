"""mcst 예외 계층입니다."""

from __future__ import annotations

from typing import Any


class McstError(Exception):
    """모든 mcst 오류의 기본 예외입니다."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        result_code: str | None = None,
        endpoint: str | None = None,
        failure_kind: str | None = None,
        response: Any | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.result_code = result_code
        self.endpoint = endpoint
        self.failure_kind = failure_kind
        self.response = response


class McstAuthError(McstError):
    """인증 또는 활용 신청 실패입니다."""


class McstRequestError(McstError):
    """잘못된 요청 또는 클라이언트 쪽 HTTP 오류입니다."""


class McstNoDataError(McstError):
    """상위 서비스가 데이터 없음 응답을 반환했습니다."""


class McstRateLimitError(McstError):
    """할당량 또는 호출 제한 오류입니다."""


class McstServerError(McstError):
    """상위 서버 오류입니다."""


class McstParseError(McstError):
    """응답 파싱 오류입니다."""
