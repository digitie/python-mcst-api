from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

import pytest

from mcst import CultureOpenApiClient, DataGoFileApiClient, save_fixture
from mcst.debug import REDACTED


@dataclass
class FakeResponse:
    text: str
    status_code: int = 200
    headers: dict[str, str] | None = None

    @property
    def content(self) -> bytes:
        return self.text.encode("utf-8")

    def json(self) -> Any:
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


def test_culture_debug_request_redacts_key_and_saves_fixture(tmp_path):
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

    debug_run = client.debug_request("leisure_activity_facilities", num_of_rows=1)

    assert debug_run.error is None
    assert debug_run.function == "culture.leisure_activity_facilities"
    assert debug_run.request["query"]["serviceKey"] == REDACTED
    assert debug_run.processed["items"][0]["name"] == "테스트 시설"
    assert "raw" not in debug_run.processed

    path = save_fixture(
        debug_run,
        base_dir=tmp_path,
        case_name="Secret Case",
        description="민감정보 마스킹 fixture 저장",
        library_version="0.1.0",
    )
    saved = json.loads(path.read_text(encoding="utf-8"))

    assert path.name == "secret_case.json"
    assert saved["request"]["query"]["serviceKey"] == REDACTED
    assert saved["meta"]["source"] == "debug_ui"
    with pytest.raises(FileExistsError):
        save_fixture(debug_run, base_dir=tmp_path, case_name="Secret Case")


def test_data_go_debug_request_uses_fixture_function_name():
    response = FakeResponse(
        '{"page":1,"perPage":1,"totalCount":1,"data":[{"도서관명":"시립 도서관"}]}',
        headers={"Content-Type": "application/json"},
    )
    client = DataGoFileApiClient("secret-key", session=FakeSession(response))

    debug_run = client.debug_request("public_libraries", per_page=1)

    assert debug_run.error is None
    assert debug_run.function == "data_go.public_libraries"
    assert debug_run.request["query"]["serviceKey"] == REDACTED
    assert debug_run.processed["items"] == [{"도서관명": "시립 도서관"}]
