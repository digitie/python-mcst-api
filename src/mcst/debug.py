"""디버그 실행 결과와 fixture 저장 헬퍼입니다."""

from __future__ import annotations

import json
import re
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass, is_dataclass
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from pydantic import BaseModel

SENSITIVE_KEYS = {
    "authorization",
    "x-api-key",
    "api_key",
    "apikey",
    "access_token",
    "refresh_token",
    "servicekey",
    "service_key",
}
DEFAULT_EXCLUDE_FIELDS = ("fetched_at", "request_id", "updated_at")
REDACTED = "<REDACTED>"


@dataclass(frozen=True, slots=True)
class DebugRun:
    """fixture로 저장할 수 있는 단일 디버그 실행 결과입니다."""

    function: str
    input: dict[str, Any]
    request: dict[str, Any]
    response: dict[str, Any]
    parsed: Any
    processed: Any
    trace: tuple[str, ...] = ()
    error: dict[str, Any] | None = None


def jsonable(value: Any) -> Any:
    """Pydantic 모델과 컨테이너를 JSON 저장 가능한 값으로 바꿉니다."""

    if isinstance(value, BaseModel):
        return value.model_dump(mode="json")
    if is_dataclass(value) and not isinstance(value, type):
        return jsonable(asdict(value))
    if isinstance(value, Mapping):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, tuple | list):
        return [jsonable(item) for item in value]
    return value


def redact_sensitive(value: Any) -> Any:
    """API 키와 인증 토큰이 fixture에 저장되지 않도록 제거합니다."""

    if isinstance(value, Mapping):
        result: dict[str, Any] = {}
        for key, item in value.items():
            text_key = str(key)
            if text_key.lower() in SENSITIVE_KEYS:
                result[text_key] = REDACTED
            else:
                result[text_key] = redact_sensitive(item)
        return result
    if isinstance(value, Sequence) and not isinstance(value, str | bytes | bytearray):
        return [redact_sensitive(item) for item in value]
    return value


def processed_page(value: BaseModel) -> dict[str, Any]:
    """회귀 비교에 쓸 안정적인 페이지 결과를 만듭니다.

    원본 응답은 fixture의 `response.body`가 보존하므로 processed snapshot에서는
    `raw`를 제외합니다.
    """

    data = value.model_dump(mode="json")
    data.pop("raw", None)
    return data


def error_to_dict(exc: BaseException) -> dict[str, Any]:
    """UI에서 표시하기 쉬운 예외 정보를 만듭니다."""

    data: dict[str, Any] = {
        "type": type(exc).__name__,
        "message": str(exc),
    }
    from .exceptions import McstError

    if isinstance(exc, McstError):
        for attr in ("failure_kind", "endpoint", "status_code", "result_code"):
            value = getattr(exc, attr)
            if value is not None:
                data[attr] = value
    return data


def default_assertion() -> dict[str, Any]:
    """fixture 저장 시 사용하는 기본 assertion 설정입니다."""

    return {
        "mode": "snapshot",
        "exclude_fields": list(DEFAULT_EXCLUDE_FIELDS),
        "required_fields": [],
    }


def fixture_from_debug_run(
    debug_run: DebugRun,
    *,
    case_name: str,
    description: str = "",
    assertion: Mapping[str, Any] | None = None,
    library_version: str | None = None,
) -> dict[str, Any]:
    """디버그 실행 결과를 표준 fixture 딕셔너리로 변환합니다."""

    safe_case_name = slugify(case_name)
    return {
        "name": safe_case_name,
        "function": debug_run.function,
        "description": description,
        "input": redact_sensitive(jsonable(debug_run.input)),
        "request": redact_sensitive(jsonable(debug_run.request)),
        "response": redact_sensitive(jsonable(debug_run.response)),
        "parsed": jsonable(debug_run.parsed),
        "processed": jsonable(debug_run.processed),
        "assertion": dict(assertion or default_assertion()),
        "meta": {
            "created_at": datetime.now(ZoneInfo("Asia/Seoul")).isoformat(),
            "library_version": library_version,
            "source": "debug_ui",
        },
    }


def save_fixture(
    debug_run: DebugRun,
    *,
    base_dir: str | Path,
    case_name: str,
    description: str = "",
    assertion: Mapping[str, Any] | None = None,
    library_version: str | None = None,
    overwrite: bool = False,
) -> Path:
    """디버그 실행 결과를 `tests/fixtures/{function}/{case}.json` 형태로 저장합니다."""

    fixture = fixture_from_debug_run(
        debug_run,
        case_name=case_name,
        description=description,
        assertion=assertion,
        library_version=library_version,
    )
    fixture_dir = Path(base_dir) / debug_run.function
    fixture_dir.mkdir(parents=True, exist_ok=True)
    fixture_path = fixture_dir / f"{fixture['name']}.json"
    if fixture_path.exists() and not overwrite:
        raise FileExistsError(f"Fixture already exists: {fixture_path}")
    fixture_path.write_text(json.dumps(fixture, ensure_ascii=False, indent=2), encoding="utf-8")
    return fixture_path


def slugify(value: str) -> str:
    """case 이름을 파일명으로 쓰기 안전한 slug로 바꿉니다."""

    normalized = re.sub(r"[^\w가-힣.-]+", "_", value.strip().lower())
    normalized = re.sub(r"_+", "_", normalized).strip("_.")
    if not normalized:
        raise ValueError("case_name must not be empty")
    return normalized
