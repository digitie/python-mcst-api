"""MCST 읽기 전용 독립 MockTransport 회귀 검증."""

from __future__ import annotations

import asyncio
import hashlib
import hmac
import threading
from urllib.parse import parse_qsl, quote

import httpx
import pytest

from mcst import CultureOpenApiClient, FileDataClient, McstClient
from mcst._file_io import run_file_io
from mcst._http import HttpClient
from mcst.catalog import CatalogEntry, DatasetKind, SourcePortal


class Budget:
    def __init__(self):
        self.count = 0

    async def acquire(self):
        self.count += 1


def file_entry():
    return CatalogEntry(
        slug="mock_file",
        title="mock",
        provider="mock",
        kind=DatasetKind.FILE_DOWNLOAD,
        source=SourcePortal.CULTURE_GO_KR,
        detail_url="https://download.test/page",
        file_url="https://download.test/data.csv",
    )


def signature_for_wire(request):
    auth = request.headers["authorization"]
    credential = auth.split("Credential=", 1)[1].split(",", 1)[0]
    _, scope = credential.split("/", 1)
    date, region, service, terminal = scope.split("/")
    names = auth.split("SignedHeaders=", 1)[1].split(",", 1)[0]
    raw_path = request.url.raw_path.split(b"?", 1)[0].decode("ascii")
    pairs = [
        (quote(k, safe="-_.~"), quote(v, safe="-_.~"))
        for k, v in parse_qsl(request.url.query.decode(), keep_blank_values=True)
    ]
    query = "&".join(f"{k}={v}" for k, v in sorted(pairs))
    headers = "".join(
        f"{name}:{' '.join(request.headers[name].split())}\n" for name in names.split(";")
    )
    payload = hashlib.sha256(request.content).hexdigest()
    assert payload == request.headers["x-amz-content-sha256"]
    canonical = "\n".join([request.method, raw_path, query, headers, names, payload])
    string_to_sign = "\n".join(
        [
            "AWS4-HMAC-SHA256",
            request.headers["x-amz-date"],
            scope,
            hashlib.sha256(canonical.encode()).hexdigest(),
        ]
    )
    key = b"AWS4mock-secret"
    for value in (date, region, service, terminal):
        key = hmac.new(key, value.encode(), hashlib.sha256).digest()
    return hmac.new(key, string_to_sign.encode(), hashlib.sha256).hexdigest()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "endpoint,object_key,defaults",
    [
        ("https://storage.test", "folder/한 글+.csv", {}),
        ("https://storage.test/prefix", "normal.csv", {"tenant": "mock"}),
        ("https://storage.test/한 글", "normal.csv", {}),
    ],
)
async def test_public_rustfs_signature_matches_actual_wire(
    tmp_path, endpoint, object_key, defaults
):
    requests = []

    async def handler(request):
        requests.append(request)
        if request.method == "GET":
            return httpx.Response(200, content=b"column\nvalue\n")
        assert request.headers["authorization"].split("Signature=", 1)[1] == signature_for_wire(
            request
        )
        return httpx.Response(200)

    budget = Budget()
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler), params=defaults
    ) as session:
        async with FileDataClient(session=session, rate_limiter=budget) as client:
            await client.save_rustfs(
                file_entry(),
                tmp_path / "local.csv",
                bucket="bucket",
                object_key=object_key,
                endpoint_url=endpoint,
                region_name="us-east-1",
                access_key_id="mock-access",
                secret_access_key="mock-secret",
            )
        assert not session.is_closed
    assert len(requests) == budget.count == 3


@pytest.mark.asyncio
async def test_file_worker_repeated_cancel_drains_and_preserves_first_cancel():
    started, release, finished = threading.Event(), threading.Event(), threading.Event()

    def worker():
        started.set()
        release.wait(10)
        finished.set()
        raise ValueError("worker failed after cancellation")

    task = asyncio.create_task(run_file_io(worker))
    await asyncio.to_thread(started.wait, 5)
    task.cancel("first")
    await asyncio.sleep(0)
    task.cancel("second")
    await asyncio.sleep(0)
    assert not task.done()
    release.set()
    with pytest.raises(asyncio.CancelledError, match="first"):
        await task
    assert finished.is_set()


def culture_entry():
    return CatalogEntry(
        slug="mock_culture",
        title="mock",
        provider="mock",
        kind=DatasetKind.KCISA_OPEN_API,
        source=SourcePortal.CULTURE_GO_KR,
        detail_url="https://culture.test/detail",
        endpoint_url="https://culture.test/request",
    )


def odcloud_entry():
    return CatalogEntry(
        slug="mock_odcloud",
        title="mock",
        provider="mock",
        kind=DatasetKind.DATA_GO_FILE_API,
        source=SourcePortal.DATA_GO_KR,
        detail_url="https://odcloud.test/detail",
        public_data_pk="123",
        public_data_detail_pk="abc",
    )


def culture_payload(name="record"):
    return {
        "response": {
            "header": {"resultCode": "00"},
            "body": {"items": [{"title": name}], "totalCount": 1},
        }
    }


def test_from_env_retains_name_and_fallback_names(monkeypatch):
    monkeypatch.setenv("MCST_REVIEW_ONLY_KEY", "'mock-selected'")
    monkeypatch.setenv("MCST_REVIEW_ONLY_FALLBACK", '"mock-fallback"')
    assert (
        CultureOpenApiClient.from_env("MCST_REVIEW_ONLY_KEY", fallback_names=()).service_key
        == "mock-selected"
    )
    monkeypatch.delenv("MCST_REVIEW_ONLY_KEY")
    assert (
        CultureOpenApiClient.from_env(
            name="MCST_REVIEW_ONLY_KEY", fallback_names=("MCST_REVIEW_ONLY_FALLBACK",)
        ).service_key
        == "mock-fallback"
    )


@pytest.mark.asyncio
async def test_all_providers_share_retry_redirect_and_put_budget(monkeypatch, tmp_path):
    import mcst._http as http_module

    async def no_sleep(*args):
        pass

    monkeypatch.setattr(http_module, "_sleep_before_retry", no_sleep)
    sent, culture_calls = [], 0

    async def handler(request):
        nonlocal culture_calls
        sent.append(request)
        if request.method == "PUT":
            assert request.headers["authorization"].split("Signature=", 1)[1] == signature_for_wire(
                request
            )
            return httpx.Response(200)
        if request.url.host == "culture.test":
            culture_calls += 1
            if culture_calls == 1:
                return httpx.Response(503)
            if culture_calls == 2:
                raise httpx.ConnectError("mock", request=request)
            if culture_calls == 3:
                return httpx.Response(302, headers={"location": "/final"})
            return httpx.Response(200, json=culture_payload())
        if request.url.host == "api.odcloud.kr":
            return httpx.Response(200, json={"data": [{"name": "record"}], "totalCount": 1})
        return httpx.Response(200, content=b"column\nvalue\n")

    budget = Budget()
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler), follow_redirects=True
    ) as session:
        async with McstClient(
            service_key="mock-key", session=session, rate_limiter=budget
        ) as client:
            assert (
                client.culture.rate_limiter
                is client.data_go.rate_limiter
                is client.file_data.rate_limiter
                is budget
            )
            assert (await client.culture.request(culture_entry())).items
            assert (await client.data_go.request(odcloud_entry())).items
            await client.file_data.save_rustfs(
                file_entry(),
                tmp_path / "saved.csv",
                bucket="bucket",
                endpoint_url="https://storage.test",
                region_name="us-east-1",
                access_key_id="mock-access",
                secret_access_key="mock-secret",
            )
        assert not session.is_closed
    assert budget.count == len(sent) == 8


class Gate(Budget):
    def __init__(self, block_at):
        super().__init__()
        self.block_at = block_at
        self.entered, self.release = asyncio.Event(), asyncio.Event()

    async def acquire(self):
        await super().acquire()
        if self.count == self.block_at:
            self.entered.set()
            await self.release.wait()


@pytest.mark.asyncio
@pytest.mark.parametrize("when", [1, 2])
@pytest.mark.parametrize("action", ["close", "auth", "cancel"])
async def test_token_wait_prevents_send_after_close_auth_or_cancel(when, action):
    sent, responses = [], []

    async def handler(request):
        sent.append(request)
        response = (
            httpx.Response(302, headers={"location": "/final"})
            if len(sent) == 1
            else httpx.Response(200)
        )
        responses.append(response)
        return response

    budget = Gate(when)
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler), follow_redirects=True
    ) as session:
        client = HttpClient(session=session, rate_limiter=budget)
        task = asyncio.create_task(client.get_response("https://mock.test/start"))
        await budget.entered.wait()
        if action == "close":
            await client.aclose()
            expected = RuntimeError
        elif action == "auth":
            session.auth = httpx.DigestAuth("mock", "mock")
            expected = TypeError
        else:
            task.cancel()
            expected = asyncio.CancelledError
        budget.release.set()
        with pytest.raises(expected):
            await task
        assert len(sent) == when - 1
        assert all(response.is_closed for response in responses)


@pytest.mark.asyncio
@pytest.mark.parametrize("status", [307, 500])
async def test_rustfs_error_closes_response_and_never_redirects(tmp_path, status):
    sent, responses = [], []

    async def handler(request):
        sent.append(request)
        response = (
            httpx.Response(status, headers={"location": "https://wrong.test"})
            if request.method == "PUT"
            else httpx.Response(200, content=b"name\nmock\n")
        )
        responses.append(response)
        return response

    budget = Budget()
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler), follow_redirects=True
    ) as session:
        async with FileDataClient(session=session, rate_limiter=budget) as client:
            with pytest.raises(RuntimeError, match=str(status)):
                await client.save_rustfs(
                    file_entry(),
                    tmp_path / "saved.csv",
                    bucket="bucket",
                    endpoint_url="https://storage.test",
                    region_name="us-east-1",
                    access_key_id="mock-access",
                    secret_access_key="mock-secret",
                )
    assert len(sent) == budget.count == 3
    assert all(response.is_closed for response in responses)


@pytest.mark.asyncio
async def test_owned_sessions_are_lazy_reused_and_all_closed(monkeypatch):
    import mcst._http as http_module

    pools = []

    async def handler(request):
        if request.url.host == "culture.test":
            return httpx.Response(200, json=culture_payload())
        if request.url.host == "api.odcloud.kr":
            return httpx.Response(200, json={"data": [{"name": "record"}], "totalCount": 1})
        return httpx.Response(200, content=b"name\nmock\n")

    def build():
        pool = httpx.AsyncClient(transport=httpx.MockTransport(handler))
        pools.append(pool)
        return pool

    monkeypatch.setattr(http_module, "build_session", build)
    async with McstClient(service_key="mock-key", max_rps=100) as client:
        assert not pools
        await client.culture.request(culture_entry())
        await client.culture.request(culture_entry())
        assert len(pools) == 1
        await client.data_go.request(odcloud_entry())
        await client.file_data.read_csv(file_entry())
        assert len(pools) == 3
    assert all(pool.is_closed for pool in pools)


@pytest.mark.asyncio
async def test_concurrent_debug_has_isolated_success_and_failure():
    entered = 0
    ready = asyncio.Event()

    async def handler(request):
        nonlocal entered
        entered += 1
        if entered == 2:
            ready.set()
        await ready.wait()
        marker = request.url.params["keyword"]
        if marker == "beta":
            return httpx.Response(403, text="beta mock-key")
        return httpx.Response(200, json=culture_payload(marker))

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as session:
        async with CultureOpenApiClient(service_key="mock-key", session=session) as client:
            alpha, beta = await asyncio.gather(
                client.debug_request(culture_entry(), keyword="alpha"),
                client.debug_request(culture_entry(), keyword="beta"),
            )
    assert alpha.parsed.items[0].name == "alpha"
    assert alpha.error is None and beta.error
    assert alpha.input["keyword"] == "alpha" and beta.input["keyword"] == "beta"
    assert "mock-key" not in str(alpha) + str(beta)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "endpoint,key",
    [
        ("https://storage.test", "folder/../normal.csv"),
        ("https://storage.test", "folder/./normal.csv"),
        ("https://storage.test/../prefix", "normal.csv"),
        ("https://storage.test/%2E%2E/prefix", "normal.csv"),
    ],
)
async def test_dot_segments_fail_before_download_or_budget(tmp_path, endpoint, key):
    sent = []

    async def handler(request):
        sent.append(request)
        return httpx.Response(200)

    budget = Budget()
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as session:
        async with FileDataClient(session=session, rate_limiter=budget) as client:
            with pytest.raises(ValueError):
                await client.save_rustfs(
                    file_entry(),
                    tmp_path / "saved.csv",
                    bucket="bucket",
                    object_key=key,
                    endpoint_url=endpoint,
                    region_name="us-east-1",
                    access_key_id="mock-access",
                    secret_access_key="mock-secret",
                )
    assert budget.count == len(sent) == 0
    assert not (tmp_path / "saved.csv").exists()


@pytest.mark.asyncio
@pytest.mark.parametrize("method", ["GET", "PUT"])
async def test_cancel_while_consuming_body_closes_stream(tmp_path, method):
    started, closed = asyncio.Event(), asyncio.Event()

    class Stream(httpx.AsyncByteStream):
        async def __aiter__(self):
            started.set()
            await asyncio.Event().wait()
            yield b"never"

        async def aclose(self):
            closed.set()

    async def handler(request):
        if method == "PUT" and request.method == "GET":
            return httpx.Response(200, content=b"name\nmock\n")
        return httpx.Response(200, stream=Stream())

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as session:
        async with FileDataClient(session=session, max_rps=100) as client:
            if method == "GET":
                task = asyncio.create_task(client.download(file_entry()))
            else:
                task = asyncio.create_task(
                    client.save_rustfs(
                        file_entry(),
                        tmp_path / "saved.csv",
                        bucket="bucket",
                        endpoint_url="https://storage.test",
                        region_name="us-east-1",
                        access_key_id="mock-access",
                        secret_access_key="mock-secret",
                    )
                )
            await started.wait()
            task.cancel()
            with pytest.raises(asyncio.CancelledError):
                await task
            assert closed.is_set()


@pytest.mark.asyncio
@pytest.mark.parametrize("action", ["close", "cancel"])
async def test_rustfs_put_wait_checks_close_and_cancel(tmp_path, action):
    sent = []

    async def handler(request):
        sent.append(request)
        return httpx.Response(200, content=b"name\nmock\n")

    budget = Gate(3)
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as session:
        async with FileDataClient(session=session, rate_limiter=budget) as client:
            task = asyncio.create_task(
                client.save_rustfs(
                    file_entry(),
                    tmp_path / "saved.csv",
                    bucket="bucket",
                    endpoint_url="https://storage.test",
                    region_name="us-east-1",
                    access_key_id="mock-access",
                    secret_access_key="mock-secret",
                )
            )
            await budget.entered.wait()
            if action == "close":
                await client.aclose()
                expected = RuntimeError
            else:
                task.cancel()
                expected = asyncio.CancelledError
            budget.release.set()
            with pytest.raises(expected):
                await task
            assert len(sent) == 2 and all(request.method == "GET" for request in sent)
