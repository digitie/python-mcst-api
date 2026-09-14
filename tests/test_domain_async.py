"""MCST 모의 서버 기반 도메인/파일 계약 독립 검증."""

import io
import zipfile

import httpx

from mcst import McstClient
from mcst.catalog import CatalogEntry, DatasetKind, SourcePortal
from mcst.exceptions import McstAuthError, McstParseError, McstRateLimitError, McstRequestError
from mcst.models import CultureRecord, Page

CSV = "시설코드,시설명,위도,경도\r\n00001,서울공원,0,127.25\r\n00002,도서관,,\r\n"
FILE_ENTRY = CatalogEntry(
    slug="synthetic",
    title="모의 파일",
    provider="모의 기관",
    kind=DatasetKind.FILE_DOWNLOAD,
    source=SourcePortal.CULTURE_GO_KR,
    detail_url="https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00001&dataType=BATCH",
)


async def test_domain_pagination_and_file_roundtrip(tmp_path):
    calls = []
    mode = "culture"

    async def handler(request):
        calls.append(request)
        query = request.url.params
        if request.url.host == "www.culture.go.kr":
            assert query["fileDataNo"] == "00001" and query["dataType"] == "BATCH"
            return httpx.Response(
                200,
                text="<a onclick=\"fnFileDwld('https://big.kcisa.kr/common/bbsAtchFileDownload.do?fileId=0001&amp;downFileName=문화.csv')\">파일</a>",
            )
        if request.url.host == "big.kcisa.kr":
            assert query["fileId"] == "0001" and query["downFileName"] == "문화.csv"
            if mode == "zip_cp949":
                buf = io.BytesIO()
                with zipfile.ZipFile(buf, "w") as archive:
                    archive.writestr("README.txt", "notice")
                    archive.writestr("자료.CSV", CSV.encode("cp949"))
                return httpx.Response(200, content=buf.getvalue())
            if mode == "zip_no_csv":
                buf = io.BytesIO()
                with zipfile.ZipFile(buf, "w") as archive:
                    archive.writestr("README.txt", "notice")
                return httpx.Response(200, content=buf.getvalue())
            return httpx.Response(200, content=CSV.encode("utf-8-sig"))
        if mode.startswith("error_"):
            code = mode[6:]
            return httpx.Response(
                200,
                json={
                    "response": {
                        "header": {
                            "resultCode": code,
                            "resultMsg": {
                                "03": "NO_DATA",
                                "22": "LIMIT_ERROR",
                                "30": "AUTH_ERROR",
                                "12": "INVALID_REQUEST",
                            }.get(code, "FAIL"),
                        },
                        "body": {"items": "", "totalCount": 0},
                    }
                },
            )
        page = int(query.get("pageNo", query.get("page", "1")))
        rows = [
            {
                "title": "시설" + str(n),
                "address": "서울",
                "tel": "00102",
                "longitude": "127.25",
                "latitude": "0",
                "code": f"{n:05}",
            }
            for n in range((page - 1) * 2 + 1, page * 2 + 1)
        ]
        if request.url.host == "api.odcloud.kr":
            return httpx.Response(200, json={"data": rows, "totalCount": 4})
        if mode == "repeat":
            rows = [{"title": "같은 시설", "code": "00001"}]
        return httpx.Response(
            200,
            json={
                "response": {
                    "header": {"resultCode": "00", "resultMsg": "OK"},
                    "body": {"items": {"item": rows}, "totalCount": 10 if mode == "repeat" else 4},
                }
            },
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as session:
        async with McstClient(
            "default-synthetic",
            service_keys={
                "cafe_bookstores": "cafe-synthetic",
                "public_libraries": "library-synthetic",
            },
            session=session,
            max_rps=100000,
        ) as client:
            page = await client.culture.cafe_bookstores(
                page_no=1, num_of_rows=2, keyword="서울", params={"custom": "0007"}
            )
            assert (
                isinstance(page, Page)
                and isinstance(page.items, tuple)
                and isinstance(page.items[0], CultureRecord)
            )
            assert (
                page.items[0].latitude == 0
                and page.items[0].longitude == 127.25
                and page.items[0].tel == "00102"
            )
            assert page.items[0].raw["code"] == "00001"
            assert calls[-1].url.params["serviceKey"] == "cafe-synthetic"
            assert (
                calls[-1].url.params["custom"] == "0007"
                and calls[-1].url.params["keyword"] == "서울"
            )
            await client.culture.used_bookstores(
                params={"serviceKey": "override-synthetic"}, num_of_rows=2
            )
            assert calls[-1].url.params["serviceKey"] == "override-synthetic"
            await client.data_go.public_libraries(per_page=2, params={"cond[지역::EQ]": "서울"})
            assert (
                calls[-1].url.params["serviceKey"] == "library-synthetic"
                and calls[-1].url.params["cond[지역::EQ]"] == "서울"
            )
            items = [
                item
                async for item in client.culture.iter_items(
                    "cafe_bookstores", num_of_rows=2, max_items=3
                )
            ]
            assert [item.raw["code"] for item in items] == ["00001", "00002", "00003"]
            rows = [
                row
                async for row in client.data_go.iter_items(
                    "public_libraries", per_page=2, max_pages=2
                )
            ]
            assert [row["code"] for row in rows] == ["00001", "00002", "00003", "00004"]
            mode = "repeat"
            before = len(calls)
            rows = [
                row
                async for row in client.culture.iter_items(
                    "cafe_bookstores", num_of_rows=2, max_pages=9
                )
            ]
            assert len(rows) == 1 and len(calls) == before + 2
            print("PER_DATASET_KEYS_PARAMS_MODELS_PAGINATION_REPEAT_PASS")
            for code, exc_type in [
                ("03", None),
                ("22", McstRateLimitError),
                ("30", McstAuthError),
                ("12", McstRequestError),
            ]:
                mode = "error_" + code
                before = len(calls)
                if exc_type is None:
                    assert not (await client.culture.cafe_bookstores()).items
                else:
                    try:
                        await client.culture.cafe_bookstores()
                    except exc_type as exc:
                        assert exc.result_code == code
                    else:
                        raise AssertionError(code)
                assert len(calls) == before + 1
            mode = "culture"
            run = await client.debug_fetch("cafe_bookstores", num_of_rows=2)
            assert (
                run.error is None
                and isinstance(run.parsed, Page)
                and isinstance(run.parsed.items, tuple)
            )
            assert run.processed["items"][0]["latitude"] == 0
            assert run.request["query"]["serviceKey"] == "<REDACTED>"
            print("NODATA_PROVIDER_ERRORS_DEBUGRUN_SHAPE_PASS")
            for mode in ["utf8_bom", "zip_cp949"]:  # noqa: B007 - 모의 전송 함수가 클로저로 읽는다.
                before = len(calls)
                rows = await client.file_data.read_csv(FILE_ENTRY)
                assert rows == [
                    {"시설코드": "00001", "시설명": "서울공원", "위도": "0", "경도": "127.25"},
                    {"시설코드": "00002", "시설명": "도서관", "위도": "", "경도": ""},
                ]
                assert len(calls) == before + 2
                iterated = [row async for row in client.file_data.iter_csv(FILE_ENTRY)]
                assert iterated == rows
            mode = "zip_no_csv"
            try:
                await client.file_data.read_csv(FILE_ENTRY)
            except McstParseError:
                pass
            else:
                raise AssertionError("no CSV archive accepted")
            mode = "utf8_bom"
            target = tmp_path / "domain.csv"
            await client.file_data.save(FILE_ENTRY, target)
            assert target.read_bytes() == CSV.encode("utf-8-sig")
            before = len(calls)
            try:
                await client.file_data.save(FILE_ENTRY, target)
            except FileExistsError:
                pass
            else:
                raise AssertionError("overwrite=False ignored")
            assert len(calls) == before
            print("DOWNLOAD_QUERY_ZIP_CP949_UTF8BOM_CSV_SAVE_ITER_PASS")
        assert not session.is_closed
    print("ALL_DOMAIN_PASS", len(calls), "mock requests")
