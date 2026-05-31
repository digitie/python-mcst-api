# python-mcst-api

`python-mcst-api`는 문화체육관광부 및 산하기관의 공개 데이터 중 여행, 여가, 숙박, 문화시설, 도서관 위치/운영 정보에 맞춘 비공식 Python 클라이언트입니다.

한국관광공사 제공 서비스, 행정안전부/지자체 단독 제공 자료, 도서관 소장자료/서지/ISBN/추천도서 데이터는 제외했습니다.

현재 구현은 선별형이지만 `culture.go.kr`의 다른 OpenAPI와 파일데이터도 같은 카탈로그 구조로 확장할 수 있습니다. 전체 목록 조사표는 [docs/culture-go-kr-full-catalog.md](docs/culture-go-kr-full-catalog.md)에 정리했습니다.

## 설치

배포 패키지 이름은 `python-mcst-api`이고, Python 코드에서 사용하는 import 이름은 `mcst`입니다.

```bash
pip install -e .[dev]
```

## 개발 환경 메모

이 저장소의 Windows 작업 환경에서는 `rg.exe`가 권한 문제로 실행되지 않을 수 있습니다. 검색이 필요하면 PowerShell의 `Get-ChildItem -Recurse -File`과 `Select-String`을 사용합니다.

이 worktree에서는 Git 명령도 WSL 기본 `git` 대신 Windows Git (`git.exe`)를 사용합니다. 예를 들어 `/mnt/c/Program Files/Git/cmd/git.exe status`처럼 실행하면 `.git`가 Windows 경로를 가리키는 worktree에서도 상태 조회와 브랜치 작업이 안정적으로 동작합니다.

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

대체 환경 변수도 인식합니다.

- `DATA_GO_KR_SERVICE_KEY`
- `DATA_GO_KR_SERVICE_KEY`
- `DATA_GO_KR_SERVICE_KEY`

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

## 디버그 fixture 저장

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
- `public_libraries`: 전국공공도서관정보
- `small_libraries`: 작은도서관 운영 현황
- `golf_courses_status`: 전국 골프장 현황
- `public_sports_facilities`: 전국공공체육시설 현황
- `marathon_events`: 국내마라톤대회 정보

## 라이브 테스트

```bash
pytest -m live
```

현재 네트워크에서 `api.kcisa.kr` DNS가 막혀 있거나, 서비스키가 ODCloud에 등록되어 있지 않으면 해당 live test는 실패 대신 skip 처리합니다. 일반 단위 테스트는 외부 서비스를 호출하지 않습니다.
