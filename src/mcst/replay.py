"""저장된 fixture response를 외부 API 호출 없이 다시 처리하는 헬퍼입니다."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ._convert import to_int_or_none
from ._http import _normalize_payload, _rows_to_tuple
from .exceptions import McstParseError, McstRequestError
from .models import CultureRecord, Page, RawRecord


def replay_case(case: Mapping[str, Any]) -> dict[str, Any]:
    """표준 fixture case를 replay하고 processed snapshot을 반환합니다."""

    function = str(case.get("function") or "")
    response = case.get("response")
    if not isinstance(response, Mapping):
        raise McstParseError("fixture response must be an object")
    body = response.get("body")
    input_data = case.get("input")
    if not isinstance(input_data, Mapping):
        input_data = {}

    if function.startswith("culture."):
        culture_page = process_culture_body(body, input_data=input_data)
        data = culture_page.model_dump(mode="json")
    elif function.startswith("data_go."):
        data_go_page = process_data_go_body(body, input_data=input_data)
        data = data_go_page.model_dump(mode="json")
    else:
        raise McstRequestError(f"unknown fixture function: {function}")
    data.pop("raw", None)
    return data


def process_culture_body(
    body: Any,
    *,
    input_data: Mapping[str, Any] | None = None,
) -> Page[CultureRecord]:
    """KCISA fixture body를 `Page[CultureRecord]`로 다시 처리합니다."""

    input_data = input_data or {}
    page_no = to_int_or_none(input_data.get("page_no")) or 1
    num_of_rows = to_int_or_none(input_data.get("num_of_rows")) or 10
    payload = _normalize_payload(body, page_no=page_no, num_of_rows=num_of_rows)
    return Page(
        items=tuple(CultureRecord.from_row(row) for row in payload.items),
        page_no=payload.page_no,
        num_of_rows=payload.num_of_rows,
        total_count=payload.total_count,
        raw=payload.raw,
    )


def process_data_go_body(
    body: Any,
    *,
    input_data: Mapping[str, Any] | None = None,
) -> Page[RawRecord]:
    """ODCloud fixture body를 `Page[RawRecord]`로 다시 처리합니다."""

    if not isinstance(body, Mapping):
        raise McstParseError("ODCloud fixture body must be an object")
    input_data = input_data or {}
    page_no = to_int_or_none(input_data.get("page_no")) or 1
    per_page = to_int_or_none(input_data.get("per_page")) or 10
    rows = body.get("data") or body.get("items") or []
    return Page(
        items=_rows_to_tuple(rows, endpoint="fixture"),
        page_no=to_int_or_none(body.get("page")) or page_no,
        num_of_rows=to_int_or_none(body.get("perPage")) or per_page,
        total_count=to_int_or_none(body.get("totalCount")),
        raw=body,
    )
