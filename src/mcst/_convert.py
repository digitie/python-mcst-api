"""클라이언트가 공유하는 작은 변환 도우미입니다."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


def strip_or_none(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def to_int_or_none(value: Any) -> int | None:
    text = strip_or_none(value)
    if text is None:
        return None
    try:
        return int(float(text.replace(",", "")))
    except ValueError:
        return None


def to_float_or_none(value: Any) -> float | None:
    text = strip_or_none(value)
    if text is None:
        return None
    try:
        return float(text.replace(",", ""))
    except ValueError:
        return None


def without_none(params: Mapping[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in params.items() if value is not None}


def first_value(row: Mapping[str, Any], *names: str) -> Any:
    folded = {str(key).casefold(): value for key, value in row.items()}
    for name in names:
        if name in row:
            return row[name]
        value = folded.get(name.casefold())
        if value is not None:
            return value
    return None
