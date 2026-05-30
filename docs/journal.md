# JOURNAL — 작업 일지

새 항목은 항상 파일 맨 위에 추가(역시간순). 기존 항목은 절대 수정하지 않는다 — 잘못된 결정조차 기록으로 남는 것이 가치다.

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
- **로컬 품질 게이트 통과**:
  - `python -m compileall src/mcst tests` -> Success.
  - `python -m pytest` -> 21 Passed, 3 Skipped (Live 테스트).
  - `python -m ruff check .` -> All checks passed.
  - `python -m mypy src/mcst` -> Success (no issues found).
- **Git Flow 제어 검증**:
  - `chore/apply-mcp-and-style` 피처 브랜치 생성 및 정상적으로 모든 갱신 파일들을 스테이징하여 커밋. 이후 `master`에 안전하게 머지 예정.

**다음 작업**: 해당 변경 내용을 `master` 브랜치에 merge 및 통합 완료.

---

## 2026-05-30 (프로젝트 초기 스타일 및 MCP 통합 정리 - T-001 기안)

**작업**: 에이전트 간 맥락 단절을 줄이기 위해 `maplibre-vworld-js` 프로젝트의 스타일 양식을 프로젝트에 기안 및 신규 도입함.

**구현 상세**:
- `docs/tasks.md`, `docs/journal.md`, `docs/decisions.md`를 신규 도입하고, 의사결정 ADR-1을 등록함.

**다음 작업**: 설정 도입 상세 이식 및 에이전트 가이드 문서 작성.
