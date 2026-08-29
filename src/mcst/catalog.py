"""선별된 문화체육관광부 공개 데이터 카탈로그.

이 카탈로그는 한국관광공사 서비스, 행정안전부 자료, 지자체 단독 제공 자료,
도서관 소장자료/서지 데이터셋을 의도적으로 제외합니다.

2026-06-11 재편(#7): MCST culture/도서관 데이터는 CSV 파일 다운로드를 주요
경로로 사용합니다(`CULTURE_FILE_DATASETS`, `LIBRARY_FILE_DATASETS`).
KCISA OpenAPI(`api.kcisa.kr`)는 공인 DNS로 해석되지 않고 KCISA 전용 발급
키가 필요해(#6) `CULTURE_OPEN_APIS`는 명세 참고용으로만 유지합니다.

`update_cycle`은 각 데이터셋 명세서(`spec_url`, culture.go.kr openapiView)
또는 data.go.kr fileData 페이지의 "업데이트 주기"를 2026-06-11에 실측한
값입니다. culture.go.kr 파일 다운로드 페이지(filedatDtl)가 별도로 표기하는
갱신주기는 `notes`에 기록합니다.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from .exceptions import McstRequestError


class SourcePortal(StrEnum):
    CULTURE_GO_KR = "culture.go.kr"
    DATA_GO_KR = "data.go.kr"
    MCST_GO_KR = "mcst.go.kr"


class DatasetKind(StrEnum):
    KCISA_OPEN_API = "kcisa_open_api"
    FILE_DOWNLOAD = "file_download"
    DATA_GO_FILE_API = "data_go_file_api"
    LINK = "link"


@dataclass(frozen=True, slots=True)
class CatalogEntry:
    """선별된 데이터셋 또는 API 항목입니다.

    파일 다운로드 데이터셋(`FILE_DOWNLOAD`)은 `detail_url`이 파일 다운로드
    페이지(culture.go.kr filedatDtl.do 또는 data.go.kr fileData.do)이고,
    `spec_url`이 명세서 페이지입니다. 실제 CSV 링크는 파일명에 업로드
    일시가 박혀 있어 하드코딩할 수 없으므로 다운로드 시점에 `detail_url`
    페이지를 스크레이핑해 얻습니다 (`mcst.file_data`).
    """

    slug: str
    title: str
    provider: str
    kind: DatasetKind
    source: SourcePortal
    detail_url: str
    spec_url: str | None = None
    update_cycle: str | None = None
    endpoint_url: str | None = None
    file_url: str | None = None
    public_data_pk: str | None = None
    public_data_detail_pk: str | None = None
    tags: tuple[str, ...] = ()
    notes: str | None = None


CULTURE_OPEN_APIS: dict[str, CatalogEntry] = {
    "media_famous_places": CatalogEntry(
        slug="media_famous_places",
        title="한국문화정보원_미디어콘텐츠 영상 내 유명지",
        provider="한국문화정보원",
        kind=DatasetKind.KCISA_OPEN_API,
        source=SourcePortal.CULTURE_GO_KR,
        detail_url="https://www.culture.go.kr/data/openapi/openapiView.do?id=583&gubun=A",
        endpoint_url="https://api.kcisa.kr/openapi/API_TOU_048/request",
        tags=("tourism", "filming-location", "poi"),
    ),
    "barrier_free_places": CatalogEntry(
        slug="barrier_free_places",
        title="한국문화정보원_전국 문화예술관광지 배리어프리 정보",
        provider="한국문화정보원",
        kind=DatasetKind.KCISA_OPEN_API,
        source=SourcePortal.CULTURE_GO_KR,
        detail_url="https://www.culture.go.kr/data/openapi/openapiView.do?id=584&gubun=A",
        endpoint_url="https://api.kcisa.kr/openapi/API_TOU_049/request",
        tags=("tourism", "accessibility", "poi"),
    ),
    "pet_friendly_culture_facilities": CatalogEntry(
        slug="pet_friendly_culture_facilities",
        title="한국문화정보원_전국 반려동물 동반가능 문화시설 위치",
        provider="한국문화정보원",
        kind=DatasetKind.KCISA_OPEN_API,
        source=SourcePortal.CULTURE_GO_KR,
        detail_url="https://www.culture.go.kr/data/openapi/openapiView.do?id=585&gubun=A",
        endpoint_url="https://api.kcisa.kr/openapi/API_TOU_050/request",
        tags=("leisure", "pet", "poi"),
    ),
    "leisure_activity_facilities": CatalogEntry(
        slug="leisure_activity_facilities",
        title="한국문화정보원_전국 문화 여가 활동 시설(액티비티)",
        provider="한국문화정보원",
        kind=DatasetKind.KCISA_OPEN_API,
        source=SourcePortal.CULTURE_GO_KR,
        detail_url="https://www.culture.go.kr/data/openapi/openapiView.do?id=587&gubun=A",
        endpoint_url="https://api.kcisa.kr/openapi/API_CIA_082/request",
        tags=("leisure", "activity", "sports", "park", "poi"),
    ),
    "leisure_camping_facilities": CatalogEntry(
        slug="leisure_camping_facilities",
        title="한국문화정보원_전국 문화 여가 활동 시설(캠핑)",
        provider="한국문화정보원",
        kind=DatasetKind.KCISA_OPEN_API,
        source=SourcePortal.CULTURE_GO_KR,
        detail_url="https://www.culture.go.kr/data/openapi/openapiView.do?id=588&gubun=A",
        endpoint_url="https://api.kcisa.kr/openapi/API_CIA_083/request",
        tags=("leisure", "camping", "poi"),
    ),
    "family_infant_culture_facilities": CatalogEntry(
        slug="family_infant_culture_facilities",
        title="한국문화정보원_전국 가족 유아 동반 가능 문화시설",
        provider="한국문화정보원",
        kind=DatasetKind.KCISA_OPEN_API,
        source=SourcePortal.CULTURE_GO_KR,
        detail_url="https://www.culture.go.kr/data/openapi/openapiView.do?id=592&gubun=A",
        endpoint_url="https://api.kcisa.kr/openapi/API_CIA_085/request",
        tags=("family", "infant", "leisure", "poi"),
    ),
    "world_restaurants": CatalogEntry(
        slug="world_restaurants",
        title="한국문화정보원_전국 세계음식점",
        provider="한국문화정보원",
        kind=DatasetKind.KCISA_OPEN_API,
        source=SourcePortal.CULTURE_GO_KR,
        detail_url="https://www.culture.go.kr/data/openapi/openapiView.do?id=594&gubun=A",
        endpoint_url="https://api.kcisa.kr/openapi/API_TOU_052/request",
        tags=("travel", "food", "poi"),
    ),
    "independent_bookstores": CatalogEntry(
        slug="independent_bookstores",
        title="한국문화정보원_전국 독립서점 및 운영정보",
        provider="한국문화정보원",
        kind=DatasetKind.KCISA_OPEN_API,
        source=SourcePortal.CULTURE_GO_KR,
        detail_url="https://www.culture.go.kr/data/openapi/openapiView.do?id=623&gubun=A",
        endpoint_url="https://api.kcisa.kr/openapi/API_CIA_089/request",
        tags=("leisure", "bookstore", "operation", "poi"),
        notes="Library/book-related entry is included only as location/operation leisure data.",
    ),
    "cafe_bookstores": CatalogEntry(
        slug="cafe_bookstores",
        title="한국문화정보원_카페가 있는 서점데이터",
        provider="한국문화정보원",
        kind=DatasetKind.KCISA_OPEN_API,
        source=SourcePortal.CULTURE_GO_KR,
        detail_url="https://www.culture.go.kr/data/openapi/openapiView.do?id=624&gubun=A",
        endpoint_url="https://api.kcisa.kr/openapi/API_CIA_090/request",
        tags=("leisure", "bookstore", "cafe", "operation", "poi"),
        notes="Library/book-related entry is included only as location/operation leisure data.",
    ),
    "used_bookstores": CatalogEntry(
        slug="used_bookstores",
        title="한국문화정보원_전국 중고서점 및 운영정보",
        provider="한국문화정보원",
        kind=DatasetKind.KCISA_OPEN_API,
        source=SourcePortal.CULTURE_GO_KR,
        detail_url="https://www.culture.go.kr/data/openapi/openapiView.do?id=547&gubun=A",
        endpoint_url="https://api.kcisa.kr/API_CNV_045/request",
        update_cycle="연간",
        tags=("leisure", "bookstore", "used", "operation", "poi"),
        notes=(
            "Library/book-related entry is included only as location/operation leisure data. "
            "data.go.kr page reports realtime, culture.go.kr spec reports annual."
        ),
    ),
    "leisure_classes": CatalogEntry(
        slug="leisure_classes",
        title="한국문화정보원_전국 문화 여가 활동 시설(클래스)",
        provider="한국문화정보원",
        kind=DatasetKind.KCISA_OPEN_API,
        source=SourcePortal.CULTURE_GO_KR,
        detail_url="https://www.culture.go.kr/data/openapi/openapiView.do?id=586&gubun=A",
        endpoint_url="https://api.kcisa.kr/openapi/API_CIA_081/request",
        tags=("leisure", "class", "poi"),
    ),
    "recommended_travel_destinations": CatalogEntry(
        slug="recommended_travel_destinations",
        title="문화체육관광부_추천여행지",
        provider="문화체육관광부",
        kind=DatasetKind.KCISA_OPEN_API,
        source=SourcePortal.CULTURE_GO_KR,
        detail_url="https://www.culture.go.kr/data/openapi/openapiView.do?id=581&gubun=A",
        endpoint_url="https://api.kcisa.kr/openapi/API_TOU_046/request",
        tags=("tourism", "recommendation", "poi"),
    ),
}


CULTURE_FILE_DATASETS: dict[str, CatalogEntry] = {
    "recommended_travel_destinations_csv": CatalogEntry(
        slug="recommended_travel_destinations_csv",
        title="문화체육관광부_추천여행지",
        provider="문화체육관광부",
        kind=DatasetKind.FILE_DOWNLOAD,
        source=SourcePortal.CULTURE_GO_KR,
        detail_url=(
            "https://www.culture.go.kr/data/filedat/filedatDtl.do"
            "?fileDataNo=00000000000000000299&category=D&orderBy=dwldCnt"
            "&category=G&dataType=BATCH"
        ),
        spec_url=(
            "https://www.culture.go.kr/data/openapi/openapiView.do"
            "?id=581&category=D&orderBy=rdfCnt&gubun=A"
        ),
        update_cycle="상시",
        tags=("tourism", "recommendation", "poi", "csv"),
        notes="파일 페이지 갱신주기: 월간",
    ),
    "independent_bookstores_csv": CatalogEntry(
        slug="independent_bookstores_csv",
        title="한국문화정보원_전국 독립서점 및 운영정보",
        provider="한국문화정보원",
        kind=DatasetKind.FILE_DOWNLOAD,
        source=SourcePortal.CULTURE_GO_KR,
        detail_url=(
            "https://www.culture.go.kr/data/filedat/filedatDtl.do"
            "?fileDataNo=00000000000000000443&category=C&orderBy=dwldCnt"
            "&category=H&dataType=BATCH"
        ),
        spec_url=(
            "https://www.culture.go.kr/data/openapi/openapiView.do"
            "?id=623&keyword=%EB%8F%85%EB%A6%BD%EC%84%9C%EC%A0%90&searchField=all&gubun=A"
        ),
        update_cycle="상시",
        tags=("leisure", "bookstore", "operation", "poi", "csv"),
        notes=(
            "파일 페이지 갱신주기: 월간. "
            "Library/book-related entry is included only as location/operation leisure data."
        ),
    ),
    "media_famous_places_csv": CatalogEntry(
        slug="media_famous_places_csv",
        title="한국문화정보원_미디어콘텐츠 영상 내 유명지",
        provider="한국문화정보원",
        kind=DatasetKind.FILE_DOWNLOAD,
        source=SourcePortal.CULTURE_GO_KR,
        detail_url=(
            "https://www.culture.go.kr/data/filedat/filedatDtl.do"
            "?fileDataNo=00000000000000000412&category=D&orderBy=dwldCnt"
            "&category=H&dataType=BATCH"
        ),
        spec_url=(
            "https://www.culture.go.kr/data/openapi/openapiView.do"
            "?id=583&category=D&orderBy=rdfCnt&gubun=A"
        ),
        update_cycle="상시",
        tags=("tourism", "filming-location", "poi", "csv"),
        notes="파일 페이지 갱신주기: 월간",
    ),
    "tourism_attractions_csv": CatalogEntry(
        slug="tourism_attractions_csv",
        title="한국문화관광연구원 외_관광지정보",
        provider="한국문화관광연구원 외",
        kind=DatasetKind.FILE_DOWNLOAD,
        source=SourcePortal.CULTURE_GO_KR,
        detail_url=(
            "https://www.culture.go.kr/data/filedat/filedatDtl.do"
            "?fileDataNo=00000000000000000275"
            "&keyword=%EA%B4%80%EA%B4%91%EC%A7%80%EC%A0%95%EB%B3%B4&category=C&dataType=BATCH"
        ),
        spec_url=(
            "https://www.culture.go.kr/data/openapi/openapiView.do"
            "?id=319&category=D&orderBy=rdfCnt&gubun=A"
        ),
        update_cycle="연간",
        tags=("tourism", "poi", "csv"),
        notes="파일 페이지 갱신주기: 월간",
    ),
    "world_restaurants_csv": CatalogEntry(
        slug="world_restaurants_csv",
        title="한국문화정보원_전국 세계음식점",
        provider="한국문화정보원",
        kind=DatasetKind.FILE_DOWNLOAD,
        source=SourcePortal.CULTURE_GO_KR,
        detail_url=(
            "https://www.culture.go.kr/data/filedat/filedatDtl.do"
            "?fileDataNo=00000000000000000416&category=D&orderBy=dwldCnt"
            "&category=H&dataType=BATCH"
        ),
        spec_url=(
            "https://www.culture.go.kr/data/openapi/openapiView.do"
            "?id=594&keyword=%EC%84%B8%EA%B3%84%EC%9D%8C%EC%8B%9D%EC%A0%90&searchField=all&gubun=A"
        ),
        update_cycle="연간",
        tags=("travel", "food", "poi", "csv"),
        notes="파일 페이지 갱신주기: 연간",
    ),
    "pet_friendly_culture_facilities_csv": CatalogEntry(
        slug="pet_friendly_culture_facilities_csv",
        title="한국문화정보원_전국 반려동물 동반가능 문화시설 위치",
        provider="한국문화정보원",
        kind=DatasetKind.FILE_DOWNLOAD,
        source=SourcePortal.CULTURE_GO_KR,
        detail_url=(
            "https://www.culture.go.kr/data/filedat/filedatDtl.do"
            "?fileDataNo=00000000000000000414&category=D&orderBy=dwldCnt"
            "&category=H&dataType=BATCH"
        ),
        spec_url=(
            "https://www.culture.go.kr/data/openapi/openapiView.do"
            "?id=585&keyword=%EB%B0%98%EB%A0%A4%EB%8F%99%EB%AC%BC&searchField=all&gubun=A"
        ),
        update_cycle="상시",
        tags=("leisure", "pet", "poi", "csv"),
        notes="파일 페이지 갱신주기: 월간",
    ),
    "barrier_free_places_csv": CatalogEntry(
        slug="barrier_free_places_csv",
        title="한국문화정보원_전국 문화예술관광지 배리어프리 정보",
        provider="한국문화정보원",
        kind=DatasetKind.FILE_DOWNLOAD,
        source=SourcePortal.CULTURE_GO_KR,
        detail_url=(
            "https://www.culture.go.kr/data/filedat/filedatDtl.do"
            "?fileDataNo=00000000000000000413&category=D&orderBy=dwldCnt"
            "&category=H&dataType=BATCH"
        ),
        spec_url=(
            "https://www.culture.go.kr/data/openapi/openapiView.do"
            "?id=584&keyword=%EB%B0%B0%EB%A6%AC%EC%96%B4%ED%94%84%EB%A6%AC&searchField=all&gubun=A"
        ),
        update_cycle="상시",
        tags=("tourism", "accessibility", "poi", "csv"),
        notes="파일 페이지 갱신주기: 월간",
    ),
    "cafe_bookstores_csv": CatalogEntry(
        slug="cafe_bookstores_csv",
        title="한국문화정보원_카페가 있는 서점데이터",
        provider="한국문화정보원",
        kind=DatasetKind.FILE_DOWNLOAD,
        source=SourcePortal.CULTURE_GO_KR,
        detail_url=(
            "https://www.culture.go.kr/data/filedat/filedatDtl.do"
            "?fileDataNo=00000000000000000444&category=C&orderBy=dwldCnt"
            "&category=H&dataType=BATCH"
        ),
        spec_url=(
            "https://www.culture.go.kr/data/openapi/openapiView.do"
            "?id=624&keyword=%EC%B9%B4%ED%8E%98&searchField=all&gubun=A"
        ),
        update_cycle="상시",
        tags=("leisure", "bookstore", "cafe", "operation", "poi", "csv"),
        notes=(
            "파일 페이지 갱신주기: 월간. "
            "Library/book-related entry is included only as location/operation leisure data."
        ),
    ),
    "leisure_activity_facilities_csv": CatalogEntry(
        slug="leisure_activity_facilities_csv",
        title="한국문화정보원_전국 문화 여가 활동 시설(액티비티)",
        provider="한국문화정보원",
        kind=DatasetKind.FILE_DOWNLOAD,
        source=SourcePortal.CULTURE_GO_KR,
        detail_url=(
            "https://www.culture.go.kr/data/filedat/filedatDtl.do"
            "?fileDataNo=00000000000000000243&category=C&orderBy=dwldCnt"
            "&category=H&dataType=BATCH"
        ),
        spec_url=(
            "https://www.culture.go.kr/data/openapi/openapiView.do"
            "?id=587&keyword=%EC%95%A1%ED%8B%B0%EB%B9%84%ED%8B%B0&searchField=all&gubun=A"
        ),
        update_cycle="상시",
        tags=("leisure", "activity", "sports", "park", "poi", "csv"),
        notes="파일 페이지 갱신주기: 월간",
    ),
    "leisure_classes_csv": CatalogEntry(
        slug="leisure_classes_csv",
        title="한국문화정보원_전국 문화 여가 활동 시설(클래스)",
        provider="한국문화정보원",
        kind=DatasetKind.FILE_DOWNLOAD,
        source=SourcePortal.CULTURE_GO_KR,
        detail_url=(
            "https://www.culture.go.kr/data/filedat/filedatDtl.do"
            "?fileDataNo=00000000000000000242&category=C&orderBy=dwldCnt"
            "&category=H&dataType=BATCH"
        ),
        spec_url=(
            "https://www.culture.go.kr/data/openapi/openapiView.do"
            "?id=586&keyword=%ED%81%B4%EB%9E%98%EC%8A%A4&searchField=all&gubun=A"
        ),
        update_cycle="상시",
        tags=("leisure", "class", "poi", "csv"),
        notes="파일 페이지 갱신주기: 월간",
    ),
    "family_infant_culture_facilities_csv": CatalogEntry(
        slug="family_infant_culture_facilities_csv",
        title="한국문화정보원_전국 가족 유아 동반 가능 문화시설",
        provider="한국문화정보원",
        kind=DatasetKind.FILE_DOWNLOAD,
        source=SourcePortal.CULTURE_GO_KR,
        detail_url=(
            "https://www.culture.go.kr/data/filedat/filedatDtl.do"
            "?fileDataNo=00000000000000000246&category=C&orderBy=dwldCnt"
            "&category=H&dataType=BATCH"
        ),
        spec_url=(
            "https://www.culture.go.kr/data/openapi/openapiView.do"
            "?id=592&keyword=%EC%9C%A0%EC%95%84&searchField=all&gubun=A"
        ),
        update_cycle="연간",
        tags=("family", "infant", "leisure", "poi", "csv"),
        notes="파일 페이지 갱신주기: 월간",
    ),
    "children_bookstores_csv": CatalogEntry(
        slug="children_bookstores_csv",
        title="한국문화정보원_전국 아동서점 운영정보",
        provider="한국문화정보원",
        kind=DatasetKind.FILE_DOWNLOAD,
        source=SourcePortal.CULTURE_GO_KR,
        detail_url=(
            "https://www.culture.go.kr/data/filedat/filedatDtl.do"
            "?fileDataNo=00000000000000000282&category=C&orderBy=dwldCnt"
            "&category=H&dataType=BATCH"
        ),
        spec_url=(
            "https://www.culture.go.kr/data/openapi/openapiView.do"
            "?id=537&keyword=%EC%95%84%EB%8F%99%EC%84%9C%EC%A0%90&searchField=all&gubun=A"
        ),
        update_cycle="연간",
        tags=("leisure", "bookstore", "operation", "poi", "csv"),
        notes=(
            "파일 페이지 갱신주기: 월간. "
            "Library/book-related entry is included only as location/operation leisure data."
        ),
    ),
    "used_bookstores_csv": CatalogEntry(
        slug="used_bookstores_csv",
        title="한국문화정보원_전국 중고서점 및 운영정보",
        provider="한국문화정보원",
        kind=DatasetKind.FILE_DOWNLOAD,
        source=SourcePortal.CULTURE_GO_KR,
        detail_url=(
            "https://www.culture.go.kr/data/filedat/filedatDtl.do"
            "?fileDataNo=00000000000000000286&category=B&category=H&dataType=BATCH"
        ),
        spec_url="https://www.culture.go.kr/data/openapi/openapiView.do?id=547&gubun=A",
        update_cycle="연간",
        tags=("leisure", "bookstore", "used", "operation", "poi", "csv"),
        notes=(
            "파일 페이지 갱신주기: 연간. "
            "Library/book-related entry is included only as location/operation leisure data."
        ),
    ),
    "leisure_camping_facilities_csv": CatalogEntry(
        slug="leisure_camping_facilities_csv",
        title="한국문화정보원_전국 문화 여가 활동 시설(캠핑)",
        provider="한국문화정보원",
        kind=DatasetKind.FILE_DOWNLOAD,
        source=SourcePortal.CULTURE_GO_KR,
        detail_url=(
            "https://www.culture.go.kr/data/filedat/filedatDtl.do"
            "?fileDataNo=00000000000000000244&category=C&orderBy=dwldCnt"
            "&category=H&dataType=BATCH"
        ),
        spec_url=(
            "https://www.culture.go.kr/data/openapi/openapiView.do"
            "?id=588&keyword=%EC%97%AC%EA%B0%80&searchField=all&gubun=A"
        ),
        update_cycle="상시",
        tags=("leisure", "camping", "poi", "csv"),
        notes="파일 페이지 갱신주기: 월간",
    ),
    "golf_courses_status": CatalogEntry(
        slug="golf_courses_status",
        title="문화체육관광부_전국 골프장 현황",
        provider="문화체육관광부",
        kind=DatasetKind.FILE_DOWNLOAD,
        source=SourcePortal.DATA_GO_KR,
        detail_url="https://www.data.go.kr/data/15118920/fileData.do",
        update_cycle="수시 (1회성 데이터)",
        public_data_pk="15118920",
        public_data_detail_pk="uddi:0e5b12d2-1cc8-4caf-ba96-c2c7d1ef8d83",
        tags=("leisure", "golf", "csv"),
        notes="명세서 페이지 없음 — data.go.kr fileData 페이지의 업데이트 주기 실측값.",
    ),
}


LIBRARY_FILE_DATASETS: dict[str, CatalogEntry] = {
    "public_libraries": CatalogEntry(
        slug="public_libraries",
        title="문화체육관광부_국가도서관통계_전국공공도서관정보",
        provider="문화체육관광부",
        kind=DatasetKind.FILE_DOWNLOAD,
        source=SourcePortal.DATA_GO_KR,
        detail_url="https://www.data.go.kr/data/15072611/fileData.do",
        update_cycle="연간",
        public_data_pk="15072611",
        public_data_detail_pk="uddi:4e0d4d95-76e2-4a03-9886-ba11052ac3fb",
        tags=("library", "location", "operation", "csv"),
        notes="Included as library location/operation data only; holdings are excluded.",
    ),
}


FILE_DATASETS: dict[str, CatalogEntry] = {
    "tourism_lodging_status": CatalogEntry(
        slug="tourism_lodging_status",
        title="문화체육관광부_전국 관광숙박시설 현황",
        provider="문화체육관광부",
        kind=DatasetKind.DATA_GO_FILE_API,
        source=SourcePortal.DATA_GO_KR,
        detail_url="https://www.data.go.kr/data/3075666/fileData.do",
        file_url="https://www.data.go.kr/cmm/cmm/fileDownload.do?atchFileId=FILE_000000003618700&fileDetailSn=1&insertDataPrcus=N",
        public_data_pk="3075666",
        public_data_detail_pk="uddi:4c5f84ce-4541-4542-9da4-9a2f236b4a12",
        tags=("lodging", "tourism", "csv", "odcloud"),
    ),
    "hotels_status": CatalogEntry(
        slug="hotels_status",
        title="문화체육관광부_전국호텔현황",
        provider="문화체육관광부",
        kind=DatasetKind.DATA_GO_FILE_API,
        source=SourcePortal.DATA_GO_KR,
        detail_url="https://www.data.go.kr/data/15118900/fileData.do",
        file_url="https://www.data.go.kr/cmm/cmm/fileDownload.do?atchFileId=FILE_000000002995528&fileDetailSn=1&insertDataPrcus=N",
        public_data_pk="15118900",
        public_data_detail_pk="uddi:b8fa9309-7c1f-415e-b706-9e189e4a056a",
        tags=("lodging", "hotel", "csv", "odcloud"),
    ),
    "public_sports_facilities": CatalogEntry(
        slug="public_sports_facilities",
        title="문화체육관광부_전국공공체육시설 현황",
        provider="문화체육관광부",
        kind=DatasetKind.DATA_GO_FILE_API,
        source=SourcePortal.DATA_GO_KR,
        detail_url="https://www.data.go.kr/data/15119078/fileData.do",
        file_url="https://www.data.go.kr/cmm/cmm/fileDownload.do?atchFileId=FILE_000000002791123&fileDetailSn=1&insertDataPrcus=N",
        public_data_pk="15119078",
        public_data_detail_pk="uddi:893b5a28-fb02-4a0b-b2ec-b76a803d3259",
        tags=("leisure", "sports", "csv", "odcloud"),
    ),
    "registered_sports_businesses": CatalogEntry(
        slug="registered_sports_businesses",
        title="문화체육관광부_전국 등록신고 체육시설업 현황",
        provider="문화체육관광부",
        kind=DatasetKind.DATA_GO_FILE_API,
        source=SourcePortal.DATA_GO_KR,
        detail_url="https://www.data.go.kr/data/15123280/fileData.do",
        file_url="https://www.data.go.kr/cmm/cmm/fileDownload.do?atchFileId=FILE_000000003510874&fileDetailSn=1&insertDataPrcus=N",
        public_data_pk="15123280",
        public_data_detail_pk="uddi:d0b409c4-01b8-467a-8963-b65a02a1e50b",
        tags=("leisure", "sports", "csv", "odcloud"),
    ),
    "marathon_events": CatalogEntry(
        slug="marathon_events",
        title="문화체육관광부_국내마라톤대회 정보",
        provider="문화체육관광부",
        kind=DatasetKind.DATA_GO_FILE_API,
        source=SourcePortal.DATA_GO_KR,
        detail_url="https://www.data.go.kr/data/15138980/fileData.do",
        file_url="https://www.data.go.kr/cmm/cmm/fileDownload.do?atchFileId=FILE_000000003607547&fileDetailSn=1&insertDataPrcus=N",
        public_data_pk="15138980",
        public_data_detail_pk="uddi:eedc77c5-a56b-4e77-9c1d-9396fa9cc1d3",
        tags=("leisure", "sports", "event", "csv", "odcloud"),
    ),
}


LINK_DATASETS: dict[str, CatalogEntry] = {
    "tourism_complexes": CatalogEntry(
        slug="tourism_complexes",
        title="문화체육관광부_관광지 관광단지 현황",
        provider="문화체육관광부",
        kind=DatasetKind.LINK,
        source=SourcePortal.DATA_GO_KR,
        detail_url="https://www.data.go.kr/data/3075662/fileData.do",
        file_url="https://www.mcst.go.kr/site/s_policy/dept/deptView.jsp?pCurrentPage=1&pType=05&pTab=01&pSeq=2038&pDataCD=0417000000&pSearchType=01&pSearchWord=%EA%B4%80%EA%B4%91%EC%A7%80+%EB%B0%8F+%EA%B4%80%EA%B4%91%EB%8B%A8%EC%A7%80",
        public_data_pk="3075662",
        public_data_detail_pk="uddi:3f3ef943-bdc2-4518-91f5-aa99f2593aaa",
        tags=("tourism", "poi", "link"),
    ),
    "tourism_special_zones": CatalogEntry(
        slug="tourism_special_zones",
        title="문화체육관광부_관광특구 현황",
        provider="문화체육관광부",
        kind=DatasetKind.LINK,
        source=SourcePortal.DATA_GO_KR,
        detail_url="https://www.data.go.kr/data/3075663/fileData.do",
        file_url="https://www.mcst.go.kr/kor/s_policy/dept/deptView.jsp?pCurrentPage=1&pType=05&pTab=01&pSeq=2032&pDataCD=0417000000&pSearchType=01&pSearchWord=%EA%B4%80%EA%B4%91%ED%8A%B9%EA%B5%AC",
        public_data_pk="3075663",
        public_data_detail_pk="uddi:2ed57b03-bcf1-4c9f-9d85-c617a941d439",
        tags=("tourism", "zone", "link"),
    ),
    "recommended_travel_places": CatalogEntry(
        slug="recommended_travel_places",
        title="문화체육관광부_추천관광지",
        provider="문화체육관광부",
        kind=DatasetKind.LINK,
        source=SourcePortal.DATA_GO_KR,
        detail_url="https://www.data.go.kr/data/3070143/fileData.do",
        file_url="https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000299&keyword=%EC%B6%94%EC%B2%9C%EC%97%AC%ED%96%89%EC%A7%80&dataType=BATCH",
        public_data_pk="3070143",
        public_data_detail_pk="uddi:042ae9dc-e8ed-4a70-af62-ec2ab8143475_201911151335",
        tags=("tourism", "recommendation", "link"),
    ),
    "traditional_temples": CatalogEntry(
        slug="traditional_temples",
        title="문화체육관광부_전통사찰 현황",
        provider="문화체육관광부",
        kind=DatasetKind.LINK,
        source=SourcePortal.DATA_GO_KR,
        detail_url="https://www.data.go.kr/data/3075623/fileData.do",
        file_url="https://www.mcst.go.kr/kor/s_policy/dept/deptView.jsp?pCurrentPage=1&pType=03&pTab=01&pSeq=1572&pDataCD=0417000000&pSearchType=01&pSearchWord=%EC%A0%84%ED%86%B5%EC%82%AC%EC%B0%B0+%ED%98%84%ED%99%A9",
        public_data_pk="3075623",
        public_data_detail_pk="uddi:c2ea0836-8f99-418b-9630-c936e018d672",
        tags=("tourism", "temple", "heritage", "link"),
    ),
    "culture_infrastructure_status": CatalogEntry(
        slug="culture_infrastructure_status",
        title="문화체육관광부 전국문화기반시설 현황",
        provider="문화체육관광부",
        kind=DatasetKind.LINK,
        source=SourcePortal.DATA_GO_KR,
        detail_url="https://www.data.go.kr/data/3075558/fileData.do",
        file_url="https://www.mcst.go.kr/site/s_policy/dept/deptView.jsp?pCurrentPage=1&pType=02&pTab=01&pSeq=2078&pDataCD=0417000000&pSearchType=01&pSearchWord=",
        public_data_pk="3075558",
        public_data_detail_pk="uddi:d0063c10-09c8-46a5-b89a-db41e73e513e",
        tags=("culture-facility", "library", "museum", "location", "operation", "link"),
    ),
    "registered_performance_halls": CatalogEntry(
        slug="registered_performance_halls",
        title="문화체육관광부_전국 등록공연장 현황",
        provider="문화체육관광부",
        kind=DatasetKind.LINK,
        source=SourcePortal.DATA_GO_KR,
        detail_url="https://www.data.go.kr/data/3075660/fileData.do",
        file_url="https://www.mcst.go.kr/kor/s_policy/dept/deptView.jsp?pCurrentPage=1&pType=02&pTab=01&pSeq=1403&pDataCD=0417000000&pSearchType=01&pSearchWord=",
        public_data_pk="3075660",
        public_data_detail_pk="uddi:c7fc3f60-8a2f-48e7-89d6-cd996151934a",
        tags=("leisure", "performance", "link"),
    ),
}


ALL_DATASETS: dict[str, CatalogEntry] = {
    **CULTURE_OPEN_APIS,
    **CULTURE_FILE_DATASETS,
    **LIBRARY_FILE_DATASETS,
    **FILE_DATASETS,
    **LINK_DATASETS,
}


def catalog_entry_to_dict(entry: CatalogEntry) -> dict[str, Any]:
    """카탈로그 항목을 UI와 JSON 응답에서 쓰기 쉬운 dict로 변환합니다."""

    return {
        "slug": entry.slug,
        "label": dataset_label(entry),
        "title": entry.title,
        "provider": entry.provider,
        "kind": entry.kind.value,
        "source": entry.source.value,
        "detail_url": entry.detail_url,
        "spec_url": entry.spec_url,
        "update_cycle": entry.update_cycle,
        "endpoint_url": entry.endpoint_url,
        "file_url": entry.file_url,
        "public_data_pk": entry.public_data_pk,
        "public_data_detail_pk": entry.public_data_detail_pk,
        "tags": list(entry.tags),
        "notes": entry.notes,
    }


def dataset_label(entry: CatalogEntry | Mapping[str, Any]) -> str:
    """사람이 알아보기 쉬운 데이터셋 표시명을 반환합니다."""

    if isinstance(entry, CatalogEntry):
        title = entry.title
        slug = entry.slug
    else:
        title = str(entry.get("title") or "")
        slug = str(entry.get("slug") or "")
    return f"{title} ({slug})" if slug else title


def iter_api_catalog(
    *,
    kind: DatasetKind | str | None = None,
    include_links: bool = False,
) -> tuple[CatalogEntry, ...]:
    """선별된 API/파일 데이터 카탈로그 항목을 반환합니다.

    기본값은 실제 호출 또는 다운로드 대상이 없는 링크 전용 항목을 제외합니다.
    """

    kind_value = DatasetKind(kind) if kind is not None else None
    entries: Iterable[CatalogEntry] = ALL_DATASETS.values()
    if kind_value is not None:
        entries = [entry for entry in entries if entry.kind == kind_value]
    elif not include_links:
        entries = [entry for entry in entries if entry.kind != DatasetKind.LINK]
    return tuple(sorted(entries, key=lambda entry: (entry.kind.value, entry.title, entry.slug)))


def get_api_catalog(
    *,
    kind: DatasetKind | str | None = None,
    include_links: bool = False,
) -> tuple[dict[str, Any], ...]:
    """API 카탈로그를 JSON 직렬화 가능한 dict 목록으로 반환합니다."""

    return tuple(
        catalog_entry_to_dict(entry)
        for entry in iter_api_catalog(kind=kind, include_links=include_links)
    )


def get_dataset(slug: str) -> CatalogEntry:
    """slug로 카탈로그 항목을 반환합니다."""

    try:
        return ALL_DATASETS[slug]
    except KeyError as exc:
        known = ", ".join(sorted(ALL_DATASETS))
        raise McstRequestError(f"unknown dataset slug {slug!r}; known slugs: {known}") from exc
