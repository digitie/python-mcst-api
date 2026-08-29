# 에이전트 작업 지침

## 목표

이 저장소는 문화체육관광부 및 산하기관의 일부 공공데이터/API(여행, 여가, 숙박, 문화시설, 도서관 위치/운영)를 감싸는 작은 타입 지정 Python 패키지입니다. `mcst.catalog`를 지원 데이터셋의 단일 기준으로 삼아, downstream이 직접 사용할 수 있는 안정된 typed client와 Pydantic 모델을 제공합니다. 변경은 작게 유지하고, 카탈로그 중심으로 구현하며, 테스트와 문서를 함께 갱신합니다.

## Think Before Coding

- 공개 동작을 바꾸기 전에 `README.md`, `docs/catalog.md`, `src/mcst/catalog.py`를 먼저 읽어 대상 항목과 기존 계약을 확인합니다.
- 외부 API(culture.go.kr, KCISA, data.go.kr) 관련 작업은 새 wrapper/adapter/gateway가 정말 필요한지부터 판단한 뒤 진행합니다.

## Simplicity First

- 불필요한 얇은 wrapper, 단순 전달용 함수/클래스, 장기 호환 alias, 임시 facade는 만들지 않습니다.
- 단순 재포장을 위한 의존성 추가는 피하고, 정확성·유지보수성·공개 API에 직접적 이득이 있을 때만 새 의존성을 도입합니다.

## Surgical Changes

- 최소 수정을 기본값으로 하되, 라이선스·의존성·저장소 범위에 맞는 검증된 외부 구현이 있으면 최소 수정과 충돌하더라도 그 구현을 직접 적용하는 편을 우선합니다.
- 하나의 데이터셋 래퍼를 되돌려도 관계없는 카탈로그·문서 작업이 함께 사라지지 않도록 커밋을 작게 유지합니다.

## Goal-Driven Execution

- downstream이 직접 사용할 안정된 public client, typed model, enum, helper 제공을 목표로 삼습니다. 필요한 endpoint·pagination·cursor·exception·raw payload 계약이 부족하면 이 저장소의 public API를 먼저 안정화합니다.
- 공개 API 또는 지원 카탈로그가 바뀌면 같은 패치에서 관련 문서(`README.md`, `docs/catalog.md`)와 테스트를 함께 갱신합니다.

## Practical Bias

- fixture로 쉽게 검증 가능한 동작은 오프라인 테스트를 먼저 추가하거나 갱신하고, 실제 서비스 검증은 `pytest -m live`로 보완합니다.
- 한국 공공 API는 HTTP 200으로 애플리케이션 오류를 반환하는 일이 많으므로, 항상 본문 수준의 결과 코드를 확인합니다.
- 이 Windows 환경에서는 `rg.exe`가 `Access is denied`로 실행되지 않을 수 있습니다. 그런 경우 `Get-ChildItem -Recurse -File`과 `Select-String`으로 우회합니다. 문서는 UTF-8로 저장되어 있지만 PowerShell 기본 출력 인코딩 때문에 한글이 깨져 보일 수 있으므로, 파일을 읽을 때는 `Get-Content -Encoding UTF8`을 사용하고 Python 등으로 한글을 출력할 때는 필요하면 `$OutputEncoding`과 `[Console]::OutputEncoding`을 UTF-8로 먼저 지정합니다.

## 문서 언어 정책

이 저장소의 모든 Markdown/RST 문서(README, `docs/`, `AGENTS.md`, 테스트 설명, changelog 포함)와 Python 코드 안의 주석·docstring은 한글로 작성합니다. 코드 식별자, 명령어, URL, 환경 변수명, 공식 데이터셋명, API 필드명처럼 원문 유지가 필요한 값과 외부 자료에서 가져온 공식 명칭은 임의로 번역하지 않고 그대로 둡니다. 새 문서나 기존 문서를 수정할 때도 이 규칙을 우선합니다.

## 식별자 표

| 이름 | 값 |
| --- | --- |
| PyPI/배포 패키지 이름 | `python-mcst-api` |
| Python import 이름 | `mcst` |
| GitHub 저장소 | `digitie/python-mcst-api` |
| 서비스키 환경 변수 (우선) | `KCISA_SERVICE_KEY` |
| 서비스키 환경 변수 (fallback) | `DATA_GO_KR_SERVICE_KEY` |

## 절대 하지 말 것 (DO NOT)

- 한국관광공사 제공 서비스/데이터, 행정안전부·지자체 등 비문체부 공공기관 자료는 카탈로그에 명시적으로 포함된 경우가 아니면 추가하지 않습니다. 도서관은 위치/운영 정보만 포함하고 소장자료·서지·ISBN·국가자료종합목록·추천도서·장서 검색 API는 포함하지 않습니다.
- 불필요한 얇은 wrapper/adapter/gateway, 단순 전달용 함수/클래스, 장기 호환 alias, 임시 facade는 만들지 않습니다. 기존 코드의 책임 경계가 충분하면 그 경계를 그대로 사용합니다.
- API 키를 커밋하거나 로그, 예외 메시지, `repr` 출력, 문서, 테스트 출력에 노출하지 않습니다.
- `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `__pycache__`, `.coverage`, 빌드 산출물, 가상환경을 커밋에 포함하지 않습니다.
- 일반(비-live) 테스트에서 네트워크를 호출하지 않습니다 — HTTP 동작은 fake session 또는 fixture로 검증합니다.

## 공개 동작을 바꾸기 전에

1. `README.md`를 읽습니다.
2. `docs/catalog.md`를 읽습니다.
3. 대상 항목을 `src/mcst/catalog.py`에서 확인합니다.
4. fixture로 쉽게 검증 가능한 동작은 오프라인 테스트를 먼저 추가하거나
   갱신합니다.
5. 공개 API 또는 지원 카탈로그가 바뀌면 같은 패치에서 문서도 갱신합니다.

## 모듈 책임

- `mcst.catalog`: 선별 데이터/API 목록과 포함/제외 판단의 기준입니다.
- `mcst._http`: 세션, 재시도, 응답 정규화, 제공자 오류 매핑을 담당합니다.
- `mcst._convert`: 응답 경계에서 쓰는 작은 변환 헬퍼입니다.
- `mcst.models`: 공개 Pydantic 응답 모델입니다.
- `mcst.culture`: `culture.go.kr`/KCISA OpenAPI 클라이언트입니다.
- `mcst.data_go`: 공공데이터포털 ODCloud 자동변환 파일 API 클라이언트입니다.
- `mcst.file_data`: 직접 파일 다운로드와 CSV 파싱 헬퍼입니다.
- `mcst.client`: 상위 편의 클라이언트입니다.
- `mcst.debug`: Web UI나 로컬 디버그 도구가 쓸 `DebugRun`, 민감정보 마스킹,
  fixture 저장 헬퍼입니다. Streamlit에는 의존하지 않습니다.
- `mcst.replay`: 저장된 fixture response를 외부 API 호출 없이 다시 처리하는
  테스트 replay 헬퍼입니다.
- `mcst.exceptions`: 공개 예외 계층입니다.
- `tests`: 기본은 오프라인 테스트이며, live 테스트는 반드시 명시적으로
  표시합니다.

## API 키 정책

- TripMate live 확인에는 가능한 경우 `DATA_GO_KR_SERVICE_KEY`를 사용합니다.
- `api.kcisa.kr`는 data.go.kr 발급 키가 아닌 KCISA 전용 키가 필요하므로,
  문체부/KCISA API는 `KCISA_SERVICE_KEY`를 우선 읽고 `DATA_GO_KR_SERVICE_KEY`는
  fallback으로만 사용합니다(대부분 인증에 실패합니다).

## 테스트 정책

- HTTP 동작은 fake session 또는 fixture로 검증합니다.
- 디버그 UI가 저장한 fixture는 `tests/fixtures/**/*.json`에 두고,
  `tests/test_generated_fixtures.py`에서 replay 방식으로 검증합니다.
- live 테스트는 반드시 `@pytest.mark.live`를 사용합니다.
- live 테스트는 실제 데이터의 불안정한 값이 아니라 응답 형태와 오류 매핑을
  검증합니다.
- live 키가 있지만 제공자가 거절하면 명확한 이유와 함께 skip 처리합니다.
- 현재 환경에서 `api.kcisa.kr` DNS를 해석할 수 없으면 KCISA live 테스트를
  명확한 이유와 함께 skip 처리합니다.
- 새 파서를 추가할 때는 단일 객체 응답과 리스트 응답을 모두 테스트합니다.

## 검증 명령

```bash
python -m compileall src/mcst tests
python -m pytest
python -m ruff check .
python -m mypy src/mcst
```

실제 서비스를 검증할 때만 live 테스트를 실행합니다.

```bash
python -m pytest -m live
```

## 문서 갱신 정책

같은 패치에서 관련 문서를 갱신합니다.

- 사용자용 사용법 변경: `README.md`
- 지원 데이터/API 변경: `docs/catalog.md`, `src/mcst/catalog.py`
- 사용자에게 보이는 오류 동작 변경: 관련 테스트와 필요 시 `README.md`
- 에이전트 작업 방식 변경: 이 파일

## 커밋 위생

- 하나의 데이터셋 래퍼를 되돌려도 관계없는 카탈로그나 문서 작업이 함께
  사라지지 않도록 커밋을 작게 유지합니다.
- 카탈로그 항목의 한국어 제공기관명과 공식 데이터셋명은 정확히 보존합니다.
