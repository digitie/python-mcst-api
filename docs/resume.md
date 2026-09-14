# 현재 상태

2026-09-14 T-006: canonical 비동기 클라이언트, 공유 AsyncTokenBucket,
네이티브 RustFS PUT, 파일 취소 정리, UI/문서 전환을 구현했다.
카탈로그 39개와 도메인 인자/모델 계약을 보존했다.

오프라인80+14subtests, mypy17/ruff/compile, 독립 적대적 리뷰2인 통과.
리뷰 후 최종live21pass/1fail/2skip: 어린이 서점 다운로드 링크 실패,
KCISA 클래스/액티비티 HTTP403. 403에 대한 사용자 판단까지 머지를 보류한다.
세부 증거는 [검증 기록](verification-async-tps.md)을 따른다.
