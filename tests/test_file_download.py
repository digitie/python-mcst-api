"""CSV 파일 다운로드 전환(#6, #7) — 스크레이핑 추출/해석 표면 테스트."""

from __future__ import annotations

from pathlib import Path

import httpx
import pytest

from mcst import FileDataClient, extract_download_url
from mcst.catalog import CULTURE_FILE_DATASETS, CatalogEntry, DatasetKind, SourcePortal
from mcst.exceptions import McstParseError

from .test_clients import FakeResponse, RoutedFakeSession

HTML_FIXTURE_DIR = Path(__file__).parent / "fixtures" / "html"

_FILEDAT_PAGE_URL = (
    "https://www.culture.go.kr/data/filedat/filedatDtl.do"
    "?fileDataNo=00000000000000000443&category=H&dataType=BATCH"
)
_DATA_GO_PAGE_URL = "https://www.data.go.kr/data/15013109/fileData.do"


def test_extract_download_url_culture_filedat_page():
    """culture.go.kr filedatDtl.do의 fnFileDwld 링크를 추출하고
    한글/공백 query 값을 percent-encoding으로 정규화한다."""

    page_html = (HTML_FIXTURE_DIR / "filedat_dtl.html").read_text(encoding="utf-8")

    url = extract_download_url(page_html, _FILEDAT_PAGE_URL)

    assert url is not None
    parsed = httpx.URL(url)
    assert parsed.host == "big.kcisa.kr"
    assert parsed.path == "/common/bbsAtchFileDownload.do"
    assert parsed.params["downFileName"] == "API_CIA_089_20260530182204.csv"
    # 정규화 후 원시 한글/공백이 그대로 남지 않는다
    assert " " not in url


def test_extract_download_url_data_go_file_page():
    """data.go.kr fileData.do의 fileDownload.do 링크를 절대 URL로 추출한다."""

    page_html = (HTML_FIXTURE_DIR / "data_go_file_data.html").read_text(encoding="utf-8")

    url = extract_download_url(page_html, _DATA_GO_PAGE_URL)

    assert url is not None
    parsed = httpx.URL(url)
    assert parsed.host == "www.data.go.kr"
    assert parsed.path == "/cmm/cmm/fileDownload.do"
    assert parsed.params["atchFileId"] == "FILE_000000003647024"


def test_extract_download_url_returns_none_for_unknown_page_or_missing_link():
    assert extract_download_url("<html></html>", "https://example.com/page") is None
    assert extract_download_url("<html>링크 없음</html>", _FILEDAT_PAGE_URL) is None
    assert extract_download_url("<html>링크 없음</html>", _DATA_GO_PAGE_URL) is None


def _file_download_entry(*, file_url: str | None) -> CatalogEntry:
    return CatalogEntry(
        slug="fixture_dataset",
        title="테스트 데이터셋",
        provider="테스트 기관",
        kind=DatasetKind.FILE_DOWNLOAD,
        source=SourcePortal.CULTURE_GO_KR,
        detail_url=(
            "https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=0&dataType=BATCH"
        ),
        file_url=file_url,
    )


def test_resolve_file_url_falls_back_to_static_file_url():
    entry = _file_download_entry(file_url="https://example.com/static.csv")
    session = RoutedFakeSession({entry.detail_url: FakeResponse("<html>링크 없음</html>")})
    client = FileDataClient(session=session)

    assert client.resolve_file_url(entry) == "https://example.com/static.csv"


def test_resolve_file_url_raises_parse_error_without_link_or_fallback():
    entry = _file_download_entry(file_url=None)
    session = RoutedFakeSession({entry.detail_url: FakeResponse("<html>링크 없음</html>")})
    client = FileDataClient(session=session)

    with pytest.raises(McstParseError):
        client.resolve_file_url(entry)


def test_file_client_datasets_include_file_download_entries():
    client = FileDataClient(session=RoutedFakeSession({}))

    slugs = {entry.slug for entry in client.datasets()}

    assert set(CULTURE_FILE_DATASETS) <= slugs
