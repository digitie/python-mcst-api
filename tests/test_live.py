from __future__ import annotations

import os
import socket

import pytest

from mcst import CultureOpenApiClient, McstClient
from mcst.exceptions import McstError

pytestmark = pytest.mark.live


def _service_key() -> str:
    for name in ("KCISA_SERVICE_KEY", "DATA_GO_KR_SERVICE_KEY"):
        value = os.getenv(name)
        if value:
            return value.strip().strip('"').strip("'")
    pytest.skip("KCISA_SERVICE_KEY or DATA_GO_KR_SERVICE_KEY is not set")
    raise AssertionError("unreachable")


def test_live_kcisa_leisure_classes_with_tripmate_key():
    key = _service_key()
    try:
        socket.gethostbyname("api.kcisa.kr")
    except OSError as exc:
        pytest.skip(f"api.kcisa.kr DNS is not resolvable in this environment: {exc}")

    client = CultureOpenApiClient(key, timeout=20)
    try:
        page = client.leisure_classes(num_of_rows=1)
    except McstError as exc:
        pytest.skip(f"KCISA live call is unavailable in this environment: {exc}")

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
async def test_live_async_kcisa_leisure_classes_with_tripmate_key():
    key = _service_key()
    try:
        socket.gethostbyname("api.kcisa.kr")
    except OSError as exc:
        pytest.skip(f"api.kcisa.kr DNS is not resolvable in this environment: {exc}")

    async with McstClient.aio(service_key=key, timeout=20) as client:
        try:
            page = await client.culture.leisure_classes(num_of_rows=1)
        except McstError as exc:
            pytest.skip(f"KCISA live call is unavailable in this environment: {exc}")

    assert page.page_no == 1
    assert page.num_of_rows == 1
    assert page.items
    assert key not in repr(page.raw)
