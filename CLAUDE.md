# CLAUDE.md — 프로젝트 컨텍스트

이 파일은 에이전트가 매 세션 시작 시 자동으로 읽어 프로젝트 상태를 파악하는 문서입니다.
프로젝트 규칙은 `AGENTS.md`에, 상세 설계는 `docs/architecture.md`에 있습니다.
이 파일은 **현재 상태**와 **세션 간 연속성**에 집중합니다.

## 프로젝트 현황 (2026-05-30)

문화체육관광부 및 산하기관이 제공하는 여가, 관광, 체육, 도서관 위치 데이터 등 일부 공공데이터/API를 다루는 작은 타입 지정 Python 패키지입니다.
Pydantic v2 및 httpx를 기반으로 하며, downstream이 직접 사용할 수 있는 안정된 typed client 및 모델을 제공합니다.
현재 오프라인 테스트 및 live 테스트 구조가 완전히 수립되어 있으며, mypy strict 정적 검사와 ruff 린트 검사가 완전 통과(Success) 상태를 유지하고 있습니다.

### 현재 작업

- T-001: 프로젝트 초기 스타일 및 MCP 통합 정리 (진행 중)

### 잔존 기술 부채

- (없음 — 새 부채가 발견되면 `docs/tasks.md`에 T-NNN으로 등록합니다)

### 브랜치 상황

- `chore/apply-mcp-and-style`: 이 스타일과 MCP 설정을 적용 중인 피처 브랜치 (작업 완료 후 `master`로 병합 예정).

## 에이전트 worktree + CodeGraph

각 에이전트는 독립된 checkout 환경을 활용하여 브랜치 및 인덱스 충돌을 방지합니다.
- ChatGPT Codex: `F:\dev\python-mcst-api-codex`
- Claude Code: `F:\dev\python-mcst-api-claude`
- Google Antigravity 2.0: `F:\dev\python-mcst-api-antigravity`

새 작업 시 해당 worktree에서 `git fetch` 후 `git switch -c agent/<topic> master`로 브랜치를 생성합니다.
CodeGraph는 worktree마다 최초 1회 `codegraph init -i`를 실행하고, 이후에는 작업 시작마다 `codegraph sync`를 실행해 인덱스를 최신화합니다. `.codegraph/` 폴더는 gitignore 대상입니다.

## 로컬 개발 환경

```
F:\dev\python-mcst-api\
├── src/                # 라이브러리 소스 코드
│   └── mcst/
│       ├── catalog.py  # 지원하는 데이터셋 카탈로그 단일 기준
│       ├── _http.py    # httpx 세션, 재시도, 오류 매핑
│       ├── _convert.py # 응답 변환 유틸리티
│       ├── models.py   # Pydantic 응답 모델
│       └── client.py   # 통합 편리한 공개 클라이언트
├── tests/              # pytest 테스트 스위트
└── docs/               # 설계, 결정 기록, 작업 저널 등
```

- **파이썬 버전**: Python >= 3.11
- **인코딩 설정**: Windows PowerShell에서 한글 인코딩 깨짐 방지를 위해 아래 환경 변수 설정을 먼저 실행합니다.
  ```powershell
  $OutputEncoding = [System.Text.UTF8Encoding]::new()
  [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
  ```

## 빠른 검증 명령

PR을 올리거나 머지하기 전에 작업자는 로컬에서 반드시 다음 4대 검증을 완수해야 합니다 (GitHub Actions는 보조적이며, 로컬 게이트 통과가 우선입니다).

```bash
# 1. 컴파일 에러 체크
python -m compileall src/mcst tests

# 2. 단위/오프라인 테스트 구동
python -m pytest

# 3. 코드 린트 및 스타일 포맷 검사
python -m ruff check .

# 4. strict 타입 정적 검사
python -m mypy src/mcst

# (선택) 실제 공공 API 서버 통신 상태 검증 (KEY가 환경 변수에 있을 때만 실행)
python -m pytest -m live
```

## 주요 결정 사항

- **ADR-1**: `maplibre-vworld-js` 에이전트 협업 스타일(저널, 테스크, ADR) 및 MCP 독립 worktree 환경 도입.

상세는 `docs/decisions.md`를 참고하십시오.

## 작업 후 의무사항

작업자는 작업을 종료하기 전에 아래 5대 의무를 반드시 이행해야 합니다.
1. `docs/journal.md`에 항목 추가 (날짜, 요약, 구현 상세, 검증, 다음 작업 - 역시간순)
2. `docs/tasks.md`의 테스크 상태 갱신 (완료는 Done 섹션 이동)
3. 새로운 아키텍처 결정이 있었다면 `docs/decisions.md`에 ADR 추가
4. 사용자 가시적인 변경이 있었다면 `CHANGELOG.md` 갱신
5. 로컬 검증 명령이 100% 성공 상태인지 다시 확인
