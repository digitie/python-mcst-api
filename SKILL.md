# SKILL — python-mcst-api 에이전트 매뉴얼

> 이 파일은 당신(AI 에이전트)이 작업을 시작하기 전 반드시 읽어야 합니다.
> 1회만 정독해도 불필요한 시행착오와 구현 결함을 완전히 방지할 수 있습니다.

## 1. 정체성

이 저장소(`python-mcst-api`)는 대한민국 문화체육관광부(MCST) 및 그 산하/유관기관이 제공하는 문화, 여가, 숙박, 여행, 체육, 도서관 위치 데이터 등 선별된 데이터셋을 파이썬 환경에서 안전하게 소비할 수 있게 돕는 **타입 지정(Typed) Python 클라이언트 패키지**입니다.

이 패키지는 철저하게 `src/mcst/catalog.py`에 선별 등록된 카탈로그를 유일한 기준으로 봅니다. 범위 밖의 다른 지자체나 타 부처(행안부 등)의 데이터는 카탈로그에 명시적으로 추가된 경우가 아니라면 일절 구현 대상에서 제외합니다.

### 식별자 매핑

| 항목 | 값 |
|------|----|
| GitHub 저장소 | `python-mcst-api` |
| 패키지명 | `mcst` |
| 주 의존성 | `httpx`, `pydantic>=2.7` |
| 개발 의존성 | `pytest`, `pytest-asyncio`, `pytest-cov`, `ruff`, `mypy` |

## 2. 빠른 시작

```bash
# Windows PowerShell 환경 인코딩 설정
$OutputEncoding = [System.Text.UTF8Encoding]::new()
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()

# 의존성 설치 및 가상환경 구동
pip install -e .[dev]

# 4대 품질 검증 수행 (PR 전 필수 로컬 실행)
python -m compileall src/mcst tests
python -m pytest
python -m ruff check .
python -m mypy src/mcst
```

모든 개발 작업은 에이전트 전용 고정 worktree 경로(`python-mcst-api-claude`, `python-mcst-api-antigravity`, `python-mcst-api-codex`)에서 진행하며, 매 세션마다 `git fetch` 후 새 브랜치를 따고 `codegraph sync`를 수행하는 것을 원칙으로 합니다 (ADR-1).

## 3. 디렉토리 지도

```
src/mcst/
  catalog.py     — 선별 데이터셋 및 API 목록 정보의 단일 Source of Truth
  _http.py       — httpx.AsyncClient 기반의 재시도, 세션 관리, 오류 정규화 공통 엔진
  _convert.py    — 문자열 날짜 변환 등 작은 도메인-중립적 변환 헬퍼
  models.py      — 다운스트림이 안전하게 받아 쓸 Pydantic v2 응답 모델 스키마
  culture.py     — culture.go.kr (KCISA) OpenAPI 전용 어댑터/클라이언트
  data_go.py     — 공공데이터포털 ODCloud 자동변환 파일 API 어댑터/클라이언트
  file_data.py   — 원본 CSV/JSON 직접 파일 다운로드 및 파싱 유틸리티
  client.py      — 소비자가 쓸 최상위 편의 통합 클라이언트 (McstClient)
  exceptions.py  — McstError 등 공개 예외 클래스 계층 구조
  debug.py       — Web UI 및 로컬 분석기용 민감 데이터 마스킹 및 fixture 저장 유틸리티
  replay.py      — 실제 HTTP 요청 없이 저장된 fixture를 재현하는 오프라인 테스트 헬퍼
tests/
  fixtures/      — 디버깅이나 단위 테스트에 쓰이는 실제 API 응답 mockup JSON들
  test_*.py      — 오프라인 mock 테스트 스위트
  test_live.py   — 실제 공공 서버망을 찔러보는 live 테스트 (평소엔 skip)
```

## 4. 절대 하지 말 것 (DO NOT)

1. **API 키 평문 노출 금지**: 테스트 코드, fixture 파일, docs 문서, 예외 에러 메시지(`repr` 포함) 등에 어떠한 형태의 API 키나 UUID 비밀값을 절대 커밋하거나 포함하지 마십시오.
2. **관광공사 데이터셋 구현 금지**: 한국관광공사가 제공하는 서비스와 데이터셋은 관광 테마에 해당하더라도 이 패키지의 범위(문체부 본청/유관기관 위주)가 아니므로 일절 제외합니다.
3. **불필요하고 얇은 Wrapper 생성 금지**: 외부 API를 단순히 중첩해서 씌우기만 하는 무의미한 통과 클래스나 장기 호환용 임시 Facade는 설계 복잡도만 높이므로 배제합니다.
4. **결과 코드 미검증 응답 수용 금지**: 한국 공공 OpenAPI는 HTTP 200 통과 응답에 실제 에러 내용(예: "SERVICE_KEY_IS_NOT_REGISTERED_ERROR")을 XML/JSON 페이로드로 담아 보내는 경우가 허다합니다. 따라서 응답 바디 수준의 결과 코드(`resultCode` 등)를 철저히 검증해야 합니다.
5. **live 데코레이터 누락 금지**: 실제 외부 서버를 직접 타격하는 테스트 케이스에는 반드시 `@pytest.mark.live` 데코레이터를 지정하여 오프라인 단위 테스트 구동 시 자동으로 차단/스킵될 수 있게 하십시오.
6. **동일 패치 내 문서 미갱신 금지**: 지원 API 추가나 기능 변경 시, `docs/catalog.md`, `src/mcst/catalog.py` 및 관련 테스트 코드를 같은 PR/패치에 담아 동시에 갱신해야 합니다.
7. **비밀값이 포함된 예외 전파 금지**: 인증 오류 처리나 HTTP 실패 예외 발생 시, 원본 예외 메시지나 요청 파라미터 내의 API 키 값을 마스킹(`redact`) 처리한 뒤 예외를 가공하여 전파하십시오.
8. **PowerShell 인코딩 깨짐 무시 금지**: 한글 인코딩이 깨진 상태로 shell 출력을 읽어 오류를 잘못 분석하지 않도록, 세션 진입 즉시 한글 출력 활성화 명령을 먼저 수행하십시오.

## 5. 자주 묻는 작업 시작 파일

| 구현 목표 | 시작 파일 |
|------|-----------|
| 새로운 문체부 산하기관 API 추가 | `src/mcst/catalog.py`에 카탈로그 추가 -> `src/mcst/models.py`에 모델 선언 -> `src/mcst/culture.py` 또는 `data_go.py`에 클라이언트 메서드 추가 |
| 공공 API 호출 재시도 정책 수정 | `src/mcst/_http.py`의 `AsyncClient` 설정 및 `_request` 내부 재시도 가드 |
| 응답 내 한국어 날짜/타입 포맷팅 헬퍼 | `src/mcst/_convert.py` |
| 새로운 오프라인 테스트 Fixture 활용 검증 | `tests/fixtures/`에 원본 JSON 추가 -> `tests/test_generated_fixtures.py`에 replay 구동 추가 |

## 6. 도메인 어휘

| 용어 | 의미 |
|------|------|
| **MCST** | 문화체육관광부 (Ministry of Culture, Sports and Tourism) |
| **KCISA** | 한국문화정보원. `culture.go.kr` OpenAPI 서비스를 실무 운영하는 주체 |
| **data.go.kr** | 대한민국 공공데이터포털. 문체부 산하 기관들이 원본 파일 및 API를 개방하는 포털 |
| **ODCloud** | 공공데이터포털에서 파일 데이터(CSV)를 실시간 JSON API 형태로 동적 변환하여 제공하는 백엔드 클라우드 포커스 인터페이스 |
| **Replay** | 사전에 `debug.py` 유틸 등으로 덤프해둔 실제 공공 API 응답 mockup(`tests/fixtures/**/*.json`)을 활용하여, 외부 네트워크 단절 상황에서도 동일한 변환 파서 로직을 정교하게 재현하여 검증하는 테스트 패턴 |

## 7. 작업 후 체크리스트

- [ ] `python -m compileall src/mcst tests` 컴파일 성공 확인
- [ ] `python -m pytest` 단위 테스트 100% 통과 확인
- [ ] `python -m ruff check .` 린트 경고 없음 확인
- [ ] `python -m mypy src/mcst` 정적 타입 strict 무오류 확인
- [ ] `docs/journal.md`에 날짜별 상세 저널 추가 완료 (역시간순)
- [ ] `docs/tasks.md`에 `T-NNN` 진행 상태 `Done` 업데이트 완료
- [ ] 결정 사항에 대한 ADR(Architecture Decision Record)이 존재하는 경우 `docs/decisions.md` 반영 완료
- [ ] 가시적인 갱신 사항 발생 시 `CHANGELOG.md` 갱신 여부 점검
