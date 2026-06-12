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


class HttpxSemanticsFakeSession:
    """httpx 의미론 모사 fake — ``params``를 명시하면(빈 dict 포함) URL 자체의
    query를 **대체**한다 (#9 회귀 재현용). RoutedFakeSession은 url 문자열을
    그대로 비교해 이 결함을 잡지 못했다."""

    def __init__(self, routes: dict[str, FakeResponse]) -> None:
        self.routes = routes
        self.calls: list[str] = []

    def get(
        self,
        url: str,
        *,
        params: dict[str, object] | None = None,
        timeout: float,
    ) -> FakeResponse:
        if params is not None:
            # httpx: explicit params는 기존 query를 통째로 대체한다.
            base = url.split("?", 1)[0]
            if params:
                from urllib.parse import urlencode

                url = f"{base}?{urlencode(params)}"
            else:
                url = base
        self.calls.append(url)
        try:
            return self.routes[url]
        except KeyError:  # pragma: no cover - 테스트 작성 오류 가드
            raise AssertionError(f"unexpected URL in fake session: {url}") from None


def test_get_response_preserves_url_query_when_no_params():
    """#9 회귀: 빈 params가 detail_url의 query를 박탈해 빈 셸 페이지가 오던 버그.

    httpx 의미론 fake로, params 없는 ``get_response`` 호출이 URL query를
    보존하는지(=wrapper가 빈 params를 전달하지 않는지) 검증한다."""

    entry = _file_download_entry(file_url=None)
    csv_url = "https://big.kcisa.kr/common/bbsAtchFileDownload.do?downFileName=x.csv"
    html = f"<a onclick=\"fnFileDwld('{csv_url}')\">다운로드</a>"
    session = HttpxSemanticsFakeSession(
        {
            entry.detail_url: FakeResponse(html),
            csv_url: FakeResponse("h1,h2\nv1,v2\n"),
        }
    )
    client = FileDataClient(session=session)

    rows = client.read_csv(entry)

    assert rows == [{"h1": "v1", "h2": "v2"}]
    assert session.calls[0] == entry.detail_url  # query 보존
