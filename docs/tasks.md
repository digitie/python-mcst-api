# TASKS — 작업 관리

본 문서는 프로젝트의 작업 백로그와 진행 상황을 투명하게 추적합니다. 완료된 작업은 하단으로 이동시킵니다.

---

## 진행 중인 작업 (In Progress)

- (현재 진행 중인 작업이 없습니다. 새로운 작업 시작 시 T-NNN 번호를 추가하고 이 섹션으로 이관하십시오.)

---

## 백로그 (Backlog)

- [ ] **T-003: 카탈로그 누락 API 확인 및 신규 스키마 보완**
  - 문화체육관광부에서 추가로 공개한 공공 데이터셋 중, 관광/여가 테마에 부합하는 항목이 있는지 catalog.md와 대조 분석.
  - 신규 스키마 개발 및 models.py 통합, replay용 fixture 덤프 확보.
- [ ] **T-004: _http 엔진의 재시도 백오프 지수 및 타임아웃 튜닝**
  - KCISA/data.go.kr 서버의 극심한 부하 상황 시 408/504 타임아웃 에러를 미연에 방지하기 위한 transport level 최적화.
  - dynamic client timeout 제어 prop 노출 검토.

---

## 완료된 작업 (Done)

- [x] **T-002: 워크트리 Prefix 변경 및 물리적 에이전트 독립 환경 구축**
  - **일자**: 2026-05-31
  - **내용**: 각 에이전트 환경의 prefix를 `python-mcst-api-*`로 전면 교체 완료 및 로컬 Windows 터미널에서 3개의 worktree를 실제로 생성하고 `codegraph init`까지의 완벽한 인덱싱 초기화를 이룩함.
- [x] **T-001: maplibre-vworld-js 스타일 및 MCP 설정 전면 이식**
  - **일자**: 2026-05-31
  - **내용**: 에이전트별 독립 worktree 연동을 위한 JSON/TOML 설정 전면 갱신, CLAUDE.md 및 SKILL.md 가이드 신설, docs 디렉토리 하위 아키텍처/개발환경/상태요약 신설 및 저널/테스크/ADR 포맷 개편 완수.
