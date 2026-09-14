from __future__ import annotations

import io
import os
import zipfile

import pytest

from mcst import CultureOpenApiClient, FileDataClient, McstClient
from mcst.catalog import ALL_DATASETS, DatasetKind
from mcst.exceptions import McstAuthError, McstNetworkError

pytestmark = [
    pytest.mark.live,
    pytest.mark.skipif(os.getenv("MCST_RUN_LIVE") != "1", reason="MCST_RUN_LIVE=1 필요"),
]


def _service_key() -> str:
    for name in ("KCISA_SERVICE_KEY", "DATA_GO_KR_SERVICE_KEY"):
        value = os.getenv(name)
        if value:
            return value.strip().strip('"').strip("'")
    pytest.skip("KCISA_SERVICE_KEY 또는 DATA_GO_KR_SERVICE_KEY 미설정")


@pytest.mark.parametrize("slug", ["leisure_classes", "leisure_activity_facilities"])
async def test_live_kcisa(slug):
    key = _service_key()
    async with CultureOpenApiClient(key, timeout=20, retries=0) as client:
        try:
            page = await client.request(slug, num_of_rows=1)
        except (McstAuthError, McstNetworkError) as exc:
            pytest.skip(f"{slug}: {exc}")
    assert page.page_no == 1
    assert page.num_of_rows == 1
    assert page.items
    assert key not in repr(page.raw)


async def test_live_odcloud_public_libraries_and_debug():
    key = os.getenv("DATA_GO_KR_SERVICE_KEY")
    if not key:
        pytest.skip("DATA_GO_KR_SERVICE_KEY 미설정")
    async with McstClient(key, timeout=20, retries=0) as client:
        page = await client.data_go.public_libraries(per_page=1)
        assert page.items
        run = await client.data_go.debug_request("public_libraries", per_page=1)
        assert run.error is None, run.error
        assert run.parsed.items


@pytest.mark.parametrize(
    "slug",
    [
        entry.slug
        for entry in ALL_DATASETS.values()
        if entry.kind in {DatasetKind.FILE_DOWNLOAD, DatasetKind.DATA_GO_FILE_API}
        and entry.slug not in {"public_sports_facilities", "registered_sports_businesses"}
    ],
)
async def test_live_file_csv(slug):
    async with FileDataClient(timeout=30, retries=0) as client:
        rows = await client.read_csv(slug)
    assert rows, f"{slug}: 빈 파일"
    assert len(rows[0]) >= 2, f"{slug}: 복수 CSV 컬럼 없음"
    assert all(
        isinstance(key, str) and not key.lstrip().startswith(("<", "{", "["))
        for key in rows[0]
    ), f"{slug}: CSV 대신 HTML/XML/JSON 오류 본문 또는 잘못된 컬럼 수 수신"


@pytest.mark.parametrize(
    "slug,marker",
    [
        ("public_sports_facilities", "xl/workbook.xml"),
        ("registered_sports_businesses", "Contents/header.xml"),
    ],
)
async def test_live_file_document_download(slug, marker):
    # 실제 원본은 XLSX/HWPX이므로 다운로드 계약과 컨테이너 무결성을 확인한다.
    async with FileDataClient(timeout=30, retries=0) as client:
        data = await client.download(slug)
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        assert marker in archive.namelist()
        assert archive.read(marker)
        assert archive.testzip() is None
