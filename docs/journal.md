# JOURNAL — 작업 일지

새 항목은 항상 파일 맨 위에 추가(역시간순). 기존 항목은 절대 수정하지 않는다 — 잘못된 결정조차 기록으로 남는 것이 가치다.

---

## 2026-06-12 (#9 — 빈 params가 URL query를 박탈: 파일 다운로드 live 전수 실패 수정)

**작업**: #7 머지 직후 live 검증에서 culture.go.kr 상세페이지 13종 전부
`could not find a CSV download link`로 실패. 격리 실험으로
`session.get(url, params={})` — **httpx는 params를 명시하면(빈 dict 포함) URL
자체의 query를 통째로 대체**함을 확인(`request.url`에 query 부재).
`get_response`가 항상 `params=query`를 전달해 `fileDataNo` 등이 박탈된 빈 셸
페이지를 받고 있었다. 기존 fixture 테스트는 fake가 httpx의 이 의미론을 흉내
내지 않아 잡지 못했다.

**구현**: 동기/비동기 `get_response` 모두 query가 비면 params를 전달하지 않음.
httpx 의미론 모사 fake(`HttpxSemanticsFakeSession`) 회귀 테스트 추가. 수정 후
**파일 카탈로그 15종 전수 live 다운로드 성공**(tourism_attractions 64,194행,
media_famous_places 15,034행, pet_friendly 23,929행, public_libraries 1,296행 등).
게이트: pytest 34 passed / ruff / mypy green.


**작업**: KCISA OpenAPI(`api.kcisa.kr`)가 공인 DNS로 해석되지 않고 data.go.kr
발급 키가 아닌 KCISA 전용 키를 요구(#6 — krtour-map T-212e live full reload에서
HTTP 403/401 실측)하여, culture/도서관 데이터셋의 주요 수급 경로를 **서비스키가
필요 없는 CSV 파일 다운로드**로 전환(#7)했다.

**구현 상세**:
- **카탈로그 재편** (`catalog.py`): `CULTURE_FILE_DATASETS` 14종
  (`*_csv` + `golf_courses_status`) + `LIBRARY_FILE_DATASETS`(`public_libraries`)
  신설. `CULTURE_OPEN_APIS`(11종)는 명세 참고용으로 강등. `update_cycle`은
  각 명세서/fileData 페이지 실측값(2026-06-11).
- **다운로드 시점 링크 해석** (`file_data.py`): CSV 파일명에 업로드 일시가
  박혀 있어(`API_CIA_089_20260530182204.csv`) URL 하드코딩 불가 →
  `extract_download_url`이 culture.go.kr `filedatDtl.do`의 `fnFileDwld(...)`
  또는 data.go.kr `fileData.do`의 `fileDownload.do` 링크를 스크레이핑하고
  한글/공백 query를 percent-encoding 정규화. `resolve_file_url`(동기/비동기)이
  FILE_DOWNLOAD 항목을 해석하며, 미발견 시 고정 `file_url` 폴백, 둘 다 없으면
  `McstParseError`. `iter_csv`/`read_csv`는 utf-8-sig/utf-8/cp949/euc-kr
  인코딩 폴백.
- **클라이언트 정리**: `CultureOpenApiClient`에서 파일 전용으로 이동한 3종
  (multilingual_guide/small_theaters/meeting_seminar) 헬퍼 제거.
  `DataGoFileApiClient`는 ODCloud 식별자(`public_data_pk`) 보유 항목 전용
  (`public_libraries`)으로 정리.
- **품질 보증**: 실 다운로드 페이지 HTML fixture 2종(culture/filedatDtl,
  data.go.kr/fileData) 기반 `tests/test_file_download.py` 신설(추출/정규화/
  폴백/에러/카탈로그 노출 7케이스) + 기존 클라이언트 테스트를 2-hop
  (상세페이지→CSV) 라우팅 fake로 재정렬 + cp949 폴백 검증. 게이트:
  pytest 33 passed / ruff / mypy 전부 green.

## 2026-06-07 (T-005 — S3 호환 RustFS 로컬 병행 저장 API 추가 및 동적 임포트 적용)

**작업**: 다운스트림에서 문체부 파일데이터를 다운로드할 때 로컬 파일과 동시에 S3 호환 객체 저장소인 RustFS에 저장할 수 있도록 기능을 고도화하였다.

**구현 상세**:
- **클라이언트 API 확장**:
  - `mcst.file_data.FileDataClient`에 `save_rustfs` 동기 메서드 추가.
  - `mcst.file_data.AsyncFileDataClient`에 `save_rustfs` 비동기 메서드 추가.
  - 기존의 `save`는 그대로 유지하여 완벽한 하위 호환성 확보.
- **의존성 경량성 및 동적 임포트 (Lazy Load)**:
  - `boto3`와 `botocore` 패키지를 필수 의존성에 추가하지 않고, `save_rustfs` 호출 시점에만 `importlib`를 활용하여 동적으로 로딩하도록 처리. 
  - 미설치 환경에서는 오류 안내 메시지와 함께 `ImportError`를 전파하도록 가드 처리.
- **접속 자격증명 상속 체인 구현**:
  - `_resolve_rustfs_credentials` 헬퍼를 추가하여 explicit 매개변수가 없을 시 환경 변수(`MCST_RUSTFS_*`, `RUSTFS_*`, `KRTOUR_MAP_OBJECT_STORE_*`, `AWS_*` 순)에서 자격증명과 엔드포인트를 상속하여 세팅되도록 구현.
  - 비동기 클라이언트 호출 시 `asyncio.to_thread`로 감싸 스레드 풀에서 I/O를 비차단으로 구동.
- **품질 보증**:
  - `tests/test_clients.py`에 `unittest.mock`을 활용한 S3 `put_object` 동작 및 로컬 기록 무결성 검증용 Mock 유닛 테스트 케이스 2종 추가.
  - 4대 품질 게이트(`compileall`, `pytest`, `ruff`, `mypy`) 검증을 완벽 통과.
  - ADR-3 추가 및 `CHANGELOG.md` 갱신.

**다음 작업**: 변경사항 풀 리퀘스트 및 메인 브랜치 반영 준비.

---

## 2026-05-31 (T-003 & T-004 — 신규 API 2종 추가 및 HTTP 엔진 튜닝 완료)

**작업**: 관광/여가 테마 신규 API 2종을 카탈로그에 보완하고(`T-003`), 일시적 서버 혼잡에 유연하게 대처할 수 있도록 HTTP 엔진의 동적 타임아웃과 Full Jitter 백오프 튜닝(`T-004`)을 완수하였다.

**구현 상세**:
- **신규 카탈로그 통합 (`T-003`)**:
  - `leisure_classes` (전국 문화 여가 활동 시설 - 클래스 OpenAPI, ID: 586) 및 `recommended_travel_destinations` (문화체육관광부 추천여행지 OpenAPI, ID: 581)를 `src/mcst/catalog.py` 및 `docs/catalog.md`에 추가.
  - 동기/비동기 `CultureOpenApiClient`에 편리한 단축 헬퍼 메서드 추가 및 Pydantic `CultureRecord` 자동 매핑 적용.
- **HTTP 전송 레이어 고도화 (`T-004`)**:
  - `HttpClient`/`AsyncHttpClient` 및 `KcisaHttp`, `OdcloudHttp` 등의 호출 파이프라인 전반에 동적 `timeout: float | None = None` 파라미터를 추가하여 개별 요청별 타임아웃 튜닝 지원.
  - `_sleep_before_retry` 및 `_async_sleep_before_retry`에 랜덤 지터(Full Jitter, 0~10%)를 적용하여 서버 혼잡 시 폭주 현상(Thundering Herd)을 완벽히 방지함.
- **오프라인 테스트 강화**:
  - `tests/fixtures/culture.leisure_classes/normal.xml_response.json` 및 `tests/fixtures/culture.recommended_travel_destinations/normal.xml_response.json` replay mock fixture 2종 생성.
  - `tests/test_clients.py`에 신규 단축 메서드 동작 및 dynamic timeout 전송 무결성을 검증하는 동기/비동기 유닛 테스트 추가.
  - 4대 로컬 품질 게이트(`compileall`, `pytest`, `ruff`, `mypy`)를 완벽히 통과 완료.

**다음 작업**: 생성된 `feature/T002-T003` 브랜치의 원격 저장소 풀 리퀘스트 및 master 머지 준비.

---

## 2026-05-31 (T-002 — 워크트리 Prefix 변경 및 물리적 에이전트 독립 환경 구축 완료)

**작업**: 각 에이전트의 작업 환경(worktree) prefix 규격을 기존 `mcst-*`에서 `python-mcst-api-*`로 전면 교체 및 고도화하였으며, 실제로 로컬 환경에 3개의 독립 worktree를 생성하고 `@colbymchenry/codegraph` 정적 코드 인덱스 초기화(`init -i`)까지 완벽하게 수행해 냄.

**구현 상세**:
- **설정 파일 경로 전면 치환**: 
  - `antigravity.json`, `claude.json`, `codex.json`, `.gemini/mcp.json`, `.codex/config.toml` 내의 `cwd` 경로를 `"F:\\dev\\python-mcst-api-antigravity"` 등 새로운 prefix 규격으로 100% 교체 완료.
  - `.claude/settings.local.json` 에도 새로운 prefix 경로에서의 PowerShell 명령어 실행에 대한 자동 승인(allow) 권한을 정밀하게 매핑 및 보정함.
- **에이전트 가이드 문서 최신화**:
  - `CLAUDE.md`, `SKILL.md`, `docs/resume.md` 에 기술된 `mcst-*` 고정 worktree 명세를 모두 새로운 `python-mcst-api-*` 형태로 일관성 있게 업데이트하여 문서 정합성을 맞춤.
- **물리적 Git Worktree 생성**:
  - `git worktree add -d F:\dev\python-mcst-api-claude master` 등 3개의 에이전트별 worktree를 detached HEAD 상태로 물리 생성함.
- **각 워크트리별 CodeGraph 인덱싱 수행**:
  - `npx -y @colbymchenry/codegraph init -i` 명령을 각 worktree 디렉토리 하위에서 구동하여 21개 소스 파일에 대한 코어 그래프 노드/엣지 인덱스(`.codegraph/`) 빌드를 완료함 (각각 437개 노드, 416개 엣지 생성 성공).
- **PR 및 머지 완수**:
  - `chore/change-worktree-prefix` 브랜치 상에서 설정 수정을 커밋한 뒤 `master` 브랜치로 fast-forward 병합 및 원격 저장소(`origin/master`) 푸시를 완수함.

**검증**:
- **로컬 4대 게이트 통과**: `pytest`, `ruff check`, `mypy` strict 타입 검사가 모두 Success 상태를 완벽히 통과함을 검증.
- **물리적 워크트리 목록 점검**: `git worktree list`를 가동하여 3개의 worktree 매핑을 정상 수동 검증.

**다음 작업**: 대기 중인 작업 없음. 추가 카탈로그 보완을 기획할 예정.

---

## 2026-05-31 (T-001 — maplibre-vworld-js 고도화된 에이전트 협업 스타일 및 MCP 설정 적용)

**작업**: Claude, GPT, Antigravity 에이전트의 개발 정합성과 세션 연속성 확보를 위해, `maplibre-vworld-js` 프로젝트에서 검증된 고도화된 협업 양식(저널, 테스크, ADR 표준화)과 에이전트별 독립 고정 worktree 환경(MCP 설정)을 이 프로젝트(`python-mcst-api`)에 완벽히 이식하였다.

**구현 상세**:
- **MCP 설정 개편**: 
  - `antigravity.json`, `claude.json`, `codex.json` 각 설정 파일의 `codegraph` MCP `cwd` 경로를 이 프로젝트의 고유 worktree 경로(`F:\dev\mcst-antigravity`, `F:\dev\mcst-claude`, `F:\dev\mcst-codex`)로 갱신하여 인덱스 충돌을 원천 차단함.
  - `.gemini/mcp.json`, `.codex/config.toml` 프로젝트 로컬 설정 파일 역시 같은 worktree 주소로 갱신 적용.
  - `.claude/settings.local.json`에 파이썬 검증 명령들(`python -m pytest`, `python -m ruff`, `python -m mypy` 등)의 로컬 자동 승인 권한을 상세하게 추가.
- **에이전트 가이드 문서 생성**:
  - `CLAUDE.md`: 세션 연속성과 빠른 검증 가이드를 위한 루트 진입점 문서 신설.
  - `SKILL.md`: 이 프로젝트가 다루는 데이터셋의 경계, 엄격한 DO NOT 8개 규칙, 자주 묻는 작업 시작 파일 모음과 도메인 어휘를 규정한 가이드 신설.
- **docs 디렉토리 고도화**:
  - `docs/architecture.md`: 단방향 패키지 종속성, Pydantic v2 스키마 설계 및 Coercion 규칙, HTTP 200 속 에러 핸들링, 비밀값 redaction, 오프라인 Replay 테스트 아키텍처를 상세 정리한 아키텍처 문서 신설.
  - `docs/dev-environment.md`: venv 가상환경 구축, 한글 인코딩 깨짐을 우회하는 PowerShell 환경 변수 셋업 명령, 로컬 4대 게이트 검증법을 기록한 개발자 문서 신설.
  - `docs/resume.md`: 프로젝트 현재 진척도와 알려진 함정(PowerShell UTF-8, API 키 유출, DNS 미해석 등)을 명시한 상태 요약 문서 신설.
- **기존 문서 리팩토링**:
  - `docs/journal.md`: maplibre-vworld-js 프로젝트 표준 역시간순 상세 양식으로 리모델링 완료.
  - `docs/tasks.md`: `T-NNN` 테스크 상태를 정리하고 이번 통합 작업을 Done으로 갱신.
  - `docs/decisions.md`: ADR-1을 컨텍스트, 결정, 근거, 결과+, 결과-, 후속의 표준 의사결정 포맷으로 전면 개편.

**검증**:
- **로컬 품질 게이트 통과**: `compileall`, `pytest`, `ruff`, `mypy` 모두 Success.
- **Git Flow 제어 검증**: 피처 브랜치 커밋 및 master 병합 완료.

**다음 작업**: 해당 변경 내용을 `master` 브랜치에 merge 및 통합 완료.

---

## 2026-05-30 (프로젝트 초기 스타일 및 MCP 통합 정리 - T-001 기안)

**작업**: 에이전트 간 맥락 단절을 줄이기 위해 `maplibre-vworld-js` 프로젝트의 스타일 양식을 프로젝트에 기안 및 신규 도입함.

**구현 상세**:
- `docs/tasks.md`, `docs/journal.md`, `docs/decisions.md`를 신규 도입하고, 의사결정 ADR-1을 등록함.

**다음 작업**: 설정 도입 상세 이식 및 에이전트 가이드 문서 작성.
