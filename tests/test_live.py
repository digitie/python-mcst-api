from __future__ import annotations

import os
import socket

import pytest

from mcst import CultureOpenApiClient, DataGoFileApiClient, McstClient
from mcst.exceptions import McstAuthError, McstError

pytestmark = pytest.mark.live


def _service_key() -> str:
    for name in ("TRIPMATE_DATA_GO_SERVICE_KEY", "DATA_GO_SERVICE_KEY", "MCST_SERVICE_KEY"):
        value = os.getenv(name)
        if value:
            return value.strip().strip('"').strip("'")
    pytest.skip("TRIPMATE_DATA_GO_SERVICE_KEY/DATA_GO_SERVICE_KEY/MCST_SERVICE_KEY is not set")
    raise AssertionError("unreachable")


def test_live_odcloud_leisure_classes_with_tripmate_key():
    key = _service_key()
    client = DataGoFileApiClient(key, timeout=20)

    try:
        page = client.leisure_classes(per_page=1)
    except McstAuthError as exc:
        pytest.skip(f"service key is present but ODCloud rejected it: {exc.result_code}")

    assert page.page_no == 1
    assert page.num_of_rows == 1
    assert page.items
    assert key not in repr(page.raw)


def test_live_kcisa_activity_endpoint_with_tripmate_key():
    key = _service_key()
    try:
        socket.gethostbyname("api.kcisa.kr")
    except OSError as exc:
        pytest.skip(f"api.kcisa.kr DNS is not resolvable in this environment: {exc}")

    client = CultureOpenApiClient(key, timeout=20)
    try:
        page = client.leisure_activity_facilities(num_of_rows=1)
    except McstError as exc:
        pytest.skip(f"KCISA live call is unavailable in this environment: {exc}")

    assert page.page_no >= 1
    assert page.items
    assert key not in repr(page.raw)


@pytest.mark.asyncio
async def test_live_async_odcloud_leisure_classes_with_tripmate_key():
    key = _service_key()

    async with McstClient.aio(service_key=key, timeout=20) as client:
        try:
            page = await client.data_go.leisure_classes(per_page=1)
        except McstAuthError as exc:
            pytest.skip(f"service key is present but ODCloud rejected it: {exc.result_code}")

    assert page.page_no == 1
    assert page.num_of_rows == 1
    assert page.items
    assert key not in repr(page.raw)
