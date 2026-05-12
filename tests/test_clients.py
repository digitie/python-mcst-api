from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest

from mcst import CultureOpenApiClient, DataGoFileApiClient, FileDataClient
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


def test_file_client_reads_csv_with_encoding_fallback():
    session = FakeSession(FakeResponse("name,address\nA,Seoul\n"))
    client = FileDataClient(session=session)

    rows = client.read_csv("leisure_classes_csv")

    assert rows == [{"name": "A", "address": "Seoul"}]


def test_read_csv_rejects_link_only_entries():
    client = FileDataClient(session=FakeSession(FakeResponse("")))

    with pytest.raises(McstRequestError):
        list(client.iter_csv("tourism_complexes"))
