"""공개 응답 모델입니다."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

from ._convert import first_value, to_float_or_none

T = TypeVar("T")
RawRecord = dict[str, Any]


class Page(BaseModel, Generic[T]):
    """정규화된 페이지 응답입니다."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    items: tuple[T, ...]
    page_no: int = 1
    num_of_rows: int = 0
    total_count: int | None = None
    raw: Any | None = None
    endpoint: str | None = None


class CultureRecord(BaseModel):
    """culture.go.kr/KCISA 레코드의 공통 필드를 가능한 범위에서 정리한 모델입니다.

    문화 데이터셋은 단일 스키마를 공유하지 않습니다. 추론 가능한 공통 필드는
    별도 속성으로 노출하고, 원본 행은 항상 `raw`에 보존합니다.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str | None = None
    address: str | None = None
    tel: str | None = None
    url: str | None = None
    longitude: float | None = None
    latitude: float | None = None
    category: str | None = None
    raw: RawRecord = Field(default_factory=dict)

    @classmethod
    def from_row(cls, row: Mapping[str, Any]) -> CultureRecord:
        return cls(
            name=_text(
                row,
                "title",
                "TITLE",
                "name",
                "NAME",
                "facName",
                "fcltyNm",
                "facilityName",
                "contentsName",
                "문화시설명",
                "시설명",
                "장소명",
                "서점명",
                "업소명",
                "콘텐츠명",
            ),
            address=_text(
                row,
                "address",
                "addr",
                "ADDR",
                "roadAddress",
                "jibunAddress",
                "주소",
                "도로명주소",
                "소재지",
            ),
            tel=_text(row, "tel", "TEL", "phone", "phoneNumber", "전화번호", "연락처"),
            url=_text(row, "url", "URL", "homepage", "홈페이지", "관련URL"),
            longitude=to_float_or_none(
                first_value(row, "longitude", "lon", "lng", "mapx", "x", "경도")
            ),
            latitude=to_float_or_none(
                first_value(row, "latitude", "lat", "mapy", "y", "위도")
            ),
            category=_text(row, "category", "type", "분류", "구분", "장르"),
            raw=dict(row),
        )


def _text(row: Mapping[str, Any], *names: str) -> str | None:
    value = first_value(row, *names)
    if value is None:
        return None
    text = str(value).strip()
    return text or None
