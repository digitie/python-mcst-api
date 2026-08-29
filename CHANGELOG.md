# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Fixed
- 4인 전문 리뷰어 서브에이전트의 적대적 코드 리뷰로 발견·검증된 버그 수정: `resolve_file_url()`/
  `download()`/`save()`가 `DatasetKind.LINK` 카탈로그 항목(관광단지·관광특구·추천여행지·전통사찰·
  문화기반시설·등록공연장 등 6종)을 가드하지 않아 실제 CSV 대신 HTML 안내 페이지를 그대로 저장하던
  문제(`iter_csv()`/`read_csv()`는 이미 가드하고 있어 불일치였음), 다운로드된 바이트가 zip 컨테이너인
  경우를 전혀 감지하지 않아 `UnicodeDecodeError`로 크래시하거나 더 나쁘게는 손상된 CSV를 조용히
  파싱하던 문제(zip 매직바이트 감지 후 CSV 멤버 추출 추가) 등. GitHub Actions CI(`lint`/`typecheck`/
  `test`) 추가.
- `HttpClient`/`AsyncHttpClient.get_response`가 빈 `params`(빈 dict)도 httpx에 명시 전달해 **URL 자체의 query string이 통째로 대체(박탈)**되던 결함 수정 (#9). 파일 다운로드 상세페이지처럼 query가 URL에 박힌 호출이 빈 셸 페이지를 받아 `extract_download_url`이 전부 실패했다 — 빈 params는 전달하지 않는다. httpx 의미론 모사 fake 회귀 테스트 추가. 수정 후 파일 카탈로그 15종 전수 live 다운로드 검증(2026-06-12).

### Added
- CSV 파일 다운로드 카탈로그 신설 (#6, #7): `CULTURE_FILE_DATASETS` 14종 + `LIBRARY_FILE_DATASETS`. 파일명에 업로드 일시가 박힌 최신 CSV 링크를 다운로드 시점에 해석하는 `extract_download_url`/`resolve_file_url`(동기/비동기) 추가 — culture.go.kr `filedatDtl.do`(`fnFileDwld`)와 data.go.kr `fileData.do`(`fileDownload.do`) 스크레이핑, 한글/공백 query percent-encoding 정규화, 고정 `file_url` 폴백, 미해석 시 `McstParseError`. 실 다운로드 페이지 HTML fixture 기반 `tests/test_file_download.py` 신설.
- S3 호환 객체 저장소인 RustFS에 로컬 저장과 함께 데이터를 적재하는 `save_rustfs` API를 `FileDataClient` 및 `AsyncFileDataClient`에 추가.
- `boto3` 라이브러리의 런타임 동적 임포트(Dynamic Import)를 지원하여 패키지 경량성 및 하위 호환성 유지.
- `maplibre-vworld-js` 프로젝트의 MCP 에이전트 설정 파일(`antigravity.json`, `claude.json`, `codex.json`, `.gemini/`, `.claude/`, `.codex/`) 도입.
- 작업 연속성 보장을 위한 `journal.md`, `tasks.md`, `decisions.md` 도입 및 `AGENTS.md` 갱신.
- `leisure_classes` (전국 문화 여가 활동 시설(클래스)) OpenAPI 및 `recommended_travel_destinations` (추천여행지) OpenAPI 추가 (T-002).
- 동기/비동기 `CultureOpenApiClient`에 위의 신규 API 단축 헬퍼 메서드 추가.

### Changed
- KCISA OpenAPI(`api.kcisa.kr`)는 공인 DNS 미해석 + KCISA 전용 발급 키 요구(#6)로 culture/도서관 데이터의 주요 수급 경로를 서비스키가 필요 없는 CSV 파일 다운로드로 전환 (#7). `CULTURE_OPEN_APIS`는 명세 참고용으로 강등, `CultureOpenApiClient`에서 파일 전용 이동 3종(multilingual_guide/small_theaters/meeting_seminar) 헬퍼 제거, `DataGoFileApiClient`는 ODCloud 식별자 보유 항목(`public_libraries`) 전용으로 정리.
- HTTP 전송 레이어 및 공개 클라이언트에 개별 요청별 동적 `timeout` 파라미터 전달 체인 구축 (T-003).
- 일시적 공공 서버 과부하 상황에 대비해 `_sleep_before_retry`에 Full Jitter(0%~10%) 백오프 적용 (T-003).
