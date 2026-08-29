# 디버그 UI fixture와 replay 테스트

## 설계 원칙

- Web UI는 테스트 코드를 대량 생성하지 않고 fixture JSON을 만드는 도구로 둡니다.
- `python-mcst-api` 본 패키지는 Streamlit에 의존하지 않습니다.
- 별도 UI 프로젝트는 `mcst`를 wheel 또는 editable install로 가져와 `debug_request()`를 호출합니다.
- pytest는 `tests/fixtures/**/*.json`을 자동으로 읽어 외부 API 호출 없이 replay 기반 회귀 테스트를 수행합니다.

## 디버그 실행 경계

`CultureOpenApiClient.debug_request()`와 `DataGoFileApiClient.debug_request()`는 `DebugRun`을 반환합니다.

`DebugRun`에는 다음 값이 들어갑니다.

| 필드 | 내용 |
| --- | --- |
| `function` | fixture runner가 사용할 함수 식별자입니다. 예: `culture.leisure_activity_facilities`, `data_go.leisure_classes_csv` |
| `input` | UI 또는 호출자가 입력한 dataset, paging, keyword, 추가 파라미터입니다. |
| `request` | HTTP method, URL, query입니다. 인증키는 `<REDACTED>`로 마스킹됩니다. |
| `response` | HTTP 상태(`status_code`), 소요시간(`elapsed_ms`), 응답 헤더, 파싱된 raw body입니다. |
| `parsed` | 라이브러리의 Pydantic `Page` 모델입니다. |
| `processed` | replay snapshot 비교에 사용하는 안정화된 결과입니다. `raw`는 제외합니다. |
| `trace` | UI에서 보여줄 주요 처리 단계입니다. |
| `error` | 예외가 발생했을 때 type/message와 가능한 경우 `failure_kind`, `endpoint`, `status_code`, `result_code`를 담습니다. |

## fixture 저장 형식

`save_fixture()`는 기본적으로 다음 경로에 저장하도록 설계했습니다.

```text
tests/fixtures/{function}/{case_name}.json
```

예시는 다음과 같습니다.

```python
from mcst import DataGoFileApiClient, save_fixture

client = DataGoFileApiClient.from_env()
debug_run = client.debug_request("leisure_classes_csv", per_page=3)

save_fixture(
    debug_run,
    base_dir="tests/fixtures",
    case_name="leisure_classes_normal",
    description="전국 문화 여가 활동 시설 클래스 정상 응답",
)
```

같은 파일명이 이미 있으면 기본적으로 덮어쓰지 않고 `FileExistsError`를 냅니다. 의도적으로 갱신할 때만 `overwrite=True`를 사용합니다.

## 민감정보 마스킹

fixture 저장 전 다음 key는 재귀적으로 `<REDACTED>` 처리합니다.

- `authorization`
- `x-api-key`
- `api_key`
- `apikey`
- `access_token`
- `refresh_token`
- `serviceKey`
- `service_key`

API 키는 테스트 실패 메시지, fixture, 문서 예시에 남기지 않습니다.

## assertion mode

현재 공통 runner는 아래 mode를 지원합니다.

| mode | 의미 | 상태 |
| --- | --- | --- |
| `snapshot` | `processed` 전체를 비교합니다. `exclude_fields`는 재귀적으로 제외합니다. | 기본 |
| `schema_only` | replay 결과가 생성되는지만 확인합니다. | 지원 |
| `required_fields` | 최상위 필드 존재 여부를 확인합니다. | 지원 |
| `count` | `total_count` 값을 비교합니다. | 지원 |

복잡한 custom assertion은 아직 두지 않습니다. 필요한 경우 fixture schema를 먼저 확장한 뒤 runner를 갱신합니다.

## replay 테스트 구조

현재 저장소는 다음 구조를 사용합니다.

```text
tests/
  fixtures/
    culture.leisure_activity_facilities/
      normal.xml_response.json
    data_go.leisure_classes_csv/
      normal.json_response.json
  test_generated_fixtures.py
  utils.py
```

`tests/test_generated_fixtures.py`는 모든 fixture를 읽고 `mcst.replay.replay_case()`로 처리합니다. 이 과정은 실제 MCST, KCISA, data.go.kr 서버에 접속하지 않습니다.

## 별도 Streamlit UI에서의 사용

Streamlit UI는 라이브러리 패키지와 분리합니다. 이 저장소에는 로컬 실행용 예시 UI를
`examples/streamlit_debug_ui.py`에 두었습니다. Streamlit/pandas 의존성은
`pyproject.toml`의 `debug-ui` optional extra로만 설치합니다.

```bash
pip install -e ".[debug-ui]"
python -m streamlit run examples/streamlit_debug_ui.py
```

UI는 다음 순서로 사이드바를 구성합니다.

1. Data source(`KCISA OpenAPI` / `data.go.kr ODCloud 자동변환 API`) → API 2단 선택
2. 선택한 API에 대한 설명 캡션 2줄(무엇을 하는 API인지, 어떤 데이터를 반환하는지)
3. Environment: 실제 서비스가 읽는 env var(`KCISA_SERVICE_KEY`/`DATA_GO_KR_SERVICE_KEY`)
   사용 여부를 선택하는 라디오
4. Auth: 실제 쿼리 파라미터명인 `serviceKey` 입력창
5. 서비스키 발급/활용신청 링크 버튼(카탈로그의 `detail_url`, `spec_url`)
6. Timeout 숫자 입력
7. Fixture 저장 기준 디렉터리(기본 `tests/fixtures`, `Custom...`으로 직접 입력 가능)

메인 영역의 파라미터 입력 폼은 카탈로그의 `required_params`/`optional_params`
메타데이터에서 위젯을 자동 생성합니다 — 데이터셋별 `if function_name == ...`
분기가 없습니다. 실행은 항상 `McstClient.debug_fetch()`를 통해 카탈로그
`kind`(`kcisa_open_api` / `data_go_file_api`)로 라우팅됩니다.

고정 6개 탭을 제공합니다.

- Raw Response
- Pydantic Model
- Processed Result
- Validation Errors
- Debug Trace
- Fixture / Testcase

데이터셋 선택 목록은 slug 대신 사람이 읽기 쉬운 데이터셋명과 slug를 함께 보여줍니다.
Debug Trace 탭은 `get_api_catalog()`가 반환하는 카탈로그 항목을 표시해 endpoint,
출처, 상세 페이지 URL, 요청/응답(상태 코드·소요시간 `elapsed_ms`)을 바로 확인할 수
있게 합니다. 서비스 키는 복붙 과정에서 앞뒤에 붙는 공백과 감싸는 따옴표를 제거한
뒤 요청에 사용합니다. Service key 입력칸은 선택한 데이터셋 slug별로 따로
유지되므로, API별 활용 신청 키가 다른 경우에도 현재 API의 키만 요청 파라미터에
들어갑니다.

마지막 실행 결과는 `f"{kind}:{slug}"`로 세션 상태에 스코프되므로, data source나
API를 전환해도 이전에 실행한 결과가 잘못 남아 보이지 않습니다.

UI의 저장 버튼은 `save_fixture()`만 호출하면 됩니다. 라이브러리 패키지에는 Streamlit, pandas 같은 UI 의존성을 추가하지 않습니다(`mcst` 본체는 `debug-ui` extra에 의존하지 않습니다).

`FILE_DOWNLOAD`(culture.go.kr/data.go.kr 파일 다운로드 페이지 스크레이핑 후 CSV
다운로드)와 `LINK`(외부 링크만 있고 호출 가능한 API가 없음) kind의 데이터셋은
`McstClient.debug_fetch()`가 지원하지 않습니다 — Data source 선택지에도
노출하지 않으며, `mcst.file_data.FileDataClient`에는 아직 `DebugRun`을 만드는
동등한 메서드가 없습니다.
