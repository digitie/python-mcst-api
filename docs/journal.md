# JOURNAL — 작업 일지

새 항목은 항상 파일 맨 위에 추가(역시간순). 기존 항목은 절대 수정하지 않는다 — 잘못된 결정조차 기록으로 남는 것이 가치다.

---

## 2026-05-31 (T-005 — Windows Git 사용 원칙 명시 및 CodeGraph 제외 정리)

**작업**: worktree 환경에서 WSL `git`이 Windows 경로 기반 `.git` 포인터를 안정적으로 해석하지 못하는 문제를 피하기 위해, Windows Git 사용 원칙을 문서에 명시하고 `.codegraph/`를 버전 관리 대상에서 제외하였다.

**구현 상세**:
- `.gitignore`에 `.codegraph/`를 추가하여 CodeGraph 인덱스 산출물이 추적되지 않도록 정리함.
- `AGENTS.md`, `README.md`, `CLAUDE.md`, `SKILL.md`, `docs/dev-environment.md`에 이 저장소 worktree에서는 WSL 기본 `git` 대신 Windows Git (`git.exe`)를 사용해야 한다는 운영 규칙을 추가함.
- `docs/dev-environment.md`에는 `git.exe` 기준 예시 명령을 추가하여 브랜치 생성과 상태 조회 절차를 바로 따라 할 수 있게 정리함.

**검증**:
- Windows Git 경로 확인: `/mnt/c/Program Files/Git/cmd/git.exe`
- worktree 상태 조회는 Windows 경로를 직접 해석할 수 있는 Git 사용을 전제로 문서와 설정이 일치하는지 확인함.

**다음 작업**: 변경 사항을 검토한 뒤 PR 생성 및 merge 진행.

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
