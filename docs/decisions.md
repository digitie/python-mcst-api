# 아키텍처 결정 기록 (Architecture Decision Records)

이 프로젝트의 주요 설계 결정을 기록합니다.

## 목차
- [ADR-1: maplibre-vworld-js 스타일의 문서화 및 MCP 환경 도입](#adr-1-maplibre-vworld-js-스타일의-문서화-및-mcp-환경-도입)

---

### ADR-1: maplibre-vworld-js 스타일의 문서화 및 MCP 환경 도입
- **일자**: 2026-05-30
- **상태**: Accepted
- **컨텍스트**: 다른 프로젝트(`maplibre-vworld-js`)에서 입증된 안정적인 에이전트 작업 스타일(journal, tasks, decisions 문서화)과 MCP 설정(`claude.json`, `codex.json` 등)을 공통으로 도입하여 에이전트 간 맥락 단절을 줄이고 일관된 환경을 유지하고자 함.
- **결정**: `docs/journal.md`, `docs/tasks.md`, `docs/decisions.md`를 신규 도입하고 `AGENTS.md`에 이 의무사항을 명시함. 기존 MCP 설정 파일들 역시 복사하여 프로젝트 루트에 둠.
- **결과**: 향후 에이전트는 작업을 마치기 전에 위 세 개의 문서를 업데이트하는 것을 원칙으로 함.
