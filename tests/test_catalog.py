from __future__ import annotations

from mcst import ALL_DATASETS, CULTURE_OPEN_APIS, FILE_DATASETS, get_api_catalog
from mcst.catalog import DatasetKind


def test_catalog_excludes_kto_and_non_mcst_sources():
    for entry in ALL_DATASETS.values():
        assert "한국관광공사" not in entry.provider
        assert "행정안전부" not in entry.provider


def test_library_entries_are_location_or_operation_only():
    library_entries = [entry for entry in ALL_DATASETS.values() if "library" in entry.tags]

    assert library_entries
    for entry in library_entries:
        text = f"{entry.title} {entry.notes or ''}"
        assert "소장자료" not in text
        assert "ISBN" not in text
        assert {"location", "operation"} & set(entry.tags)


def test_open_api_entries_have_kcisa_endpoints():
    assert CULTURE_OPEN_APIS
    for entry in CULTURE_OPEN_APIS.values():
        assert entry.kind == DatasetKind.KCISA_OPEN_API
        assert entry.endpoint_url is not None
        assert entry.endpoint_url.startswith("https://api.kcisa.kr/openapi/")


def test_file_api_entries_have_download_or_link_urls():
    assert FILE_DATASETS
    for entry in FILE_DATASETS.values():
        assert entry.file_url
        assert entry.detail_url.startswith("https://")


def test_get_api_catalog_returns_human_readable_labels():
    catalog = get_api_catalog(kind=DatasetKind.KCISA_OPEN_API)
    cafe = next(item for item in catalog if item["slug"] == "cafe_bookstores")

    assert cafe["title"] == "한국문화정보원_카페가 있는 서점데이터"
    assert cafe["label"] == "한국문화정보원_카페가 있는 서점데이터 (cafe_bookstores)"
    assert cafe["endpoint_url"] == "https://api.kcisa.kr/openapi/API_CIA_090/request"
