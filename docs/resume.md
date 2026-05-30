# RESUME — 프로젝트 상태 및 진척도 요약

이 문서는 에이전트가 세션 복원 후 현재 어디까지 구현이 진행되었고, 바로 다음에 이어서 해결해야 할 작업이 무엇인지를 즉각 알 수 있게 돕는 퀵 서머리 문서입니다.

---

## 1. 현재 진척도

이 저장소는 문화체육관광부 공공데이터 API를 위한 엄격한 타입의 Python 패키지로 구축되어 있습니다.
현재 `McstClient`를 통한 문화정보원(KCISA) 및 공공데이터포털(ODCloud) API 통신 기능의 코어가 완성되었으며, 높은 테스트 신뢰성과 타입 안정성을 확보하고 있습니다.

- **완료된 주요 이정표**:
  - `mcst.catalog`에 기반한 대상 데이터셋 범위 기준 확립.
  - `httpx.AsyncClient` 기반의 마스킹 기능과 재시도 복원력을 갖춘 공통 `_http` 엔진 구축.
  - 저장된 raw response mockup(`tests/fixtures/**/*.json`)을 재생하여 파서 정합성을 100% 보장하는 Replay 테스트 완성.
  - 엄격한 mypy 타입 체킹 및 ruff 린트 규격 정착.
  - `maplibre-vworld-js` 프로젝트의 고도화된 에이전트 협업 체계(T-NNN 관리, 저널, ADR) 및 MCP 설정 전면 이식 완료.

---

## 2. 다음 한 작업 (Next Action)

현재 대기 중이거나 즉시 이어서 실행해야 하는 우선순위 1순위 작업 목록입니다.

1. **프로젝트 MCP 환경 완전 구동**:
   - `mcst-claude`, `mcst-antigravity`, `mcst-codex` 고정 worktree 생성 및 에이전트 연동 상태 확인.
   - `codegraph init -i` 및 `codegraph sync`를 이용해 이 파이썬 패키지의 소스 코드에 대한 코드 그래프 인덱싱 수행.
2. **카탈로그 신규 데이터셋 추가 및 테스트 보완**:
   - 문체부의 누락된 핵심 여가/숙박 데이터셋이 존재할 경우 `mcst.catalog`에 신규 추가 후 대응 모델 및 클라이언트 작성.

---

## 3. 알려진 함정 (Known Pitfalls)

에이전트가 작업 중 실수하기 쉬운 주요 함정 목록입니다.

> [!WARNING]
> - **PowerShell UTF-8 깨짐 함정**: Windows Powershell의 출력 인코딩이 UTF-8로 정합되지 않은 상태에서 `python -m pytest` 등을 돌리다 오류가 나면, 한글이 깨진 덤프를 보게 되어 디버깅에 큰 지장을 받습니다. 반드시 터미널 구동 시 `[Console]::OutputEncoding`을 강제 설정해두십시오.
> - **API 키 평문 커밋 함정**: `tests/fixtures/` 아래의 mock JSON을 수동으로 저장하거나 만들 때, 실서버 응답 페이로드 내에 포함되어 있던 인증용 API 키 값이 여과 없이 포함되는 일이 없도록 visual inspection을 수행해 키 값을 소각하십시오.
> - **KCISA DNS 확인 불가 함정**: 회사 사내망 환경이나 일시적인 네트워크 제한으로 `api.kcisa.kr` DNS 해석이 불가한 경우, KCISA 관련 live 테스트는 skip 처리되도록 테스트 케이스 가드를 면밀히 유지하십시오.
