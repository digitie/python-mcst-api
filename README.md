# python-mcst-api

![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)
![GPL-3.0-or-later 라이선스](https://img.shields.io/badge/License-GPL--3.0--or--later-blue.svg)
![Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)

`python-mcst-api`는 문화체육관광부 및 산하기관의 공개 데이터 중 여행, 여가, 숙박, 문화시설, 도서관 위치/운영 정보에 맞춘 비공식 Python 클라이언트입니다. `mcst.catalog`에 등록된 데이터셋별로 KCISA OpenAPI, 공공데이터포털(data.go.kr) 자동변환 API, 파일 다운로드를 비동기 전용 typed client와 Pydantic 응답 모델로 감쌉니다.

한국관광공사 제공 서비스, 행정안전부/지자체 단독 제공 자료, 도서관 소장자료/서지/ISBN/추천도서 데이터는 제외했습니다.

현재 구현 상태와 최근 변경 사항은 [CHANGELOG.md](CHANGELOG.md)의 `[Unreleased]` 절을 참고하십시오.

## 제공 표면

| 표면 | 진입점 | 설명 |
| --- | --- | --- |
| 비동기 클라이언트 | `McstClient` | KCISA OpenAPI, data.go.kr 자동변환, 파일 다운로드를 하나로 묶은 편의 클라이언트 |
| 카탈로그 조회 | `get_api_catalog()` / `get_api_catalog_entry()` | 지원 데이터셋을 사람이 읽을 수 있는 라벨, endpoint, 파라미터 메타데이터로 JSON 직렬화 |
| 디버그 fixture 저장 | `McstClient.debug_fetch()` / `debug_request()` / `save_fixture()` | 카탈로그 `kind`로 라우팅되는 제네릭 디버그 실행 결과를 fixture로 저장해 오프라인 replay 테스트에 재사용 |

## 먼저 읽을 문서

| 필요한 정보 | 문서 |
| --- | --- |
| 지원 데이터셋 전체 목록과 포함/제외 기준 | [docs/catalog.md](docs/catalog.md) |
| culture.go.kr 전체 API/파일데이터 조사표(확장 대상) | [docs/culture-go-kr-full-catalog.md](docs/culture-go-kr-full-catalog.md) |
| 디버그 UI fixture 구조와 replay 테스트 방식 | [docs/debug-fixtures.md](docs/debug-fixtures.md) |
| 패키지 아키텍처와 모듈 의존 방향 | [docs/architecture.md](docs/architecture.md) |
| 로컬 개발 환경 구성과 품질 검증 도구 | [docs/dev-environment.md](docs/dev-environment.md) |
| 의사결정 기록(ADR) | [docs/decisions.md](docs/decisions.md) |
| 프로젝트 진행 상태 요약 | [docs/resume.md](docs/resume.md) |
| 작업 일지 | [docs/journal.md](docs/journal.md) |
| 작업 백로그 | [docs/tasks.md](docs/tasks.md) |

## 설치

배포 패키지 이름은 `python-mcst-api`이고, Python 코드에서 사용하는 import 이름은 `mcst`입니다.

```bash
pip install -e .[dev]
```

## 개발 환경 메모

이 저장소의 Windows 작업 환경에서는 `rg.exe`가 권한 문제로 실행되지 않을 수 있습니다. 검색이 필요하면 PowerShell의 `Get-ChildItem -Recurse -File`과 `Select-String`을 사용합니다.

문서는 UTF-8로 저장합니다. PowerShell에서 한글이 깨져 보이면 `Get-Content -Encoding UTF8`로 읽고, 스크립트 출력에는 필요에 따라 `$OutputEncoding`과 `[Console]::OutputEncoding`을 UTF-8로 지정합니다.

## 인증키

KCISA OpenAPI와 공공데이터포털 자동변환 API는 서비스키가 필요합니다.
직접 전달하거나 UI에 붙여넣은 키는 앞뒤 공백과 감싸는 따옴표를 제거한 뒤
요청 파라미터에 넣습니다.
문체부/KCISA API는 API별 활용 신청 상태가 다를 수 있으므로 slug별 키도
전달할 수 있습니다.

```powershell
$env:DATA_GO_KR_SERVICE_KEY="..."
```

`api.kcisa.kr`는 data.go.kr 발급 키가 아닌 KCISA 전용 키가 필요하므로,
문체부/KCISA API는 `KCISA_SERVICE_KEY`를 우선 읽고 `DATA_GO_KR_SERVICE_KEY`는
fallback으로만 사용합니다(대부분 인증에 실패합니다).

- `KCISA_SERVICE_KEY` (우선)
- `DATA_GO_KR_SERVICE_KEY` (fallback)

## 빠른 사용

문화·도서관 자료의 기본 수급 경로는 서비스키가 필요 없는 CSV 파일 다운로드입니다.
상세페이지에서 현재 파일 URL을 해석한 다음 다운로드합니다.

```python
import asyncio
from mcst import McstClient


async def main():
    async with McstClient(max_rps=5) as client:
        rows = await client.file_data.read_csv("cafe_bookstores_csv")
        print(len(rows), rows[:1])
        async for row in client.file_data.iter_csv("public_libraries"):
            print(row)
            break


if __name__ == "__main__":
    asyncio.run(main())
```

## 비동기 API 및 TPS 설정

`McstClient`, `CultureOpenApiClient`, `DataGoFileApiClient`, `FileDataClient`는
비동기 전용입니다. 네트워크 호출은 `await`, 페이지/CSV 순회는 `async for`,
수명 관리는 `async with` 또는 `await client.aclose()`를 사용합니다.
이전 `Async*` 클래스, `.aio()`, `adebug_fetch()`, 동기 컨텍스트/`close()`는 제거했습니다.
카탈로그 조회, 모델 변환, `save_fixture()` 같은 로컬 도구는 동기 함수입니다.

KCISA 전용 키와 ODCloud 활용 신청이 준비된 환경에서 다음 예제를 사용합니다.
`KCISA_SERVICE_KEY`와 `DATA_GO_KR_SERVICE_KEY`를 각각 읽으며,
`service_keys={"cafe_bookstores": "..."}`처럼 데이터셋별 키도 지정할 수 있습니다.

```python
import asyncio
from mcst import AsyncTokenBucket, McstClient


async def main():
    bucket = AsyncTokenBucket(max_rps=2, capacity=1)
    async with McstClient(rate_limiter=bucket) as client:
        page = await client.culture.cafe_bookstores(num_of_rows=10)
        print(page.total_count, page.items)
        libraries = await client.data_go.public_libraries(per_page=5)
        print(libraries.items)


if __name__ == "__main__":
    asyncio.run(main())
```

기본값은 초당 5개 토큰, 초기 버스트 5개입니다. `capacity=1`은 초기 버스트를
1개로 제한합니다. `max_rps`는 유한한 양수, `capacity`는 1 이상이어야 합니다.
`rate_limiter`를 주입하면 그 버킷의 설정을 사용합니다. 하나의 `McstClient` 안에서
culture·ODCloud·파일 클라이언트가 같은 버킷을 공유합니다. 여러 클라이언트에도
같은 버킷을 주입할 수 있으며, 사용 범위는 하나의 이벤트 루프입니다.
최초 요청, 각 재시도, 각 리디렉션, 파일 상세페이지/다운로드 GET, RustFS PUT마다
한 토큰을 소비합니다. 재시도 대기도 `asyncio.sleep`을 사용합니다.

내부 HTTPX 세션은 첫 요청 때 생성하고 종료 시 닫습니다. 주입한 비동기 세션은
호출자가 닫습니다. 자동 추가 요청을 만들 수 있는 Digest/custom Auth는 거부하며
기본 인증 또는 인증 없는 세션을 지원합니다. 사용자 정의 전송 계층의 자체 재시도는
비활성화해야 라이브러리가 실제 송신 전체의 TPS를 제어할 수 있습니다.

파일 쓰기·ZIP/CSV 파싱은 작업 스레드에서 실행합니다. 취소 시 시작된 파일 작업이
끝난 뒤 취소를 전파하므로 반환 후 파일이 계속 변경되지 않습니다. `iter_csv`는
전체 다운로드와 파싱 후 행을 순회하며 네트워크 스트리밍 API가 아닙니다.

### 로컬 및 RustFS 저장

`await client.file_data.save(dataset, path)`와
`await client.file_data.save_rustfs(dataset, path, bucket=..., object_key=...)`를 제공합니다.
기본 `overwrite=False`이며 기존 파일을 덮어쓰지 않습니다.
RustFS는 다운로드와 같은 버킷을 사용해 네이티브 HTTPX SigV4 PUT을 보냅니다.
PUT은 자동 재시도하거나 리디렉션하지 않습니다. 업로드 실패 시 먼저 저장한 로컬 파일은 남습니다.
객체 키와 endpoint의 독립된 `.`/`..` 경로 조각은 요청 전에 거부합니다.
RustFS용 주입 세션은 `httpx.AsyncClient`이어야 합니다.

접속 정보는 명시적 인자를 우선하며 기존 `MCST_RUSTFS_*`, `RUSTFS_*`,
`KRTOUR_MAP_OBJECT_STORE_*`, `AWS_*` 환경 변수 폴백을 유지합니다.
access key와 secret key를 지정해야 합니다. `boto3`는 사용하지 않으며
AWS profile/IMDS의 암묵적 자격증명 탐색은 지원하지 않습니다.

## 디버그 fixture 저장 (예제)

별도 Web UI나 로컬 디버그 도구는 라이브러리에 Streamlit을 직접 의존시키지 않고
`debug_request()` 결과를 fixture로 저장하는 방식으로 연결합니다. 저장된 fixture는
외부 API를 다시 호출하지 않고 raw response를 replay해 회귀 테스트에 사용합니다.

```python
import asyncio
from mcst import CultureOpenApiClient, save_fixture


async def main():
    async with CultureOpenApiClient.from_env() as client:
        run = await client.debug_request("leisure_activity_facilities", num_of_rows=5)
    path = save_fixture(run, base_dir="tests/fixtures", case_name="leisure_activity_normal",
                        description="여가 활동 시설 조회 결과", overwrite=False)
    print(path)


if __name__ == "__main__":
    asyncio.run(main())
```

이 예제는 로컬 디버그와 오프라인 회귀 테스트 fixture 생성만을 대상으로 하며, 프로덕션 모니터링이나 배치 수집 용도로는 검증되지 않았습니다.

fixture에는 `input`, `request`, `response`, `parsed`, `processed`, `assertion`, `meta`가
저장됩니다. `serviceKey`, `Authorization`, `api_key`, token 계열 값은 저장 전에
`<REDACTED>`로 마스킹됩니다.

저장된 fixture는 기본 테스트에서 자동으로 읽습니다.

```bash
python -m pytest tests/test_generated_fixtures.py
```

로컬에서 기본 Streamlit 디버그 UI를 실행하려면 다음 명령을 사용합니다.

```bash
pip install -e ".[debug-ui]"
python -m streamlit run examples/streamlit_debug_ui.py
```

Debug Trace 탭은 선택한 데이터셋의 카탈로그 항목을 함께 보여줍니다. 예를 들어
`cafe_bookstores`는 `한국문화정보원_카페가 있는 서점데이터`로 표시됩니다.
Service key 입력칸은 선택한 API마다 별도로 유지되며, 실행 시 현재 선택한
API의 키만 요청에 사용합니다.

## 주요 카탈로그

문화 CSV와 공공도서관 CSV를 기본 경로로 사용합니다. KCISA OpenAPI,
ODCloud 식별자를 가진 파일 API, 다운로드 데이터, 외부 링크의 구분과
전체 항목은 [지원 데이터 카탈로그](docs/catalog.md)를 참고하십시오.
`get_api_catalog()`는 현재 코드와 일치하는 전체 목록을 반환합니다.

## 검증

```bash
python -m pytest
python -m ruff check .
python -m mypy src/mcst
```

### 라이브 테스트

```powershell
$env:MCST_RUN_LIVE = "1"
python -m pytest -m live
```

현재 네트워크에서 `api.kcisa.kr` DNS가 막혀 있거나, 서비스키가 ODCloud에 등록되어 있지 않으면 해당 live test는 실패 대신 skip 처리합니다. `MCST_RUN_LIVE=1` 없이 실행한 테스트는 외부 서비스를 호출하지 않습니다. skip은 실제 데이터 조회 성공을 뜻하지 않습니다.

## 데이터/외부 API 출처

- [문화공공데이터광장(culture.go.kr)](https://www.culture.go.kr/data/) — OpenAPI 및 파일데이터
- [한국문화정보원(KCISA) OpenAPI](https://www.kcisa.kr/) — `api.kcisa.kr`
- [공공데이터포털(data.go.kr)](https://www.data.go.kr/) — ODCloud 자동변환 API 및 파일데이터

## 디렉터리 개요

| 경로 | 설명 |
| --- | --- |
| `src/mcst/` | 라이브러리 소스 코드 (catalog, HTTP 엔진, 클라이언트, 모델, 예외) |
| `tests/` | pytest 테스트 스위트 (오프라인 replay 테스트 + `@pytest.mark.live`) |
| `docs/` | 설계, 카탈로그, 의사결정 기록(ADR), 작업 일지 |
| `examples/` | 로컬 Streamlit 디버그 UI(`streamlit_debug_ui.py`, `debug-ui` extra로만 설치, 라이브러리 본체는 미의존) |

## 문서/기여 규칙

- 모든 문서는 한글로 작성합니다. 코드 식별자, 명령어, URL, 환경 변수명, 공식 데이터셋명 등 원문 유지가 필요한 값만 예외입니다.
- 공개 API 또는 지원 카탈로그가 바뀌면 같은 패치에서 관련 문서(`README.md`, `docs/catalog.md`)와 테스트를 함께 갱신합니다.
- 작업 전 [AGENTS.md](AGENTS.md)의 범위 규칙과 DO NOT 목록을 확인합니다.
- API 키는 커밋, 로그, 예외 메시지, 문서, 테스트 출력 어디에도 노출하지 않습니다.

## 법적 고지

이 저장소의 라이선스(GPL-3.0-or-later, [LICENSE](LICENSE))는 이 저장소에 포함된 코드에만 적용됩니다. 이 라이브러리가 감싸는 문화체육관광부·KCISA·공공데이터포털의 데이터와 API는 각 제공기관의 이용약관과 라이선스를 따르며, 이 프로젝트는 해당 데이터의 정확성·최신성이나 API의 가용성에 대해 어떠한 법적 효력이나 보증도 제공하지 않습니다. 실제 서비스에 사용하기 전에 제공기관의 활용 신청 절차와 이용약관을 직접 확인하십시오.
