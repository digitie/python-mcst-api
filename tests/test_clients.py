from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest

from mcst import (
    AsyncCultureOpenApiClient,
    AsyncDataGoFileApiClient,
    AsyncFileDataClient,
    CultureOpenApiClient,
    DataGoFileApiClient,
    FileDataClient,
    McstClient,
)
from mcst.exceptions import McstAuthError, McstRequestError


@dataclass
class FakeResponse:
    text: str
    status_code: int = 200
    headers: dict[str, str] | None = None
    body: bytes | None = None

    @property
    def content(self) -> bytes:
        if self.body is not None:
            return self.body
        return self.text.encode("utf-8")

    def json(self) -> Any:
        import json

        return json.loads(self.text)


class FakeSession:
    def __init__(self, response: FakeResponse) -> None:
        self.response = response
        self.calls: list[tuple[str, dict[str, Any]]] = []
        self.last_timeout: float | None = None

    def get(
        self,
        url: str,
        *,
        params: dict[str, Any] | None = None,
        timeout: float,
    ) -> FakeResponse:
        self.calls.append((url, dict(params or {})))
        self.last_timeout = timeout
        return self.response


class AsyncFakeSession:
    def __init__(self, response: FakeResponse) -> None:
        self.response = response
        self.calls: list[tuple[str, dict[str, Any]]] = []
        self.last_timeout: float | None = None
        self.closed = False

    async def get(
        self,
        url: str,
        *,
        params: dict[str, Any] | None = None,
        timeout: float,
    ) -> FakeResponse:
        self.calls.append((url, dict(params or {})))
        self.last_timeout = timeout
        return self.response

    async def aclose(self) -> None:
        self.closed = True


class RoutedFakeSession:
    """URL별 응답 라우팅 fake — 파일 다운로드 2-hop(상세페이지→CSV) 흐름용."""

    def __init__(self, routes: dict[str, FakeResponse]) -> None:
        self.routes = routes
        self.calls: list[tuple[str, dict[str, Any]]] = []

    def get(
        self,
        url: str,
        *,
        params: dict[str, Any] | None = None,
        timeout: float,
    ) -> FakeResponse:
        self.calls.append((url, dict(params or {})))
        try:
            return self.routes[url]
        except KeyError:  # pragma: no cover - 테스트 작성 오류 가드
            raise AssertionError(f"unexpected URL in fake session: {url}") from None


class AsyncRoutedFakeSession:
    def __init__(self, routes: dict[str, FakeResponse]) -> None:
        self.routes = routes
        self.calls: list[tuple[str, dict[str, Any]]] = []
        self.closed = False

    async def get(
        self,
        url: str,
        *,
        params: dict[str, Any] | None = None,
        timeout: float,
    ) -> FakeResponse:
        self.calls.append((url, dict(params or {})))
        try:
            return self.routes[url]
        except KeyError:  # pragma: no cover - 테스트 작성 오류 가드
            raise AssertionError(f"unexpected URL in fake session: {url}") from None

    async def aclose(self) -> None:
        self.closed = True


def test_culture_client_parses_xml_page_and_hides_service_key_from_model():
    xml = """
    <response>
      <header><resultCode>00</resultCode><resultMsg>OK</resultMsg></header>
      <body>
        <pageNo>1</pageNo><numOfRows>1</numOfRows><totalCount>1</totalCount>
        <items>
          <item>
            <title>테스트 시설</title>
            <address>서울시 중구</address>
            <latitude>37.5</latitude>
            <longitude>127.0</longitude>
          </item>
        </items>
      </body>
    </response>
    """
    session = FakeSession(FakeResponse(xml, headers={"Content-Type": "application/xml"}))
    client = CultureOpenApiClient("secret-key", session=session)

    page = client.leisure_activity_facilities(num_of_rows=1)

    assert page.total_count == 1
    assert page.items[0].name == "테스트 시설"
    assert page.items[0].address == "서울시 중구"
    assert page.items[0].latitude == 37.5
    assert session.calls[0][1]["serviceKey"] == "secret-key"


def test_culture_client_prefers_dataset_service_key():
    session = FakeSession(FakeResponse("{}", headers={"Content-Type": "application/json"}))
    client = CultureOpenApiClient(
        service_key="fallback-key",
        service_keys={"cafe_bookstores": "  cafe-key  "},
        session=session,
    )

    client.cafe_bookstores()

    assert session.calls[0][1]["serviceKey"] == "cafe-key"


def test_culture_client_exposes_used_bookstores_method():
    session = FakeSession(FakeResponse("{}", headers={"Content-Type": "application/json"}))
    client = CultureOpenApiClient("secret-key", session=session)

    client.used_bookstores(num_of_rows=1)

    assert session.calls[0][0] == "http://api.kcisa.kr/API_CNV_045/request"
    assert session.calls[0][1]["numOfRows"] == 1


def test_culture_client_requires_key_when_calling_endpoint():
    client = CultureOpenApiClient(service_key=None, session=FakeSession(FakeResponse("{}")))

    with pytest.raises(McstAuthError):
        client.leisure_activity_facilities()


def test_data_go_client_parses_odcloud_shape():
    response = FakeResponse(
        '{"page":1,"perPage":1,"totalCount":2,"data":[{"도서관명":"시립 도서관"}]}',
        headers={"Content-Type": "application/json"},
    )
    session = FakeSession(response)
    client = DataGoFileApiClient("secret-key", session=session)

    page = client.public_libraries(per_page=1)

    assert page.total_count == 2
    assert page.items == ({"도서관명": "시립 도서관"},)
    assert "serviceKey" in session.calls[0][1]


def test_data_go_client_prefers_dataset_service_key():
    response = FakeResponse('{"page":1,"perPage":1,"totalCount":0,"data":[]}')
    session = FakeSession(response)
    client = DataGoFileApiClient(
        service_key="fallback-key",
        service_keys={"public_libraries": "  library-key  "},
        session=session,
    )

    client.public_libraries(per_page=1)

    assert session.calls[0][1]["serviceKey"] == "library-key"


@pytest.mark.asyncio
async def test_async_culture_client_parses_xml_page():
    xml = """
    <response>
      <header><resultCode>00</resultCode><resultMsg>OK</resultMsg></header>
      <body>
        <pageNo>1</pageNo><numOfRows>1</numOfRows><totalCount>1</totalCount>
        <items>
          <item><title>비동기 시설</title><address>서울시 종로구</address></item>
        </items>
      </body>
    </response>
    """
    session = AsyncFakeSession(FakeResponse(xml, headers={"Content-Type": "application/xml"}))

    async with AsyncCultureOpenApiClient("secret-key", session=session) as client:
        page = await client.leisure_activity_facilities(num_of_rows=1)

    assert page.items[0].name == "비동기 시설"
    assert session.calls[0][1]["serviceKey"] == "secret-key"
    assert client.closed is True


@pytest.mark.asyncio
async def test_async_data_go_client_parses_odcloud_shape():
    response = FakeResponse(
        '{"page":1,"perPage":1,"totalCount":1,"data":[{"도서관명":"비동기 도서관"}]}',
        headers={"Content-Type": "application/json"},
    )
    session = AsyncFakeSession(response)

    async with AsyncDataGoFileApiClient("secret-key", session=session) as client:
        page = await client.public_libraries(per_page=1)

    assert page.items == ({"도서관명": "비동기 도서관"},)
    assert session.calls[0][1]["serviceKey"] == "secret-key"


@pytest.mark.asyncio
async def test_top_level_async_client_facade():
    client = McstClient.aio(service_key="secret-key")

    async with client as active:
        assert active.culture.service_key == "secret-key"
        assert active.data_go.service_key == "secret-key"

    assert client.closed is True


_LEISURE_CLASSES_DETAIL_URL = (
    "https://www.culture.go.kr/data/filedat/filedatDtl.do"
    "?fileDataNo=00000000000000000242&category=C&orderBy=dwldCnt"
    "&category=H&dataType=BATCH"
)
_LEISURE_CLASSES_CSV_URL = (
    "https://big.kcisa.kr/common/bbsAtchFileDownload.do"
    "?downFileName=API_CIA_081_20260530.csv&downFilePath=apiExcelData"
)
_LEISURE_CLASSES_DETAIL_HTML = (
    "<a href=\"#none\" onclick=\"fnFileDwld('"
    + _LEISURE_CLASSES_CSV_URL
    + "')\">파일 다운로드</a>"
)


def test_file_client_reads_csv_with_encoding_fallback():
    """FILE_DOWNLOAD 데이터셋은 상세페이지 스크레이핑 → CSV 다운로드 2-hop이고,
    utf-8로 못 읽는 본문은 cp949 폴백으로 디코딩한다."""

    csv_bytes = "name,address\n가나다,서울\n".encode("cp949")
    session = RoutedFakeSession(
        {
            _LEISURE_CLASSES_DETAIL_URL: FakeResponse(_LEISURE_CLASSES_DETAIL_HTML),
            _LEISURE_CLASSES_CSV_URL: FakeResponse("", body=csv_bytes),
        }
    )
    client = FileDataClient(session=session)

    rows = client.read_csv("leisure_classes_csv")

    assert rows == [{"name": "가나다", "address": "서울"}]
    assert [url for url, _ in session.calls] == [
        _LEISURE_CLASSES_DETAIL_URL,
        _LEISURE_CLASSES_CSV_URL,
    ]


def test_read_csv_rejects_link_only_entries():
    client = FileDataClient(session=FakeSession(FakeResponse("")))

    with pytest.raises(McstRequestError):
        list(client.iter_csv("tourism_complexes"))


def test_culture_client_new_helpers_and_dynamic_timeout():
    xml = """
    <response>
      <header><resultCode>00</resultCode><resultMsg>OK</resultMsg></header>
      <body>
        <pageNo>1</pageNo><numOfRows>1</numOfRows><totalCount>1</totalCount>
        <items>
          <item><title>신규 시설</title><address>강원도 강릉시</address></item>
        </items>
      </body>
    </response>
    """
    session = FakeSession(FakeResponse(xml, headers={"Content-Type": "application/xml"}))
    client = CultureOpenApiClient("secret-key", session=session)

    # 신규 헬퍼 메서드 동기 호출 검증
    page1 = client.leisure_classes(num_of_rows=1)
    assert page1.items[0].name == "신규 시설"
    assert session.calls[0][0] == "https://api.kcisa.kr/openapi/API_CIA_081/request"

    page2 = client.recommended_travel_destinations(num_of_rows=1)
    assert page2.items[0].name == "신규 시설"
    assert session.calls[1][0] == "https://api.kcisa.kr/openapi/API_TOU_046/request"

    # dynamic timeout 검증
    client.leisure_classes(timeout=15.5)
    assert session.last_timeout == 15.5


@pytest.mark.asyncio
async def test_async_culture_client_new_helpers_and_dynamic_timeout():
    xml = """
    <response>
      <header><resultCode>00</resultCode><resultMsg>OK</resultMsg></header>
      <body>
        <pageNo>1</pageNo><numOfRows>1</numOfRows><totalCount>1</totalCount>
        <items>
          <item><title>비동기 신규 시설</title></item>
        </items>
      </body>
    </response>
    """
    session = AsyncFakeSession(FakeResponse(xml, headers={"Content-Type": "application/xml"}))

    async with AsyncCultureOpenApiClient("secret-key", session=session) as client:
        page1 = await client.leisure_classes(num_of_rows=1)
        assert page1.items[0].name == "비동기 신규 시설"
        assert session.calls[0][0] == "https://api.kcisa.kr/openapi/API_CIA_081/request"

        page2 = await client.recommended_travel_destinations(num_of_rows=1, timeout=8.8)
        assert page2.items[0].name == "비동기 신규 시설"
        assert session.calls[1][0] == "https://api.kcisa.kr/openapi/API_TOU_046/request"
        assert session.last_timeout == 8.8


def test_file_client_save_rustfs(tmp_path, monkeypatch):
    import sys
    import unittest.mock

    session = RoutedFakeSession(
        {
            _LEISURE_CLASSES_DETAIL_URL: FakeResponse(_LEISURE_CLASSES_DETAIL_HTML),
            _LEISURE_CLASSES_CSV_URL: FakeResponse("col1,col2\nval1,val2\n"),
        }
    )
    client = FileDataClient(session=session)

    mock_s3 = unittest.mock.MagicMock()
    mock_boto3 = unittest.mock.MagicMock()
    mock_boto3.client.return_value = mock_s3

    # 동적 mocking
    monkeypatch.setitem(sys.modules, "boto3", mock_boto3)
    monkeypatch.setitem(sys.modules, "botocore", unittest.mock.MagicMock())
    monkeypatch.setitem(sys.modules, "botocore.config", unittest.mock.MagicMock())

    monkeypatch.setenv("MCST_RUSTFS_ENDPOINT_URL", "http://test-rustfs:9000")
    monkeypatch.setenv("MCST_RUSTFS_BUCKET", "test-bucket")

    local_path = tmp_path / "test_data.csv"

    saved_path = client.save_rustfs(
        "leisure_classes_csv",
        local_path,
        object_key="custom_key.csv",
    )

    assert saved_path == local_path
    assert local_path.read_text() == "col1,col2\nval1,val2\n"

    mock_boto3.client.assert_called_once()
    mock_s3.put_object.assert_called_once_with(
        Bucket="test-bucket",
        Key="custom_key.csv",
        Body=b"col1,col2\nval1,val2\n",
        ContentType="text/csv",
    )


@pytest.mark.asyncio
async def test_async_file_client_save_rustfs(tmp_path, monkeypatch):
    import sys
    import unittest.mock

    session = AsyncRoutedFakeSession(
        {
            _LEISURE_CLASSES_DETAIL_URL: FakeResponse(_LEISURE_CLASSES_DETAIL_HTML),
            _LEISURE_CLASSES_CSV_URL: FakeResponse("col1,col2\nval1,val2\n"),
        }
    )

    mock_s3 = unittest.mock.MagicMock()
    mock_boto3 = unittest.mock.MagicMock()
    mock_boto3.client.return_value = mock_s3

    # 동적 mocking
    monkeypatch.setitem(sys.modules, "boto3", mock_boto3)
    monkeypatch.setitem(sys.modules, "botocore", unittest.mock.MagicMock())
    monkeypatch.setitem(sys.modules, "botocore.config", unittest.mock.MagicMock())

    monkeypatch.setenv("MCST_RUSTFS_ENDPOINT_URL", "http://test-rustfs:9000")
    monkeypatch.setenv("MCST_RUSTFS_BUCKET", "test-bucket")

    local_path = tmp_path / "test_data_async.csv"

    async with AsyncFileDataClient(session=session) as client:
        saved_path = await client.save_rustfs(
            "leisure_classes_csv",
            local_path,
            object_key="custom_key_async.csv",
        )

    assert saved_path == local_path
    assert local_path.read_text() == "col1,col2\nval1,val2\n"

    mock_boto3.client.assert_called_once()
    mock_s3.put_object.assert_called_once_with(
        Bucket="test-bucket",
        Key="custom_key_async.csv",
        Body=b"col1,col2\nval1,val2\n",
        ContentType="text/csv",
    )
