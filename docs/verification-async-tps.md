# 비동기 전용 및 TPS 검증

기준: origin/master `99bcb26964c552c82e02f814b43f4f438eb05d2b`.
canonical 비동기 클라이언트와 동일 AsyncTokenBucket을 적용했다.
공개 카탈로그 39개와 도메인 인자/모델 계약을 보존했다.

## 로컬 검증

- 오프라인 pytest: 80 passed, 14 subtests passed. 기본 실행 live 24개 skip.
- RuntimeWarning을 오류로 처리했다. ruff, mypy 17파일, compileall 통과.
- CodeGraph 21개 변경파일 동기화, 522노드.
- 독립 리뷰 A: 24개 전송/취소/서명 검증 승인. 실제 wire HMAC,
  요청마다 토큰 소비, 반복 취소 정리, 세션 소유권을 확인했다.
- 독립 리뷰 B: 모의 요청 26개와 문서 main 6개 실행 승인.
  from_env 인자 복원, 카탈로그/페이지/NO_DATA/CSV/ZIP/모델 계약 확인.
- 두 리뷰에서 지적한 RustFS 서명, 환경 변수 인자, quota22 우선순위,
  live 성공 판정 문제를 수정했다. 마지막 live 테스트 호출/형식 교정은 별도 재검토했다.

## 실제 서비스 검증

두 리뷰 후 2026-09-14에 로컬 키를 출력하지 않는 runner로 실행했다.
최초 결과는 11 passed / 11 failed / 2 skipped이며 전체 성공으로 집계하지 않았다.
ODCloud 공공도서관의 데이터 호출은 성공했으나 잘못 사용한 최상위 debug 라우팅을
`data_go.debug_request`로 교정했다. 파일 2개는 원본이 XLSX/HWPX임을 확인하여
CSV 파싱 대신 공개 download와 ZIP marker/CRC를 검사하도록 교정했다.

새 HTTP403이 있으므로 **머지를 보류**한다. 사용자의 기존 예외 승인에 포함되지 않는다.

| API | 실제 응답 |
| --- | --- |
| KCISA 전국 문화 여가 활동 시설 클래스 (`leisure_classes`) | HTTP403, 인증키 무효/만료/폐기 |
| KCISA 전국 문화 여가 활동 시설 액티비티 (`leisure_activity_facilities`) | HTTP403, 인증키 무효/만료/폐기 |

KCISA 테스트는 명확한 사유와 함께 skip했으며, 데이터 조회 성공으로 계산하지 않았다.
최초 파일 실패 중 7건은 big.kcisa.kr DNS 실패, children_bookstores_csv는
상세페이지에서 다운로드 링크를 찾지 못했다. 이는 HTTP403과 별개로 기록한다.
public_sports_facilities는 XLSX, registered_sports_businesses는 HWPX 원본이다.
해당 원본 다운로드와 컨테이너 CRC는 진단 실행에서 정상임을 확인했다.
실제 RustFS PUT은 실행하지 않았으며 모의 전송과 독립 서명 재계산으로 검증했다.

최종 재실행 결과는 아래에 기록한다.


### 최종 재실행

마지막 테스트 교정도 두 리뷰어가 재승인한 후 다시 실행했다.
**21 passed / 1 failed / 2 skipped**, 32.70초.

- ODCloud 공공도서관 조회와 해당 하위 클라이언트 debug: 1 passed(실제 HTTP 2회).
- CSV 19개 중 18 passed, children_bookstores_csv 1 failed(다운로드 링크 없음).
- XLSX/HWPX 다운로드와 marker·CRC: 2 passed.
- KCISA 클래스·액티비티: 각각 HTTP403으로 2 skipped. 위 보류 판단을 유지한다.
- 최초 DNS 실패 7개는 재실행에서 모두 성공했다.

모든 API/파일이 사용 가능하다는 뜻은 아니다. 새 403과 어린이 서점 링크 문제는
남아 있으며, RustFS 원격 쓰기는 실행하지 않았다. 원본 F:/dev checkout에는
미머지 제품 변경을 반영하지 않았다. 원시 로그는 작업 workspace의
verification/mcst-live-e2e.log와 mcst-live-e2e-final.log에 인증값을 마스킹해 저장했다.
