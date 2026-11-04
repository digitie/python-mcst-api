## 2026-11-04 — T-007 진행 중

Map #1441/Pinvi #643: data.go.kr 현재 파일 승인 경로와 ZIP 본 CSV 선택을 복구한다.
초안 PR 우선·실패 우선 회귀·WSL 기준선·독립 적대적 리뷰 두 명·CI 후 병합한다.
기준선 오프라인 80개/14 subtest와 compile/Ruff/mypy 17파일 통과.
현재는 구현 전이며 운영 환경은 접근하지 않는다.

# 현재 상태

2026-09-14 T-006: canonical 비동기 클라이언트, 공유 AsyncTokenBucket,
네이티브 RustFS PUT, 파일 취소 정리, UI/문서 전환을 구현했다.
카탈로그 39개와 도메인 인자/모델 계약을 보존했다.

오프라인80+14subtests, mypy17/ruff/compile, 독립 적대적 리뷰2인 통과.
리뷰 후 최종live21pass/1fail/2skip: 어린이 서점 다운로드 링크 실패,
KCISA 클래스/액티비티 HTTP403. 403에 대한 사용자 판단까지 머지를 보류한다.
세부 증거는 [검증 기록](verification-async-tps.md)을 따른다.
