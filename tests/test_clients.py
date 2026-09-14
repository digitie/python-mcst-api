from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest

from mcst import (
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


async def test_culture_client_parses_xml_page_and_hides_service_key_from_model():
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

    page = await client.leisure_activity_facilities(num_of_rows=1)

    assert page.total_count == 1
    assert page.items[0].name == "테스트 시설"
    assert page.items[0].address == "서울시 중구"
    assert page.items[0].latitude == 37.5
    assert session.calls[0][1]["serviceKey"] == "secret-key"


async def test_culture_client_prefers_dataset_service_key():
    session = FakeSession(FakeResponse("{}", headers={"Content-Type": "application/json"}))
    client = CultureOpenApiClient(
        service_key="fallback-key",
        service_keys={"cafe_bookstores": "  cafe-key  "},
        session=session,
    )

    (await client.cafe_bookstores())

    assert session.calls[0][1]["serviceKey"] == "cafe-key"


async def test_culture_client_exposes_used_bookstores_method():
    session = FakeSession(FakeResponse("{}", headers={"Content-Type": "application/json"}))
    client = CultureOpenApiClient("secret-key", session=session)

    (await client.used_bookstores(num_of_rows=1))

    assert session.calls[0][0] == "https://api.kcisa.kr/API_CNV_045/request"
    assert session.calls[0][1]["numOfRows"] == 1


async def test_culture_client_requires_key_when_calling_endpoint():
    client = CultureOpenApiClient(service_key=None, session=FakeSession(FakeResponse("{}")))

    with pytest.raises(McstAuthError):
        (await client.leisure_activity_facilities())


async def test_data_go_client_parses_odcloud_shape():
    response = FakeResponse(
        '{"page":1,"perPage":1,"totalCount":2,"data":[{"도서관명":"시립 도서관"}]}',
        headers={"Content-Type": "application/json"},
    )
    session = FakeSession(response)
    client = DataGoFileApiClient("secret-key", session=session)

    page = await client.public_libraries(per_page=1)

    assert page.total_count == 2
    assert page.items == ({"도서관명": "시립 도서관"},)
    assert "serviceKey" in session.calls[0][1]


async def test_data_go_client_prefers_dataset_service_key():
    response = FakeResponse('{"page":1,"perPage":1,"totalCount":0,"data":[]}')
    session = FakeSession(response)
    client = DataGoFileApiClient(
        service_key="fallback-key",
        service_keys={"public_libraries": "  library-key  "},
        session=session,
    )

    (await client.public_libraries(per_page=1))

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

    async with CultureOpenApiClient("secret-key", session=session) as client:
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

    async with DataGoFileApiClient("secret-key", session=session) as client:
        page = await client.public_libraries(per_page=1)

    assert page.items == ({"도서관명": "비동기 도서관"},)
    assert session.calls[0][1]["serviceKey"] == "secret-key"


@pytest.mark.asyncio
async def test_top_level_async_client_facade():
    client = McstClient(service_key="secret-key")

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
    '<a href="#none" onclick="fnFileDwld(\'' + _LEISURE_CLASSES_CSV_URL + "')\">파일 다운로드</a>"
)


async def test_file_client_reads_csv_with_encoding_fallback():
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

    rows = await client.read_csv("leisure_classes_csv")

    assert rows == [{"name": "가나다", "address": "서울"}]
    assert [url for url, _ in session.calls] == [
        _LEISURE_CLASSES_DETAIL_URL,
        _LEISURE_CLASSES_CSV_URL,
    ]


async def test_read_csv_rejects_link_only_entries():
    client = FileDataClient(session=FakeSession(FakeResponse("")))

    with pytest.raises(McstRequestError):
        [item async for item in client.iter_csv("tourism_complexes")]


async def test_culture_client_new_helpers_and_dynamic_timeout():
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
    page1 = await client.leisure_classes(num_of_rows=1)
    assert page1.items[0].name == "신규 시설"
    assert session.calls[0][0] == "https://api.kcisa.kr/openapi/API_CIA_081/request"

    page2 = await client.recommended_travel_destinations(num_of_rows=1)
    assert page2.items[0].name == "신규 시설"
    assert session.calls[1][0] == "https://api.kcisa.kr/openapi/API_TOU_046/request"

    # dynamic timeout 검증
    (await client.leisure_classes(timeout=15.5))
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

    async with CultureOpenApiClient("secret-key", session=session) as client:
        page1 = await client.leisure_classes(num_of_rows=1)
        assert page1.items[0].name == "비동기 신규 시설"
        assert session.calls[0][0] == "https://api.kcisa.kr/openapi/API_CIA_081/request"

        page2 = await client.recommended_travel_destinations(num_of_rows=1, timeout=8.8)
        assert page2.items[0].name == "비동기 신규 시설"
        assert session.calls[1][0] == "https://api.kcisa.kr/openapi/API_TOU_046/request"
        assert session.last_timeout == 8.8


@pytest.mark.asyncio
async def test_async_file_client_save_offloads_disk_write_to_thread(tmp_path, monkeypatch):
    """async save()가 로컬 파일 쓰기를 별도 스레드로 offload하는지 검증한다.

    회귀 방지 대상: 이전에는 target.parent.mkdir()/target.write_bytes()가
    asyncio.to_thread 없이 코루틴 안에서 직접 호출되어 이벤트 루프를 막았다.
    """
    import threading

    from mcst import file_data as file_data_module

    session = AsyncRoutedFakeSession(
        {
            _LEISURE_CLASSES_DETAIL_URL: FakeResponse(_LEISURE_CLASSES_DETAIL_HTML),
            _LEISURE_CLASSES_CSV_URL: FakeResponse("col1,col2\nval1,val2\n"),
        }
    )

    main_thread = threading.current_thread()
    call_threads: list[threading.Thread] = []
    real_write_file = file_data_module._write_file

    def _tracking_write_file(target: object, data: object, **kwargs) -> None:
        call_threads.append(threading.current_thread())
        real_write_file(target, data, **kwargs)  # type: ignore[arg-type]

    monkeypatch.setattr(file_data_module, "_write_file", _tracking_write_file)

    local_path = tmp_path / "test_offload.csv"
    async with FileDataClient(session=session) as client:
        saved_path = await client.save("leisure_classes_csv", local_path)

    assert saved_path == local_path
    assert local_path.read_text() == "col1,col2\nval1,val2\n"
    assert len(call_threads) == 1
    assert call_threads[0] is not main_thread


@pytest.mark.parametrize("name", ["custom_key.csv", "custom_key.bin"])
async def test_file_client_save_rustfs_native_async_put(tmp_path, name):
    import hashlib

    import httpx

    from mcst import AsyncTokenBucket

    class Bucket(AsyncTokenBucket):
        count = 0

        async def acquire(self):
            await super().acquire()
            self.count += 1

    budget = Bucket(1000)
    sent = []
    data = b"col1,col2\nval1,val2\n"

    def handler(request):
        sent.append((request, budget.count))
        if request.method == "PUT":
            return httpx.Response(200)
        if str(request.url) == _LEISURE_CLASSES_DETAIL_URL:
            return httpx.Response(200, text=_LEISURE_CLASSES_DETAIL_HTML)
        assert str(request.url) == _LEISURE_CLASSES_CSV_URL
        return httpx.Response(200, content=data)

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as session:
        async with FileDataClient(session=session, rate_limiter=budget) as client:
            saved = await client.save_rustfs(
                "leisure_classes_csv",
                tmp_path / name,
                object_key=name,
                endpoint_url="http://test-rustfs:9000",
                bucket="test-bucket",
                access_key_id="synthetic-access",
                secret_access_key="synthetic-secret",
            )
        assert not session.is_closed
    assert saved.read_bytes() == data
    assert [count for _, count in sent] == [1, 2, 3]
    request = sent[-1][0]
    assert request.url.path == "/test-bucket/" + name
    assert request.content == data
    assert request.headers["x-amz-content-sha256"] == hashlib.sha256(data).hexdigest()
    assert request.headers["authorization"].startswith(
        "AWS4-HMAC-SHA256 Credential=synthetic-access/"
    )
    assert request.headers["content-type"] == (
        "text/csv" if name.endswith(".csv") else "application/octet-stream"
    )


async def test_data_go_client_throttles_sequential_requests(monkeypatch):
    import asyncio
    from types import SimpleNamespace

    from mcst import AsyncTokenBucket, _ratelimit

    now = [1000.0]
    sleeps = []

    async def sleep(delay):
        sleeps.append(delay)
        now[0] += delay

    monkeypatch.setattr(_ratelimit, "time", SimpleNamespace(monotonic=lambda: now[0]))
    monkeypatch.setattr(
        _ratelimit,
        "asyncio",
        SimpleNamespace(Lock=asyncio.Lock, sleep=sleep, get_running_loop=asyncio.get_running_loop),
    )
    session = FakeSession(FakeResponse('{"page":1,"perPage":1,"totalCount":0,"data":[]}'))
    async with DataGoFileApiClient(
        "secret-key", session=session, rate_limiter=AsyncTokenBucket(2, capacity=1)
    ) as client:
        await client.public_libraries(per_page=1)
        await client.public_libraries(per_page=1)
    assert sleeps == [0.5]
