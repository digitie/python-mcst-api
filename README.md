# python-mcst-api

![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)
![GPL-3.0-or-later 라이선스](https://img.shields.io/badge/License-GPL--3.0--or--later-blue.svg)
![Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)

`python-mcst-api`는 문화체육관광부 및 산하기관의 공개 데이터 중 여행, 여가, 숙박, 문화시설, 도서관 위치/운영 정보에 맞춘 비공식 Python 클라이언트입니다. `mcst.catalog`에 등록된 데이터셋별로 KCISA OpenAPI, 공공데이터포털(data.go.kr) 자동변환 API, 파일 다운로드를 동기/비동기 typed client와 Pydantic 응답 모델로 감쌉니다.

한국관광공사 제공 서비스, 행정안전부/지자체 단독 제공 자료, 도서관 소장자료/서지/ISBN/추천도서 데이터는 제외했습니다.

현재 구현 상태와 최근 변경 사항은 [CHANGELOG.md](CHANGELOG.md)의 `[Unreleased]` 절을 참고하십시오.

## 제공 표면

| 표면 | 진입점 | 설명 |
| --- | --- | --- |
| 동기 클라이언트 | `McstClient` | KCISA OpenAPI, data.go.kr 자동변환, 파일 다운로드를 하나로 묶은 편의 클라이언트 |
| 비동기 클라이언트 | `McstClient.aio()` | 동일 기능을 제공하는 `httpx.AsyncClient` 기반 비동기 클라이언트 |
| 카탈로그 조회 | `get_api_catalog()` | 지원 데이터셋을 사람이 읽을 수 있는 라벨과 endpoint로 JSON 직렬화 |
| 디버그 fixture 저장 | `debug_request()` / `save_fixture()` | 실제 응답을 fixture로 저장해 오프라인 replay 테스트에 재사용 |

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

```python
from mcst import DatasetKind, McstClient, get_api_catalog

with McstClient(
    service_keys={
        "cafe_bookstores": "...",
        "leisure_activity_facilities": "...",
    }
) as client:
    # 문화공공데이터광장/KCISA OpenAPI
    page = client.culture.leisure_activity_facilities(num_of_rows=5)
    for item in page.items:
        print(item.name, item.address, item.latitude, item.longitude)

    # 공공데이터포털 자동변환 API
    classes = client.data_go.leisure_classes(per_page=5)
    print(classes.total_count, classes.items[0])

    # 파일 데이터 다운로드 및 CSV 읽기
    rows = client.file_data.read_csv("leisure_classes_csv")
    print(rows[0])

# 사람 읽기 쉬운 제목과 endpoint를 포함한 카탈로그
for item in get_api_catalog(kind=DatasetKind.KCISA_OPEN_API):
    print(item["label"], item["endpoint_url"])
```

## 비동기 사용

`python-krheritage-api`와 같은 형태로 `McstClient.aio()`를 사용합니다. 내부 transport는
`httpx.AsyncClient`이며, async 호출에는 기본 token bucket rate limit이 적용됩니다.

```python
from mcst import McstClient

async with McstClient.aio(service_keys={"cafe_bookstores": "..."}) as client:
    page = await client.culture.cafe_bookstores(num_of_rows=10)
    for item in page.items:
        print(item.name, item.address)

    classes = await client.data_go.leisure_classes(per_page=5)
    print(classes.total_count)
```

## 디버그 fixture 저장 (예제)

별도 Web UI나 로컬 디버그 도구는 라이브러리에 Streamlit을 직접 의존시키지 않고
`debug_request()` 결과를 fixture로 저장하는 방식으로 연결합니다. 저장된 fixture는
외부 API를 다시 호출하지 않고 raw response를 replay해 회귀 테스트에 사용합니다.

```python
from mcst import CultureOpenApiClient, save_fixture

client = CultureOpenApiClient.from_env()
debug_run = client.debug_request(
    "leisure_activity_facilities",
    keyword="공원",
    num_of_rows=5,
)

path = save_fixture(
    debug_run,
    base_dir="tests/fixtures",
    case_name="leisure_activity_park_normal",
    description="전국 문화 여가 활동 시설 공원 검색 정상 케이스",
    overwrite=False,
)
print(path)
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
python -m pip install -r debug-ui/requirements.txt
python -m streamlit run debug-ui/app.py
```

Debug Trace 탭은 선택한 데이터셋의 카탈로그 항목을 함께 보여줍니다. 예를 들어
`cafe_bookstores`는 `한국문화정보원_카페가 있는 서점데이터`로 표시됩니다.
Service key 입력칸은 선택한 API마다 별도로 유지되며, 실행 시 현재 선택한
API의 키만 요청에 사용합니다.

## 주요 카탈로그

### KCISA OpenAPI

- `leisure_activity_facilities`: 전국 문화 여가 활동 시설(액티비티)
- `leisure_camping_facilities`: 전국 문화 여가 활동 시설(캠핑)
- `family_infant_culture_facilities`: 전국 가족 유아 동반 가능 문화시설
- `independent_bookstores`: 전국 독립서점 및 운영정보
- `cafe_bookstores`: 카페가 있는 서점데이터
- `used_bookstores`: 전국 중고서점 및 운영정보
- `barrier_free_places`: 전국 문화예술관광지 배리어프리 정보
- `pet_friendly_culture_facilities`: 전국 반려동물 동반가능 문화시설 위치
- `media_famous_places`: 미디어콘텐츠 영상 내 유명지
- `multilingual_guide_culture_facilities`: 전국 다국어 가이드 제공 문화시설
- `small_theaters`: 전국 연극장 및 소극장 정보
- `world_restaurants`: 전국 세계음식점
- `meeting_seminar_facilities`: 전국 회의 세미나 시설정보

### 파일/API 자동변환 데이터

- `tourism_lodging_status`: 전국 관광숙박시설 현황
- `hotels_status`: 전국호텔현황
- `leisure_activity_facilities_csv`: 전국 문화 여가 활동 시설(액티비티) 데이터
- `leisure_camping_facilities_csv`: 전국 문화 여가 활동 시설(캠핑) 데이터
- `leisure_classes_csv`: 전국 문화 여가 활동 시설(클래스) 데이터
- `used_bookstores_csv`: 전국 중고서점 및 운영정보
- `public_libraries`: 전국공공도서관정보
- `small_libraries`: 작은도서관 운영 현황
- `golf_courses_status`: 전국 골프장 현황
- `public_sports_facilities`: 전국공공체육시설 현황
- `marathon_events`: 국내마라톤대회 정보

## 검증

```bash
python -m pytest
python -m ruff check .
python -m mypy src/mcst
```

### 라이브 테스트

```bash
python -m pytest -m live
```

현재 네트워크에서 `api.kcisa.kr` DNS가 막혀 있거나, 서비스키가 ODCloud에 등록되어 있지 않으면 해당 live test는 실패 대신 skip 처리합니다. 일반 단위 테스트는 외부 서비스를 호출하지 않습니다.

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
| `debug-ui/` | 로컬 Streamlit 디버그 UI (라이브러리 본체는 미의존) |

## 문서/기여 규칙

- 모든 문서는 한글로 작성합니다. 코드 식별자, 명령어, URL, 환경 변수명, 공식 데이터셋명 등 원문 유지가 필요한 값만 예외입니다.
- 공개 API 또는 지원 카탈로그가 바뀌면 같은 패치에서 관련 문서(`README.md`, `docs/catalog.md`)와 테스트를 함께 갱신합니다.
- 작업 전 [AGENTS.md](AGENTS.md)의 범위 규칙과 DO NOT 목록을 확인합니다.
- API 키는 커밋, 로그, 예외 메시지, 문서, 테스트 출력 어디에도 노출하지 않습니다.

## 법적 고지

이 저장소의 라이선스(GPL-3.0-or-later, [LICENSE](LICENSE))는 이 저장소에 포함된 코드에만 적용됩니다. 이 라이브러리가 감싸는 문화체육관광부·KCISA·공공데이터포털의 데이터와 API는 각 제공기관의 이용약관과 라이선스를 따르며, 이 프로젝트는 해당 데이터의 정확성·최신성이나 API의 가용성에 대해 어떠한 법적 효력이나 보증도 제공하지 않습니다. 실제 서비스에 사용하기 전에 제공기관의 활용 신청 절차와 이용약관을 직접 확인하십시오.
