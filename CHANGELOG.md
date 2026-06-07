# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- S3 호환 객체 저장소인 RustFS에 로컬 저장과 함께 데이터를 적재하는 `save_rustfs` API를 `FileDataClient` 및 `AsyncFileDataClient`에 추가.
- `boto3` 라이브러리의 런타임 동적 임포트(Dynamic Import)를 지원하여 패키지 경량성 및 하위 호환성 유지.
- `maplibre-vworld-js` 프로젝트의 MCP 에이전트 설정 파일(`antigravity.json`, `claude.json`, `codex.json`, `.gemini/`, `.claude/`, `.codex/`) 도입.
- 작업 연속성 보장을 위한 `journal.md`, `tasks.md`, `decisions.md` 도입 및 `AGENTS.md` 갱신.
- `leisure_classes` (전국 문화 여가 활동 시설(클래스)) OpenAPI 및 `recommended_travel_destinations` (추천여행지) OpenAPI 추가 (T-002).
- 동기/비동기 `CultureOpenApiClient`에 위의 신규 API 단축 헬퍼 메서드 추가.

### Changed
- HTTP 전송 레이어 및 공개 클라이언트에 개별 요청별 동적 `timeout` 파라미터 전달 체인 구축 (T-003).
- 일시적 공공 서버 과부하 상황에 대비해 `_sleep_before_retry`에 Full Jitter(0%~10%) 백오프 적용 (T-003).
