from __future__ import annotations

import requests

from mcst import CultureOpenApiClient, DataGoFileApiClient


class FailingSession:
    def get(self, url, *, params=None, timeout=10.0):  # noqa: ANN001
        raise requests.ConnectionError(
            "HTTPSConnectionPool(host='api.kcisa.kr', port=443): "
            "Max retries exceeded with url: "
            "/openapi/API_CIA_090/request?serviceKey=abc-123 "
            "(Caused by NameResolutionError(\"getaddrinfo failed\"))"
        )


def test_direct_service_key_is_stripped():
    assert CultureOpenApiClient(service_key="  abc-123  ").service_key == "abc-123"
    assert DataGoFileApiClient(service_key="\n'abc-123'\t").service_key == "abc-123"


def test_network_error_is_classified_and_redacted_in_debug_run():
    client = CultureOpenApiClient(
        service_key="  abc-123  ",
        retries=0,
        session=FailingSession(),
    )

    debug_run = client.debug_request("cafe_bookstores")

    assert debug_run.error
    assert debug_run.error["type"] == "McstNetworkError"
    assert debug_run.error["failure_kind"] == "network"
    assert "DNS lookup failed" in debug_run.error["message"]
    assert "abc-123" not in debug_run.error["message"]
