"""선별된 문화체육관광부 공개 데이터 카탈로그.

이 카탈로그는 한국관광공사 서비스, 행정안전부 자료, 지자체 단독 제공 자료,
도서관 소장자료/서지 데이터셋을 의도적으로 제외합니다.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from enum import StrEnum
from typing import Any


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
    """선별된 데이터셋 또는 API 항목입니다."""

    slug: str
    title: str
    provider: str
    kind: DatasetKind
    source: SourcePortal
    detail_url: str
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
    "multilingual_guide_culture_facilities": CatalogEntry(
        slug="multilingual_guide_culture_facilities",
        title="한국문화정보원_전국 다국어 가이드 제공 문화시설",
        provider="한국문화정보원",
        kind=DatasetKind.KCISA_OPEN_API,
        source=SourcePortal.CULTURE_GO_KR,
        detail_url="https://www.culture.go.kr/data/openapi/openapiView.do?id=593&gubun=A",
        endpoint_url="https://api.kcisa.kr/openapi/API_TOU_051/request",
        tags=("tourism", "guide", "culture-facility", "poi"),
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
    "small_theaters": CatalogEntry(
        slug="small_theaters",
        title="한국문화정보원_전국 연극장 및 소극장 정보",
        provider="한국문화정보원",
        kind=DatasetKind.KCISA_OPEN_API,
        source=SourcePortal.CULTURE_GO_KR,
        detail_url="https://www.culture.go.kr/data/openapi/openapiView.do?id=595&gubun=A",
        endpoint_url="https://api.kcisa.kr/openapi/API_TOU_053/request",
        tags=("leisure", "performance", "theater", "poi"),
    ),
    "meeting_seminar_facilities": CatalogEntry(
        slug="meeting_seminar_facilities",
        title="한국문화정보원_전국 회의 세미나 시설정보",
        provider="한국문화정보원",
        kind=DatasetKind.KCISA_OPEN_API,
        source=SourcePortal.CULTURE_GO_KR,
        detail_url="https://www.culture.go.kr/data/openapi/openapiView.do?id=596&gubun=A",
        endpoint_url="https://api.kcisa.kr/openapi/API_CIA_086/request",
        tags=("leisure", "meeting", "facility", "poi"),
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
}


FILE_DATASETS: dict[str, CatalogEntry] = {
    "family_infant_culture_facilities_csv": CatalogEntry(
        slug="family_infant_culture_facilities_csv",
        title="한국문화정보원_전국 가족 유아 동반 가능 문화시설",
        provider="한국문화정보원",
        kind=DatasetKind.FILE_DOWNLOAD,
        source=SourcePortal.CULTURE_GO_KR,
        detail_url="https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000246&category=C&orderBy=dwldCnt&category=H&dataType=BATCH",
        file_url="https://big.kcisa.kr/common/bbsAtchFileDownload.do?downFileName=API_CIA_085_20260508183949.csv&downFilePath=apiExcelData&orginFileName=%ED%95%9C%EA%B5%AD%EB%AC%B8%ED%99%94%EC%A0%95%EB%B3%B4%EC%9B%90_%EC%A0%84%EA%B5%AD%20%EA%B0%80%EC%A1%B1%20%EC%9C%A0%EC%95%84%20%EB%8F%99%EB%B0%98%20%EA%B0%80%EB%8A%A5%20%EB%AC%B8%ED%99%94%EC%8B%9C%EC%84%A4(20260508).csv&dataType=BATCH&fileDatNo=00000000000000000246",
        tags=("family", "infant", "leisure", "csv"),
    ),
    "independent_bookstores_csv": CatalogEntry(
        slug="independent_bookstores_csv",
        title="한국문화정보원_전국 독립서점 및 운영정보",
        provider="한국문화정보원",
        kind=DatasetKind.FILE_DOWNLOAD,
        source=SourcePortal.CULTURE_GO_KR,
        detail_url="https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000443&category=C&orderBy=dwldCnt&category=H&dataType=BATCH",
        file_url="https://big.kcisa.kr/common/bbsAtchFileDownload.do?downFileName=API_CIA_089_20260421182016.csv&downFilePath=apiExcelData&orginFileName=%ED%95%9C%EA%B5%AD%EB%AC%B8%ED%99%94%EC%A0%95%EB%B3%B4%EC%9B%90_%EC%A0%84%EA%B5%AD%20%EB%8F%85%EB%A6%BD%EC%84%9C%EC%A0%90%20%EB%B0%8F%20%EC%9A%B4%EC%98%81%EC%A0%95%EB%B3%B4(20260421).csv&dataType=BATCH&fileDatNo=00000000000000000443",
        tags=("leisure", "bookstore", "csv"),
    ),
    "cafe_bookstores_csv": CatalogEntry(
        slug="cafe_bookstores_csv",
        title="한국문화정보원_카페가 있는 서점데이터",
        provider="한국문화정보원",
        kind=DatasetKind.FILE_DOWNLOAD,
        source=SourcePortal.CULTURE_GO_KR,
        detail_url="https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000444&category=C&orderBy=dwldCnt&category=H&dataType=BATCH",
        file_url="https://big.kcisa.kr/common/bbsAtchFileDownload.do?downFileName=API_CIA_090_20260421182016.csv&downFilePath=apiExcelData&orginFileName=%ED%95%9C%EA%B5%AD%EB%AC%B8%ED%99%94%EC%A0%95%EB%B3%B4%EC%9B%90_%EC%B9%B4%ED%8E%98%EA%B0%80%20%EC%9E%88%EB%8A%94%20%EC%84%9C%EC%A0%90%EB%8D%B0%EC%9D%B4%ED%84%B0(20260421).csv&dataType=BATCH&fileDatNo=00000000000000000444",
        tags=("leisure", "bookstore", "cafe", "csv"),
    ),
    "leisure_activity_facilities_csv": CatalogEntry(
        slug="leisure_activity_facilities_csv",
        title="한국문화정보원_전국 문화 여가 활동 시설(액티비티) 데이터",
        provider="한국문화정보원",
        kind=DatasetKind.DATA_GO_FILE_API,
        source=SourcePortal.DATA_GO_KR,
        detail_url="https://www.data.go.kr/data/15111393/fileData.do",
        file_url="https://www.data.go.kr/cmm/cmm/fileDownload.do?atchFileId=FILE_000000003000511&fileDetailSn=1&insertDataPrcus=N",
        public_data_pk="15111393",
        public_data_detail_pk="uddi:703ed001-91d0-453c-b0d0-ee3c517fdecd",
        tags=("leisure", "activity", "csv", "odcloud"),
    ),
    "leisure_camping_facilities_csv": CatalogEntry(
        slug="leisure_camping_facilities_csv",
        title="한국문화정보원_전국 문화 여가 활동 시설(캠핑) 데이터",
        provider="한국문화정보원",
        kind=DatasetKind.DATA_GO_FILE_API,
        source=SourcePortal.DATA_GO_KR,
        detail_url="https://www.data.go.kr/data/15111395/fileData.do",
        file_url="https://www.data.go.kr/cmm/cmm/fileDownload.do?atchFileId=FILE_000000003000448&fileDetailSn=1&insertDataPrcus=N",
        public_data_pk="15111395",
        public_data_detail_pk="uddi:8c528230-eda4-4d83-855a-bee73605e49f",
        tags=("leisure", "camping", "csv", "odcloud"),
    ),
    "leisure_classes_csv": CatalogEntry(
        slug="leisure_classes_csv",
        title="한국문화정보원_전국 문화 여가 활동 시설(클래스) 데이터",
        provider="한국문화정보원",
        kind=DatasetKind.DATA_GO_FILE_API,
        source=SourcePortal.DATA_GO_KR,
        detail_url="https://www.data.go.kr/data/15111397/fileData.do",
        file_url="https://www.data.go.kr/cmm/cmm/fileDownload.do?atchFileId=FILE_000000002680050&fileDetailSn=1&insertDataPrcus=N",
        public_data_pk="15111397",
        public_data_detail_pk="uddi:b2a81057-13be-4bdb-a368-b753c19d3d61",
        tags=("leisure", "class", "csv", "odcloud"),
    ),
    "world_restaurants_csv": CatalogEntry(
        slug="world_restaurants_csv",
        title="한국문화정보원_전국 세계 음식점 데이터",
        provider="한국문화정보원",
        kind=DatasetKind.DATA_GO_FILE_API,
        source=SourcePortal.DATA_GO_KR,
        detail_url="https://www.data.go.kr/data/15111398/fileData.do",
        file_url="https://www.data.go.kr/cmm/cmm/fileDownload.do?atchFileId=FILE_000000003000428&fileDetailSn=1&insertDataPrcus=N",
        public_data_pk="15111398",
        public_data_detail_pk="uddi:65f027c0-2c92-411b-b9f5-cb7382fde662",
        tags=("travel", "food", "csv", "odcloud"),
    ),
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
    "golf_courses_status": CatalogEntry(
        slug="golf_courses_status",
        title="문화체육관광부_전국 골프장 현황",
        provider="문화체육관광부",
        kind=DatasetKind.DATA_GO_FILE_API,
        source=SourcePortal.DATA_GO_KR,
        detail_url="https://www.data.go.kr/data/15118920/fileData.do",
        file_url="https://www.data.go.kr/cmm/cmm/fileDownload.do?atchFileId=FILE_000000002791834&fileDetailSn=1&insertDataPrcus=N",
        public_data_pk="15118920",
        public_data_detail_pk="uddi:0e5b12d2-1cc8-4caf-ba96-c2c7d1ef8d83",
        tags=("leisure", "golf", "csv", "odcloud"),
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
    "public_libraries": CatalogEntry(
        slug="public_libraries",
        title="문화체육관광부_국가도서관통계_전국공공도서관정보",
        provider="문화체육관광부",
        kind=DatasetKind.DATA_GO_FILE_API,
        source=SourcePortal.DATA_GO_KR,
        detail_url="https://www.data.go.kr/data/15072611/fileData.do",
        file_url="https://www.data.go.kr/cmm/cmm/fileDownload.do?atchFileId=FILE_000000003516836&fileDetailSn=1&insertDataPrcus=N",
        public_data_pk="15072611",
        public_data_detail_pk="uddi:4e0d4d95-76e2-4a03-9886-ba11052ac3fb",
        tags=("library", "location", "operation", "csv", "odcloud"),
        notes="Included as library location/operation data only; holdings are excluded.",
    ),
    "small_libraries": CatalogEntry(
        slug="small_libraries",
        title="문화체육관광부_작은도서관 운영 현황",
        provider="문화체육관광부",
        kind=DatasetKind.DATA_GO_FILE_API,
        source=SourcePortal.DATA_GO_KR,
        detail_url="https://www.data.go.kr/data/15152519/fileData.do",
        file_url="https://www.data.go.kr/cmm/cmm/fileDownload.do?atchFileId=FILE_000000003527721&fileDetailSn=1&insertDataPrcus=N",
        public_data_pk="15152519",
        public_data_detail_pk="uddi:dd06fb56-1fab-4a0e-b6dc-ca0ea909173f",
        tags=("library", "location", "operation", "csv", "odcloud"),
        notes="Included as library location/operation data only; holdings are excluded.",
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
        raise KeyError(f"unknown dataset slug {slug!r}; known slugs: {known}") from exc
