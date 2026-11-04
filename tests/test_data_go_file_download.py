"""현재 data.go.kr 승인 흐름과 골프장 본 CSV의 오프라인 회귀."""

from __future__ import annotations

import asyncio
import io
import zipfile
from urllib.parse import parse_qs

import httpx
import pytest

from mcst import FileDataClient
from mcst._http import HttpClient
from mcst.exceptions import McstNetworkError, McstParseError, McstRequestError, McstServerError
from mcst.file_data import _parse_csv_rows

PAGE = "https://www.data.go.kr/data/15118920/fileData.do"
META = "/tcs/dss/selectFileDataDownload.do"
LIMIT = "/cmm/cmm/check-limit.json"
FILE = "/cmm/cmm/fileDownload.do"
HTML = """<button onclick="fileDetailObj.fn_fileDataDown(
  '15118920', 'uddi:fixture-detail', '', '1', '8')">다운로드</button>"""
COLUMNS = "지역,이름,사업자,소재지,면적(제곱미터),홀,구분"
CSV = COLUMNS + "\n서울,검증골프장,검증사업자,서울특별시,123,18,일반\n"
METADATA = {
    "status": True,
    "atchFileId": "FILE_FIXTURE",
    "fileDetailSn": "1",
    "dataSetFileDetailInfo": {
        "publicDataTyDetailCode": "DATY03",
        "dataNm": "골프장 자료 fixture",
        "publicDataSj": "골프장 현황",
    },
}


class Budget:
    def __init__(self):
        self.count = 0

    async def acquire(self):
        self.count += 1


def zipped(members):
    target = io.BytesIO()
    with zipfile.ZipFile(target, "w") as archive:
        for name, text in members:
            archive.writestr(name, text.encode("utf-8-sig"))
    return target.getvalue()


def golf_zip():
    return zipped(
        [
            ("포장/표준산출물/데이터사전.csv", "컬럼명,정의\n이름,시설 이름\n"),
            ("포장/이름이바뀐본자료.csv", CSV),
        ]
    )


@pytest.mark.parametrize("download_redirect", [False, True])
async def test_native_portal_form_cookie_budget_and_real_csv(download_redirect):
    requests = []
    form = {
        "publicDataPk": ["15118920"],
        "publicDataDetailPk": ["uddi:fixture-detail"],
        "atchFileId": [""],
        "fileDetailSn": ["1"],
        "publicDataTyCode": ["PR0051"],
        "url": [META],
    }

    async def handler(request):
        requests.append(request)
        path = request.url.path
        if path == "/data/15118920/fileData.do":
            return httpx.Response(
                200, text=HTML, headers={"set-cookie": "portal_fixture=ready; Path=/"}
            )
        assert request.headers["cookie"] == "portal_fixture=ready"
        if path == META:
            assert request.method == "POST"
            assert parse_qs(request.content.decode(), keep_blank_values=True) == form
            return httpx.Response(200, json=METADATA)
        if path == LIMIT:
            assert request.method == "POST"
            assert parse_qs(request.content.decode()) == {
                "atchFileId": ["FILE_FIXTURE"],
                "fileDetailSn": ["1"],
            }
            return httpx.Response(200, json={"needCaptcha": False})
        if path == "/fixture-csv":
            assert request.method == "GET"
            return httpx.Response(200, content=golf_zip())
        assert path == FILE and request.method == "GET"
        assert dict(request.url.params) == {
            "atchFileId": "FILE_FIXTURE",
            "fileDetailSn": "1",
            "dataNm": "골프장 자료 fixture",
        }
        if download_redirect:
            return httpx.Response(302, headers={"location": "/fixture-csv"})
        return httpx.Response(200, content=golf_zip())

    budget = Budget()
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler), follow_redirects=True
    ) as session:
        async with FileDataClient(session=session, rate_limiter=budget) as client:
            rows = await client.read_csv("golf_courses_status")
        assert not session.is_closed
    assert len(rows) == 1 and rows[0]["이름"] == "검증골프장"
    assert len(requests) == budget.count == (5 if download_redirect else 4)


@pytest.mark.parametrize("decision", [True, None, 0, "false", {}, []])
async def test_captcha_or_unknown_decision_never_downloads(decision):
    requests = []

    async def handler(request):
        requests.append(request.url.path)
        if request.url.path == "/data/15118920/fileData.do":
            return httpx.Response(200, text=HTML)
        if request.url.path == META:
            return httpx.Response(200, json=METADATA)
        assert request.url.path == LIMIT
        return httpx.Response(200, json={"needCaptcha": decision})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as session:
        async with FileDataClient(session=session) as client:
            with pytest.raises(McstRequestError) as captured:
                await client.read_csv("golf_courses_status")
    assert captured.value.result_code == (
        "CAPTCHA_REQUIRED" if decision is True else "DOWNLOAD_CHECK_FAILED"
    )
    assert requests == ["/data/15118920/fileData.do", META, LIMIT]


async def test_metadata_post_server_error_is_not_automatically_retried():
    requests = []

    async def handler(request):
        requests.append(request.method)
        if request.method == "GET":
            return httpx.Response(200, text=HTML)
        return httpx.Response(503, text="fixture unavailable")

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as session:
        async with FileDataClient(session=session, retries=3) as client:
            with pytest.raises(McstServerError):
                await client.read_csv("golf_courses_status")
    assert requests == ["GET", "POST"]


async def test_get_only_data_go_session_has_explicit_redirect_capability_error():
    class Response:
        status_code = 200
        text = HTML
        content = HTML.encode()
        headers = {}

    class GetOnly:
        async def get(self, url, *, params=None, timeout):
            return Response()

    async with FileDataClient(session=GetOnly()) as client:
        with pytest.raises(McstRequestError) as captured:
            await client.read_csv("golf_courses_status")
    assert captured.value.result_code == "SESSION_REDIRECT_UNSUPPORTED"


def test_zip_does_not_parse_first_dictionary_as_golf_data():
    rows = _parse_csv_rows(golf_zip(), "golf_courses_status", None)
    assert len(rows) == 1 and rows[0].get("이름") == "검증골프장"
    assert set(rows[0]) == set(COLUMNS.split(","))


def test_ambiguous_peer_csvs_are_rejected():
    raw = zipped([("data/a.csv", CSV), ("data/b.csv", CSV)])
    with pytest.raises(McstParseError):
        _parse_csv_rows(raw, "golf_courses_status", None)


def test_golf_dictionary_headers_are_rejected():
    with pytest.raises(McstParseError):
        _parse_csv_rows("컬럼명,정의\n이름,시설 이름\n".encode(), "golf_courses_status", None)


def test_html_200_is_not_an_empty_successful_csv():
    with pytest.raises(McstParseError):
        _parse_csv_rows(b"<!doctype html>\n<html>unavailable</html>", "fixture", None)


@pytest.mark.parametrize("encoding", [None, "utf-8", "utf-8-sig"])
def test_golf_extra_columns_remain_available(encoding):
    raw = (COLUMNS + ",새행정코드\n서울,검증골프장,사업자,서울,123,18,일반,11\n").encode(
        "utf-8-sig"
    )
    rows = _parse_csv_rows(raw, "golf_courses_status", encoding)
    assert rows[0]["새행정코드"] == "11"


@pytest.mark.parametrize("redirect_stage", ["page", "metadata", "permission"])
async def test_approval_redirect_never_downloads_before_false_decision(redirect_stage):
    requests = []

    async def handler(request):
        requests.append(request.url.path)
        if request.url.path == "/data/15118920/fileData.do":
            if redirect_stage == "page":
                return httpx.Response(
                    302, headers={"location": FILE + "?atchFileId=FIXTURE&fileDetailSn=1"}
                )
            return httpx.Response(200, text=HTML)
        if request.url.path == META:
            if redirect_stage == "metadata":
                return httpx.Response(
                    303, headers={"location": FILE + "?atchFileId=FIXTURE&fileDetailSn=1"}
                )
            return httpx.Response(200, json=METADATA)
        if request.url.path == LIMIT:
            return httpx.Response(
                307, headers={"location": FILE + "?atchFileId=FIXTURE&fileDetailSn=1"}
            )
        return httpx.Response(200, content=golf_zip())

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler), follow_redirects=True
    ) as session:
        async with FileDataClient(session=session) as client:
            try:
                await client.read_csv("golf_courses_status")
            except Exception as exc:
                captured = exc
            else:
                pytest.fail("approval redirect must fail")
    assert FILE not in requests
    assert isinstance(captured, McstRequestError)
    assert captured.result_code == "FILE_APPROVAL_REDIRECT"


@pytest.mark.parametrize("entrypoint", ["page", "form"])
async def test_non_native_auto_redirect_session_is_rejected_before_sending(entrypoint):
    requests = []

    async def handler(request):
        requests.append(request.url.path)
        if request.url.path == FILE:
            return httpx.Response(200, content=golf_zip())
        return httpx.Response(
            303, headers={"location": FILE + "?atchFileId=FIXTURE&fileDetailSn=1"}
        )

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler), follow_redirects=True
    ) as native:

        class Wrapper:
            async def get(self, url, *, params=None, timeout):
                return await native.get(url, params=params, timeout=timeout)

            async def post(self, url, *, data, timeout):
                return await native.post(url, data=data, timeout=timeout)

        if entrypoint == "page":
            async with FileDataClient(session=Wrapper()) as client:
                with pytest.raises(McstRequestError) as captured:
                    await client.read_csv("golf_courses_status")
            assert captured.value.result_code == "SESSION_REDIRECT_UNSUPPORTED"
        else:
            client = HttpClient(session=Wrapper())
            try:
                with pytest.raises(McstRequestError) as captured:
                    await client.post_form_json(PAGE, {})
                assert captured.value.result_code == "SESSION_POST_UNSUPPORTED"
            finally:
                await client.aclose()
    assert requests == []


@pytest.mark.parametrize("operation", ["close", "cancel"])
async def test_native_post_waiting_for_token_does_not_send_after_close_or_cancel(operation):
    entered, release = asyncio.Event(), asyncio.Event()
    requests = []

    class WaitingBudget:
        async def acquire(self):
            entered.set()
            await release.wait()

    async def handler(request):
        requests.append(request)
        return httpx.Response(200, json={"ok": True})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as native:
        client = HttpClient(session=native, rate_limiter=WaitingBudget())
        task = asyncio.create_task(client.post_form_json(PAGE, {}))
        await asyncio.wait_for(entered.wait(), 1)
        if operation == "close":
            await client.aclose()
            release.set()
            with pytest.raises(RuntimeError, match="closed"):
                await task
        else:
            task.cancel()
            with pytest.raises(asyncio.CancelledError):
                await task
            await client.aclose()
        assert not native.is_closed
    assert requests == []


@pytest.mark.parametrize(
    "metadata",
    [
        [],
        {"status": False},
        {**METADATA, "atchFileId": None},
        {**METADATA, "fileDetailSn": True},
        {**METADATA, "dataSetFileDetailInfo": {"publicDataTyDetailCode": "DATY03", "dataNm": ""}},
    ],
)
async def test_invalid_metadata_never_checks_or_downloads(metadata):
    requests = []

    async def handler(request):
        requests.append(request.url.path)
        if request.url.path == "/data/15118920/fileData.do":
            return httpx.Response(200, text=HTML)
        assert request.url.path == META
        return httpx.Response(200, json=metadata)

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as session:
        async with FileDataClient(session=session) as client:
            with pytest.raises(McstParseError):
                await client.read_csv("golf_courses_status")
    assert requests == ["/data/15118920/fileData.do", META]


async def test_legacy_direct_link_also_checks_permission():
    requests = []
    url = "https://www.data.go.kr" + FILE + "?atchFileId=LEGACY&fileDetailSn=3"

    async def handler(request):
        requests.append(request.url.path)
        if request.url.path == "/data/15118920/fileData.do":
            return httpx.Response(200, text='<script>{"contentUrl":"' + url + '"}</script>')
        if request.url.path == LIMIT:
            assert parse_qs(request.content.decode()) == {
                "atchFileId": ["LEGACY"],
                "fileDetailSn": ["3"],
            }
            return httpx.Response(200, json={"needCaptcha": False})
        assert request.url.path == FILE
        return httpx.Response(200, content=golf_zip())

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as session:
        async with FileDataClient(session=session) as client:
            rows = await client.read_csv("golf_courses_status")
    assert rows[0]["이름"] == "검증골프장"
    assert requests == ["/data/15118920/fileData.do", LIMIT, FILE]


async def test_converted_dataset_uses_public_subject_as_download_name():
    metadata = {
        **METADATA,
        "dataSetFileDetailInfo": {
            "publicDataTyDetailCode": "DATY05",
            "dataNm": None,
            "publicDataSj": "변환 자료",
        },
    }

    async def handler(request):
        if request.url.path == "/data/15118920/fileData.do":
            return httpx.Response(200, text=HTML)
        if request.url.path == META:
            return httpx.Response(200, json=metadata)
        if request.url.path == LIMIT:
            return httpx.Response(200, json={"needCaptcha": False})
        assert request.url.path == FILE
        assert request.url.params["dataNm"] == "변환 자료"
        return httpx.Response(200, content=golf_zip())

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as session:
        async with FileDataClient(session=session) as client:
            assert (await client.read_csv("golf_courses_status"))[0]["이름"] == "검증골프장"


async def test_form_network_failure_is_not_retried_and_redacts_credentials():
    fixture_key = "fixture-form-credential-only"
    requests = []

    async def handler(request):
        requests.append(request)
        raise httpx.ReadError(fixture_key, request=request)

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as session:
        client = HttpClient(session=session, retries=3)
        try:
            with pytest.raises(McstNetworkError) as captured:
                await client.post_form_json(
                    PAGE + "?serviceKey=" + fixture_key,
                    {
                        "serviceKey": fixture_key,
                    },
                )
        finally:
            await client.aclose()
    assert len(requests) == 1
    assert fixture_key not in str(captured.value)
    assert fixture_key not in str(vars(captured.value))
