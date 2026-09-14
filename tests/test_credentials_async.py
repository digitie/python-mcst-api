"""실제 요청 키가 오류 속성과 디버그 결과에 남지 않는지 검증합니다."""

from __future__ import annotations

import traceback
from urllib.parse import quote, quote_plus

import httpx
import pytest

from mcst import McstClient
from mcst.exceptions import McstError, McstRateLimitError
from mcst.models import CultureRecord, Page

KEY = "configured-test-key"
OVERRIDE = "override /+테스트=key"


@pytest.mark.parametrize("provider", ["culture", "data_go"])
@pytest.mark.parametrize("status", [200, 403, 429])
async def test_overridden_key_is_removed_from_all_error_fields(provider, status):
    echo = f"{KEY}|{OVERRIDE}|{quote(OVERRIDE, safe='')}|{quote_plus(OVERRIDE)}"

    def handler(request):
        assert request.url.params["serviceKey"] == OVERRIDE
        return httpx.Response(status, json={"code": "ERROR_" + echo, "message": echo})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as session:
        async with McstClient(KEY, session=session, retries=0) as client:
            child = getattr(client, provider)
            slug = "cafe_bookstores" if provider == "culture" else "public_libraries"
            with pytest.raises(McstError) as caught:
                await child.request(slug, params={"serviceKey": OVERRIDE})
    rendered = str(caught.value) + repr(vars(caught.value))
    rendered += "".join(traceback.format_exception(caught.value))
    for value in (KEY, OVERRIDE, quote(OVERRIDE, safe=""), quote_plus(OVERRIDE)):
        assert value not in rendered
    if status in (403, 429):
        assert caught.value.status_code == status


async def test_debug_masks_response_headers_models_and_unsupported_input():
    def handler(request):
        return httpx.Response(
            200,
            headers={"x-echo": quote(OVERRIDE, safe="")},
            json={"items": [{"title": OVERRIDE, "address": KEY}], "totalCount": 1},
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as session:
        async with McstClient(KEY, session=session, retries=0) as client:
            run = await client.debug_fetch("cafe_bookstores", params={"serviceKey": OVERRIDE})
            unsupported = await client.debug_fetch(
                "cafe_bookstores_csv", params={"serviceKey": OVERRIDE}, keyword=KEY
            )
    assert run.error is None
    assert isinstance(run.parsed, Page)
    assert isinstance(run.parsed.items, tuple)
    assert isinstance(run.parsed.items[0], CultureRecord)
    assert unsupported.error["failure_kind"] == "unsupported_kind"
    for value in (KEY, OVERRIDE, quote(OVERRIDE, safe="")):
        assert value not in repr(run)
        assert value not in repr(unsupported)


@pytest.mark.parametrize("status", [200, 400])
async def test_quota_classification_precedes_masking(status):
    def handler(request):
        return httpx.Response(
            status,
            json={"code": "22", "message": "LIMITED_NUMBER_OF_SERVICE_REQUESTS_EXCEEDS_ERROR"},
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as session:
        async with McstClient("22", session=session, retries=0) as client:
            with pytest.raises(McstRateLimitError):
                await client.culture.cafe_bookstores()
