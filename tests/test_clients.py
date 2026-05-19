from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest

from mcst import (
    AsyncCultureOpenApiClient,
    AsyncDataGoFileApiClient,
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

    @property
    def content(self) -> bytes:
        return self.text.encode("utf-8")

    def json(self) -> Any:
        import json

        return json.loads(self.text)


class FakeSession:
    def __init__(self, response: FakeResponse) -> None:
        self.response = response
        self.calls: list[tuple[str, dict[str, Any]]] = []

    def get(
        self,
        url: str,
        *,
        params: dict[str, Any] | None = None,
        timeout: float,
    ) -> FakeResponse:
        self.calls.append((url, dict(params or {})))
        return self.response


class AsyncFakeSession:
    def __init__(self, response: FakeResponse) -> None:
        self.response = response
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
        return self.response

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


def test_culture_client_requires_key_when_calling_endpoint():
    client = CultureOpenApiClient(service_key=None, session=FakeSession(FakeResponse("{}")))

    with pytest.raises(McstAuthError):
        client.leisure_activity_facilities()


def test_data_go_client_parses_odcloud_shape():
    response = FakeResponse(
        '{"page":1,"perPage":1,"totalCount":2,"data":[{"클래스 타이틀":"도예 클래스"}]}',
        headers={"Content-Type": "application/json"},
    )
    session = FakeSession(response)
    client = DataGoFileApiClient("secret-key", session=session)

    page = client.leisure_classes(per_page=1)

    assert page.total_count == 2
    assert page.items == ({"클래스 타이틀": "도예 클래스"},)
    assert "serviceKey" in session.calls[0][1]


def test_data_go_client_prefers_dataset_service_key():
    response = FakeResponse('{"page":1,"perPage":1,"totalCount":0,"data":[]}')
    session = FakeSession(response)
    client = DataGoFileApiClient(
        service_key="fallback-key",
        service_keys={"leisure_classes_csv": "  class-key  "},
        session=session,
    )

    client.leisure_classes(per_page=1)

    assert session.calls[0][1]["serviceKey"] == "class-key"


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
        '{"page":1,"perPage":1,"totalCount":1,"data":[{"클래스 타이틀":"비동기 클래스"}]}',
        headers={"Content-Type": "application/json"},
    )
    session = AsyncFakeSession(response)

    async with AsyncDataGoFileApiClient("secret-key", session=session) as client:
        page = await client.leisure_classes(per_page=1)

    assert page.items == ({"클래스 타이틀": "비동기 클래스"},)
    assert session.calls[0][1]["serviceKey"] == "secret-key"


@pytest.mark.asyncio
async def test_top_level_async_client_facade():
    client = McstClient.aio(service_key="secret-key")

    async with client as active:
        assert active.culture.service_key == "secret-key"
        assert active.data_go.service_key == "secret-key"

    assert client.closed is True


def test_file_client_reads_csv_with_encoding_fallback():
    session = FakeSession(FakeResponse("name,address\nA,Seoul\n"))
    client = FileDataClient(session=session)

    rows = client.read_csv("leisure_classes_csv")

    assert rows == [{"name": "A", "address": "Seoul"}]


def test_read_csv_rejects_link_only_entries():
    client = FileDataClient(session=FakeSession(FakeResponse("")))

    with pytest.raises(McstRequestError):
        list(client.iter_csv("tourism_complexes"))
