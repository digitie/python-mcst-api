# culture.go.kr 전체 목록 조사표

수집 기준: 2026-05-09 06:26 KST

이 문서는 문화공공데이터광장(culture.go.kr)의 OpenAPI 목록과 파일데이터 목록을 카테고리별로 읽어 `pymcst`의 현재 구현 여부를 대조한 조사표입니다. 현재 라이브러리는 여행, 여가, 숙박, 문화시설, 축제/행사, 도서관 위치/운영 정보에 맞춘 선별 구현이며, 향후 같은 방식으로 culture.go.kr의 다른 데이터셋과 API로 확장할 수 있습니다.

확장 시에는 `pymcst.catalog`에 원천 항목을 등록하고, OpenAPI는 `CultureClient`, 파일데이터는 `FileDataClient` 또는 자동변환 API 클라이언트에 메서드를 추가합니다. 한국관광공사 제공서비스, 문화체육관광부 및 산하기관 범위 밖 자료, 도서관 소장자료/서지/ISBN/추천도서 계열은 계속 제외 대상으로 둡니다.

## 원천

| 구분 | URL |
| --- | --- |
| OpenAPI 전체 목록 | [https://www.culture.go.kr/data/openapi/openapiList.do](https://www.culture.go.kr/data/openapi/openapiList.do) |
| 파일데이터 전체 목록 | [https://www.culture.go.kr/data/filedat/filedatList.do](https://www.culture.go.kr/data/filedat/filedatList.do) |
| 관광 파일데이터 목록 | [https://www.culture.go.kr/data/filedat/filedatList.do?category=D](https://www.culture.go.kr/data/filedat/filedatList.do?category=D) |

## 카테고리 요약

파일데이터는 일부 카테고리에서 사이트 상단의 총건수 배지와 실제 페이지 행 수가 다릅니다. 표의 `행 수`는 이 문서가 실제로 파싱한 목록 행 기준입니다.

| 코드 | 카테고리 | OpenAPI 배지 | OpenAPI 행 수 | 파일 배지 | 파일 행 수 | 구현된 API | 구현된 파일/링크 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `A` | 문화예술 | 137 | 137 | 137 | 137 | 0 | 0 |
| `B` | 문화유산 | 74 | 74 | 76 | 76 | 0 | 0 |
| `C` | 문화산업 | 84 | 84 | 84 | 84 | 6 | 3 |
| `D` | 관광 | 28 | 28 | 26 | 28 | 6 | 1 |
| `E` | 체육 | 38 | 38 | 38 | 38 | 0 | 0 |
| `F` | 도서 | 31 | 31 | 31 | 31 | 0 | 0 |
| `G` | 정책지원 | 20 | 20 | 20 | 20 | 0 | 0 |
| `H` | 문화홍보 | 7 | 7 | 9 | 9 | 0 | 0 |
| `I` | 맞춤형 API | 39 | 39 | 38 | 39 | 0 | 0 |

## 구현 상태 요약

`확장 후보`는 제목과 설명의 위치/축제/여가 관련 키워드로 1차 분류한 값입니다. 실제 구현 전에는 제공기관, 한국관광공사 연계 여부, 필드 구조, 라이선스, 인증 방식 확인이 필요합니다.

| 구분 | 구현됨 | 링크 문서화 | 확장 후보 | 제외 | 미구현 |
| --- | ---: | ---: | ---: | ---: | ---: |
| OpenAPI | 12 | 0 | 87 | 60 | 299 |
| 파일데이터 | 3 | 1 | 97 | 60 | 301 |

## OpenAPI 전체 목록

<details>
<summary>A. 문화예술 OpenAPI 137건</summary>

| ID | 제목 | 하위분류/형식 | 구현 여부 | 비고 |
| --- | --- | --- | --- | --- |
| `661` | [국립현대미술관_이벤트 정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=661&category=A&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `658` | [국립현대미술관_입주작가자료](https://www.culture.go.kr/data/openapi/openapiView.do?id=658&category=A&gubun=A) | 개인단체 > 개인 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `655` | [영상물등급위원회_영화예고편 등급분류](https://www.culture.go.kr/data/openapi/openapiView.do?id=655&category=A&gubun=A) | 창작물 > 영화/영상 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `650` | [국립아시아문화전당_행사일정](https://www.culture.go.kr/data/openapi/openapiView.do?id=650&category=A&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `644` | [국립현대미술관_레지던시작가소식](https://www.culture.go.kr/data/openapi/openapiView.do?id=644&category=A&gubun=A) | 개인단체 > 개인 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `639` | [국립한글박물관_문화행사](https://www.culture.go.kr/data/openapi/openapiView.do?id=639&category=A&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `634` | [한국문화예술위원회_채널문장](https://www.culture.go.kr/data/openapi/openapiView.do?id=634&category=A&gubun=A) | 창작물 > 기타창작물 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `633` | [영상물등급위원회_자체등급분류 정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=633&category=A&gubun=A) | 창작물 > 영화/영상 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `626` | [한국문화예술위원회_글틴-쓰면서 뒹글](https://www.culture.go.kr/data/openapi/openapiView.do?id=626&category=A&gubun=A) | 창작물 > 창작물 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `622` | [한국문화예술위원회_문장웹진](https://www.culture.go.kr/data/openapi/openapiView.do?id=622&category=A&gubun=A) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `611` | [예술의전당_전시정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=611&category=A&gubun=A) | 행사 > 전시 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `610` | [예술의전당_종합 공연정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=610&category=A&gubun=A) | 행사 > 공연 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `606` | [한국문학번역원_한국고전문학 해외소개 칼럼](https://www.culture.go.kr/data/openapi/openapiView.do?id=606&category=A&gubun=A) | 창작물 > 기타창작물 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `604` | [한국문학번역원_한국문학도서 해외소개 리뷰(에세이, 픽션)](https://www.culture.go.kr/data/openapi/openapiView.do?id=604&category=A&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `590` | [문화체육관광부_문화광장-추천도서](https://www.culture.go.kr/data/openapi/openapiView.do?id=590&category=A&gubun=A) | 창작물 > 도서 | 제외 | 도서관 소장자료/서지 계열 |
| `582` | [예술의전당_나이대별 예매 건수](https://www.culture.go.kr/data/openapi/openapiView.do?id=582&category=A&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `580` | [문화체육관광부_문화예술공연(통합)](https://www.culture.go.kr/data/openapi/openapiView.do?id=580&category=A&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `556` | [문화체육관광부 외_기관 공연정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=556&category=A&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `501` | [대한민국예술원_예술원 유고회원](https://www.culture.go.kr/data/openapi/openapiView.do?id=501&category=A&gubun=A) | 개인단체 > 개인 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `500` | [대한민국예술원_예술원 회원](https://www.culture.go.kr/data/openapi/openapiView.do?id=500&category=A&gubun=A) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `499` | [대한민국예술원_예술논문집](https://www.culture.go.kr/data/openapi/openapiView.do?id=499&category=A&gubun=A) | 개인단체 > 개인 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `498` | [대한민국예술원_기타간행물](https://www.culture.go.kr/data/openapi/openapiView.do?id=498&category=A&gubun=A) | 개인단체 > 개인 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `497` | [대한민국예술원_예술원보](https://www.culture.go.kr/data/openapi/openapiView.do?id=497&category=A&gubun=A) | 개인단체 > 개인 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `496` | [대한민국역사박물관_특별전시](https://www.culture.go.kr/data/openapi/openapiView.do?id=496&category=A&gubun=A) | 행사 > 행사 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `487` | [국립한글박물관_전시정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=487&category=A&gubun=A) | 행사 > 행사 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `482` | [재단법인 정동극장_공연정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=482&category=A&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `481` | [재단법인 정동극장_영상자료](https://www.culture.go.kr/data/openapi/openapiView.do?id=481&category=A&gubun=A) | 창작물 > 영화/영상 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `480` | [재단법인 정동극장_프로모션](https://www.culture.go.kr/data/openapi/openapiView.do?id=480&category=A&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `467` | [예술의전당_이벤트](https://www.culture.go.kr/data/openapi/openapiView.do?id=467&category=A&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `466` | [예술의전당_아카데미](https://www.culture.go.kr/data/openapi/openapiView.do?id=466&category=A&gubun=A) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `465` | [한국문화예술회관연합회_웹진](https://www.culture.go.kr/data/openapi/openapiView.do?id=465&category=A&gubun=A) | 공지및통계 > 공지 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `464` | [한국문화예술회관연합회_꿈다락토요문화학교](https://www.culture.go.kr/data/openapi/openapiView.do?id=464&category=A&gubun=A) | 창작물 > 교육 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `463` | [한국문화예술회관연합회_예술교육](https://www.culture.go.kr/data/openapi/openapiView.do?id=463&category=A&gubun=A) | 창작물 > 교육 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `456` | [한국문화예술회관연합회_공연전시정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=456&category=A&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `436` | [예술경영지원센터_KOPIS-공연시설별통계](https://www.culture.go.kr/data/openapi/openapiView.do?id=436&category=A&gubun=A) | 창작물 > 기타창작물 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `435` | [예술경영지원센터_KOPIS-공연별통계](https://www.culture.go.kr/data/openapi/openapiView.do?id=435&category=A&gubun=A) | 창작물 > 기타창작물 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `434` | [예술경영지원센터_KOPIS-국내내한별통계](https://www.culture.go.kr/data/openapi/openapiView.do?id=434&category=A&gubun=A) | 창작물 > 기타창작물 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `433` | [예술경영지원센터_KOPIS-장르별통계](https://www.culture.go.kr/data/openapi/openapiView.do?id=433&category=A&gubun=A) | 창작물 > 기타창작물 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `432` | [예술경영지원센터_KOPIS-지역별통계](https://www.culture.go.kr/data/openapi/openapiView.do?id=432&category=A&gubun=A) | 창작물 > 기타창작물 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `431` | [예술경영지원센터_KOPIS-일별예매수및매출액](https://www.culture.go.kr/data/openapi/openapiView.do?id=431&category=A&gubun=A) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `430` | [예술경영지원센터_KOPIS-예매상황판](https://www.culture.go.kr/data/openapi/openapiView.do?id=430&category=A&gubun=A) | 창작물 > 기타창작물 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `429` | [예술경영지원센터_KOPIS-극작가목록](https://www.culture.go.kr/data/openapi/openapiView.do?id=429&category=A&gubun=A) | 창작물 > 기타창작물 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `509` | [한국예술인복지재단_자료실](https://www.culture.go.kr/data/openapi/openapiView.do?id=509&category=A&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `508` | [한국예술인복지재단_보도자료](https://www.culture.go.kr/data/openapi/openapiView.do?id=508&category=A&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `507` | [한국예술인복지재단_공지사항](https://www.culture.go.kr/data/openapi/openapiView.do?id=507&category=A&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `506` | [한국예술인복지재단_입찰공고](https://www.culture.go.kr/data/openapi/openapiView.do?id=506&category=A&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `505` | [한국예술인복지재단_사업공고](https://www.culture.go.kr/data/openapi/openapiView.do?id=505&category=A&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `483` | [재단법인 정동극장_뉴스레터](https://www.culture.go.kr/data/openapi/openapiView.do?id=483&category=A&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `461` | [한국문화예술회관연합회_자료실](https://www.culture.go.kr/data/openapi/openapiView.do?id=461&category=A&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `460` | [한국문화예술회관연합회_사진자료](https://www.culture.go.kr/data/openapi/openapiView.do?id=460&category=A&gubun=A) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `459` | [한국문화예술회관연합회_보도자료](https://www.culture.go.kr/data/openapi/openapiView.do?id=459&category=A&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `457` | [한국문화예술회관연합회_공지사항](https://www.culture.go.kr/data/openapi/openapiView.do?id=457&category=A&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `428` | [예술경영지원센터_KOPIS-축제목록](https://www.culture.go.kr/data/openapi/openapiView.do?id=428&category=A&gubun=A) | 창작물 > 기타창작물 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `427` | [예술경영지원센터_KOPIS-수상작목록](https://www.culture.go.kr/data/openapi/openapiView.do?id=427&category=A&gubun=A) | 창작물 > 기타창작물 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `426` | [예술경영지원센터_KOPIS-기획제작사목록](https://www.culture.go.kr/data/openapi/openapiView.do?id=426&category=A&gubun=A) | 창작물 > 기타창작물 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `425` | [예술경영지원센터_KOPIS-공연시설별상세정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=425&category=A&gubun=A) | 창작물 > 기타창작물 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `424` | [예술경영지원센터_KOPIS-공연시설목록](https://www.culture.go.kr/data/openapi/openapiView.do?id=424&category=A&gubun=A) | 창작물 > 기타창작물 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `423` | [예술경영지원센터_KOPIS-공연상세정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=423&category=A&gubun=A) | 창작물 > 기타창작물 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `422` | [예술경영지원센터_KOPIS-공연목록](https://www.culture.go.kr/data/openapi/openapiView.do?id=422&category=A&gubun=A) | 창작물 > 기타창작물 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `406` | [한국문화예술위원회_예술자료원 소장자료](https://www.culture.go.kr/data/openapi/openapiView.do?id=406&category=A&gubun=A) | REST+ / JSON XML | 제외 | 도서관 소장자료/서지 계열 |
| `388` | [한국문화예술위원회_DA-Arts 공연예술정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=388&category=A&gubun=A) | 창작물 > 기타창작물 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `387` | [한국문화예술위원회_예술가 정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=387&category=A&gubun=A) | 개인단체 > 개인 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `386` | [한국문화예술위원회_공연장 공연정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=386&category=A&gubun=A) | 행사 > 행사 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `363` | [한국문화예술위원회_예술자료원 소장자료](https://www.culture.go.kr/data/openapi/openapiView.do?id=363&category=A&gubun=A) | 창작물 > 도서 | 제외 | 도서관 소장자료/서지 계열 |
| `353` | [한국체육산업개발(주)_올림픽공원대관정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=353&category=A&gubun=A) | 행사 > 행사 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `341` | [강원문화재단_사진자료](https://www.culture.go.kr/data/openapi/openapiView.do?id=341&category=A&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `340` | [예술의전당_공연-기타2](https://www.culture.go.kr/data/openapi/openapiView.do?id=340&category=A&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `339` | [예술의전당_공연-음악2](https://www.culture.go.kr/data/openapi/openapiView.do?id=339&category=A&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `338` | [예술의전당_공연-디자인](https://www.culture.go.kr/data/openapi/openapiView.do?id=338&category=A&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `337` | [예술의전당_공연-기타](https://www.culture.go.kr/data/openapi/openapiView.do?id=337&category=A&gubun=A) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `336` | [예술의전당_공연-서예](https://www.culture.go.kr/data/openapi/openapiView.do?id=336&category=A&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `335` | [예술의전당_공연-미술](https://www.culture.go.kr/data/openapi/openapiView.do?id=335&category=A&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `334` | [예술의전당_공연-뮤지컬](https://www.culture.go.kr/data/openapi/openapiView.do?id=334&category=A&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `333` | [예술의전당_공연-무용](https://www.culture.go.kr/data/openapi/openapiView.do?id=333&category=A&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `332` | [예술의전당_공연-발레](https://www.culture.go.kr/data/openapi/openapiView.do?id=332&category=A&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `331` | [예술의전당_공연-연극](https://www.culture.go.kr/data/openapi/openapiView.do?id=331&category=A&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `314` | [인천문화재단 외_소속 및 산하기관 교육정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=314&category=A&gubun=A) | 창작물 > 교육 | 제외 | 문화체육관광부 및 산하기관 범위 밖 |
| `313` | [한국디자인진흥원 외_ebook 간행물](https://www.culture.go.kr/data/openapi/openapiView.do?id=313&category=A&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `312` | [한국문화관광연구원 외_학술연구](https://www.culture.go.kr/data/openapi/openapiView.do?id=312&category=A&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `286` | [재단법인국악방송_국악포커스](https://www.culture.go.kr/data/openapi/openapiView.do?id=286&category=A&gubun=A) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `287` | [재단법인국악방송_공연안내](https://www.culture.go.kr/data/openapi/openapiView.do?id=287&category=A&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `288` | [재단법인국악방송_알림](https://www.culture.go.kr/data/openapi/openapiView.do?id=288&category=A&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `289` | [재단법인국악방송_보도자료](https://www.culture.go.kr/data/openapi/openapiView.do?id=289&category=A&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `290` | [대한민국예술원_공지사항](https://www.culture.go.kr/data/openapi/openapiView.do?id=290&category=A&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `291` | [대한민국예술원_사진갤러리](https://www.culture.go.kr/data/openapi/openapiView.do?id=291&category=A&gubun=A) | 창작물 > 미술 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `292` | [대한민국예술원_사진자료](https://www.culture.go.kr/data/openapi/openapiView.do?id=292&category=A&gubun=A) | 창작물 > 미술 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `293` | [대한민국예술원_예술원소식](https://www.culture.go.kr/data/openapi/openapiView.do?id=293&category=A&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `294` | [대한민국예술원_자유게시판](https://www.culture.go.kr/data/openapi/openapiView.do?id=294&category=A&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `295` | [예술의전당_공연-오페라](https://www.culture.go.kr/data/openapi/openapiView.do?id=295&category=A&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `300` | [한국문화예술교육진흥원_기초연구](https://www.culture.go.kr/data/openapi/openapiView.do?id=300&category=A&gubun=A) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `301` | [한국문화예술교육진흥원_기타](https://www.culture.go.kr/data/openapi/openapiView.do?id=301&category=A&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `302` | [한국문화예술교육진흥원_기타자료](https://www.culture.go.kr/data/openapi/openapiView.do?id=302&category=A&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `303` | [한국문화예술교육진흥원_사진자료](https://www.culture.go.kr/data/openapi/openapiView.do?id=303&category=A&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `304` | [한국문화예술교육진흥원_영상자료](https://www.culture.go.kr/data/openapi/openapiView.do?id=304&category=A&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `305` | [한국문화예술교육진흥원_정책연구](https://www.culture.go.kr/data/openapi/openapiView.do?id=305&category=A&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `306` | [한국문화예술교육진흥원_콘텐츠개발연구](https://www.culture.go.kr/data/openapi/openapiView.do?id=306&category=A&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `307` | [한국문화예술교육진흥원_평가통계연구](https://www.culture.go.kr/data/openapi/openapiView.do?id=307&category=A&gubun=A) | 공지및통계 > 통계 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `206` | [재단법인 정동극장_공지사항](https://www.culture.go.kr/data/openapi/openapiView.do?id=206&category=A&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `204` | [예술경영지원센터_국내DB](https://www.culture.go.kr/data/openapi/openapiView.do?id=204&category=A&gubun=A) | 개인단체 > 단체 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `199` | [영상물등급위원회_공연추천](https://www.culture.go.kr/data/openapi/openapiView.do?id=199&category=A&gubun=A) | REST / JSON XML | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `194` | [대한민국역사박물관_학술행사](https://www.culture.go.kr/data/openapi/openapiView.do?id=194&category=A&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `193` | [국립현대미술관_도서자료 서지정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=193&category=A&gubun=A) | 개인단체 > 개인 | 제외 | 도서관 소장자료/서지 계열 |
| `181` | [한국공예디자인문화진흥원_매거진공예디자인](https://www.culture.go.kr/data/openapi/openapiView.do?id=181&category=A&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `179` | [한국공예디자인문화진흥원_출판물](https://www.culture.go.kr/data/openapi/openapiView.do?id=179&category=A&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `176` | [한국공예디자인문화진흥원_연구보고서](https://www.culture.go.kr/data/openapi/openapiView.do?id=176&category=A&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `175` | [한국공예디자인문화진흥원_전시도록](https://www.culture.go.kr/data/openapi/openapiView.do?id=175&category=A&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `211` | [한국문화예술위원회_아르코미술관전시](https://www.culture.go.kr/data/openapi/openapiView.do?id=211&category=A&gubun=A) | 행사 > 행사 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `220` | [(재)서울시립교향악단_공연정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=220&category=A&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `221` | [재단법인세종문화회관_공연메타정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=221&category=A&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `223` | [서귀포시_공연행사정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=223&category=A&gubun=A) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `229` | [강원문화재단_문화예술자료](https://www.culture.go.kr/data/openapi/openapiView.do?id=229&category=A&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `233` | [전주시_공연전시정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=233&category=A&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `234` | [고양문화재단_공연일정](https://www.culture.go.kr/data/openapi/openapiView.do?id=234&category=A&gubun=A) | 행사 > 행사 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `235` | [한국디자인진흥원_디자인리포트-국내리포트](https://www.culture.go.kr/data/openapi/openapiView.do?id=235&category=A&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `245` | [(재)마포문화재단_마포아트센터공연전시](https://www.culture.go.kr/data/openapi/openapiView.do?id=245&category=A&gubun=A) | 행사 > 행사 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `255` | [구로문화재단_구로아트밸리공연](https://www.culture.go.kr/data/openapi/openapiView.do?id=255&category=A&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `272` | [서울시립미술관_전시정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=272&category=A&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `137` | [국립어린이청소년도서관_전시실 정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=137&category=A&gubun=A) | 행사 > 행사 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `115` | [한국문화예술위원회_나눔티켓-공연정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=115&category=A&gubun=A) | 행사 > 행사 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `113` | [국립중앙극장_공연자료](https://www.culture.go.kr/data/openapi/openapiView.do?id=113&category=A&gubun=A) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `96` | [한국체육산업개발(주)_올림픽공원공연정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=96&category=A&gubun=A) | 행사 > 행사 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `94` | [한국문화관광연구원_연구보고서-문화예술](https://www.culture.go.kr/data/openapi/openapiView.do?id=94&category=A&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `81` | [부산국악원_공연정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=81&category=A&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `80` | [남도국악원_공연정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=80&category=A&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `79` | [민속국악원_공연정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=79&category=A&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `78` | [국립국악원_공연정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=78&category=A&gubun=A) | 행사 > 행사 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `77` | [예술경영지원센터_웹진예술경영](https://www.culture.go.kr/data/openapi/openapiView.do?id=77&category=A&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `76` | [예술경영지원센터_보도자료](https://www.culture.go.kr/data/openapi/openapiView.do?id=76&category=A&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `75` | [예술경영지원센터_국내자료실](https://www.culture.go.kr/data/openapi/openapiView.do?id=75&category=A&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `74` | [예술경영지원센터_브로드캐스트](https://www.culture.go.kr/data/openapi/openapiView.do?id=74&category=A&gubun=A) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `70` | [한국문화예술위원회_공연정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=70&category=A&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `69` | [재단법인 정동극장_보도자료](https://www.culture.go.kr/data/openapi/openapiView.do?id=69&category=A&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `68` | [한국예술종합학교_공연정보5](https://www.culture.go.kr/data/openapi/openapiView.do?id=68&category=A&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `67` | [예술의전당_공연-음악회](https://www.culture.go.kr/data/openapi/openapiView.do?id=67&category=A&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `66` | [국립중앙극장_공연예술자료아카이브](https://www.culture.go.kr/data/openapi/openapiView.do?id=66&category=A&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `51` | [한국문화예술교육진흥원_기획리포트](https://www.culture.go.kr/data/openapi/openapiView.do?id=51&category=A&gubun=A) | 공지및통계 > 공지 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `44` | [국립현대미술관_전시정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=44&category=A&gubun=A) | REST+ / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |

</details>

<details>
<summary>B. 문화유산 OpenAPI 74건</summary>

| ID | 제목 | 하위분류/형식 | 구현 여부 | 비고 |
| --- | --- | --- | --- | --- |
| `654` | [국립광주박물관_소장품_리스트](https://www.culture.go.kr/data/openapi/openapiView.do?id=654&category=B&gubun=A) | 유형유산 > 유물(소장품) | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `653` | [국립경주박물관_발간자료](https://www.culture.go.kr/data/openapi/openapiView.do?id=653&category=B&gubun=A) | 창작물 > 도서 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `651` | [국립부여박물관_교육행사_전체프로그램 목록](https://www.culture.go.kr/data/openapi/openapiView.do?id=651&category=B&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `646` | [국립국악원_소장자료(공공누리)](https://www.culture.go.kr/data/openapi/openapiView.do?id=646&category=B&gubun=A) | 창작물 > 기타창작물 | 제외 | 도서관 소장자료/서지 계열 |
| `642` | [국립청주박물관_소장품](https://www.culture.go.kr/data/openapi/openapiView.do?id=642&category=B&gubun=A) | 유형유산 > 유물(소장품) | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `630` | [국립민속박물관_한국민속대백과사전](https://www.culture.go.kr/data/openapi/openapiView.do?id=630&category=B&gubun=A) | 무형유산 > 무형문화 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `552` | [국립광주박물관 외_전시도록](https://www.culture.go.kr/data/openapi/openapiView.do?id=552&category=B&gubun=A) | 유형유산 > 유물(소장품) | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `551` | [국립중앙박물관 외_유물정보(주요유물)](https://www.culture.go.kr/data/openapi/openapiView.do?id=551&category=B&gubun=A) | 유형유산 > 유물(소장품) | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `547` | [한국문화정보원_전국 중고서점 및 운영정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=547&category=B&gubun=A) | 유형유산 > 유물(소장품) | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `545` | [국립국악원_국악연감 서비스](https://www.culture.go.kr/data/openapi/openapiView.do?id=545&category=B&gubun=A) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `540` | [국립중앙박물관 외_국립지방박물관 문화행사 통합정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=540&category=B&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `539` | [국립경주박물관 외_국립지방박물관 통합 전시 정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=539&category=B&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `504` | [한국예술인복지재단_문화소식](https://www.culture.go.kr/data/openapi/openapiView.do?id=504&category=B&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `495` | [대한민국역사박물관_교육프로그램](https://www.culture.go.kr/data/openapi/openapiView.do?id=495&category=B&gubun=A) | 창작물 > 교육 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `493` | [대한민국역사박물관_소장자료](https://www.culture.go.kr/data/openapi/openapiView.do?id=493&category=B&gubun=A) | 창작물 > 기타창작물 | 제외 | 도서관 소장자료/서지 계열 |
| `492` | [대한민국역사박물관_현대사아카이브](https://www.culture.go.kr/data/openapi/openapiView.do?id=492&category=B&gubun=A) | 창작물 > 기타창작물 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `488` | [국립한글박물관_소장자료](https://www.culture.go.kr/data/openapi/openapiView.do?id=488&category=B&gubun=A) | 유형유산 > 유물(소장품) | 제외 | 도서관 소장자료/서지 계열 |
| `484` | [국립한글박물관_문헌자료와해제](https://www.culture.go.kr/data/openapi/openapiView.do?id=484&category=B&gubun=A) | 유형유산 > 유물(소장품) | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `419` | [한국정책방송원_대한뉴스관](https://www.culture.go.kr/data/openapi/openapiView.do?id=419&category=B&gubun=A) | 창작물 > 기타창작물 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `390` | [한국정책방송원_국가기록사진](https://www.culture.go.kr/data/openapi/openapiView.do?id=390&category=B&gubun=A) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `389` | [한국정책방송원_국가기록영상](https://www.culture.go.kr/data/openapi/openapiView.do?id=389&category=B&gubun=A) | 창작물 > 기타창작물 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `364` | [한국학중앙연구원_한국학자료포털](https://www.culture.go.kr/data/openapi/openapiView.do?id=364&category=B&gubun=A) | 창작물 > 도서 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `370` | [국립국악원_국악아카이브](https://www.culture.go.kr/data/openapi/openapiView.do?id=370&category=B&gubun=A) | 창작물 > 음악 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `365` | [한국학중앙연구원_장서각디지털아카이브](https://www.culture.go.kr/data/openapi/openapiView.do?id=365&category=B&gubun=A) | 창작물 > 도서 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `355` | [국립한글박물관_아카이브](https://www.culture.go.kr/data/openapi/openapiView.do?id=355&category=B&gubun=A) | 유형유산 > 유물(소장품) | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `320` | [국립국악원_학술연구-국악이론](https://www.culture.go.kr/data/openapi/openapiView.do?id=320&category=B&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `322` | [국립국악원_학술연구-구술채록](https://www.culture.go.kr/data/openapi/openapiView.do?id=322&category=B&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `323` | [국립국악원_교육연구-국악사전](https://www.culture.go.kr/data/openapi/openapiView.do?id=323&category=B&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `324` | [국립국악원_학술연구-고서](https://www.culture.go.kr/data/openapi/openapiView.do?id=324&category=B&gubun=A) | 창작물 > 음악 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `326` | [국립국악원_학술연구-악보 및 무보](https://www.culture.go.kr/data/openapi/openapiView.do?id=326&category=B&gubun=A) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `327` | [국립국악원_학술연구-해외보급자료](https://www.culture.go.kr/data/openapi/openapiView.do?id=327&category=B&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `328` | [국립국악원_학술연구-국악원 논문집](https://www.culture.go.kr/data/openapi/openapiView.do?id=328&category=B&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `329` | [국립국악원_학술연구-영인 번역](https://www.culture.go.kr/data/openapi/openapiView.do?id=329&category=B&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `330` | [국립현대미술관_소장작품](https://www.culture.go.kr/data/openapi/openapiView.do?id=330&category=B&gubun=A) | 유형유산 > 유물(소장품) | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `318` | [국립중앙박물관 외_20개 기관 유물정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=318&category=B&gubun=A) | 유형유산 > 유물(소장품) | 제외 | 문화체육관광부 및 산하기관 범위 밖 |
| `311` | [한국콘텐츠진흥원_문화원형라이브러리-음악](https://www.culture.go.kr/data/openapi/openapiView.do?id=311&category=B&gubun=A) | 창작물 > 음악 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `265` | [유네스코한국위원회_유네스코와유산](https://www.culture.go.kr/data/openapi/openapiView.do?id=265&category=B&gubun=A) | 공지및통계 > 공지 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `260` | [한국고전번역원_고전번역서 서지정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=260&category=B&gubun=A) | 유형유산 > 유물(소장품) | 제외 | 도서관 소장자료/서지 계열 |
| `182` | [국립고궁박물관_ICT유물안내](https://www.culture.go.kr/data/openapi/openapiView.do?id=182&category=B&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `187` | [대한민국역사박물관_발간자료](https://www.culture.go.kr/data/openapi/openapiView.do?id=187&category=B&gubun=A) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `198` | [한국문화정보원_전통문화종합사이트문화상징](https://www.culture.go.kr/data/openapi/openapiView.do?id=198&category=B&gubun=A) | 무형유산 > 무형문화 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `216` | [충남대학교 도서관_기호유학고문헌정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=216&category=B&gubun=A) | 유형유산 > 유물(소장품) | 제외 | 문화체육관광부 및 산하기관 범위 밖 |
| `217` | [고려대장경연구소_고려대장경지식베이스](https://www.culture.go.kr/data/openapi/openapiView.do?id=217&category=B&gubun=A) | 유형유산 > 유물(소장품) | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `219` | [동북아역사재단_동북아역사넷](https://www.culture.go.kr/data/openapi/openapiView.do?id=219&category=B&gubun=A) | 창작물 > 기타창작물 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `222` | [지역문화교류호남재단_고문서](https://www.culture.go.kr/data/openapi/openapiView.do?id=222&category=B&gubun=A) | 유형유산 > 유물(소장품) | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `231` | [동학농민혁명기념재단_동학농민혁명종합정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=231&category=B&gubun=A) | 유형유산 > 유물(소장품) | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `238` | [서울역사박물관_유물정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=238&category=B&gubun=A) | 유형유산 > 유물(소장품) | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `250` | [민속자연사박물관_제주자연사박물관](https://www.culture.go.kr/data/openapi/openapiView.do?id=250&category=B&gubun=A) | 유형유산 > 유물(소장품) | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `253` | [한국학중앙연구원_한국향토문화전자대전](https://www.culture.go.kr/data/openapi/openapiView.do?id=253&category=B&gubun=A) | 창작물 > 도서 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `254` | [한국국학진흥원_영남사림문집](https://www.culture.go.kr/data/openapi/openapiView.do?id=254&category=B&gubun=A) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `258` | [전북대학교 박물관_호남기록문화정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=258&category=B&gubun=A) | 유형유산 > 유물(소장품) | 제외 | 도서관 소장자료/서지 계열 |
| `259` | [전쟁기념관_군사유물정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=259&category=B&gubun=A) | 유형유산 > 유물(소장품) | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `155` | [한국문화정보원_디자인문양](https://www.culture.go.kr/data/openapi/openapiView.do?id=155&category=B&gubun=A) | 유형유산 > 유물(소장품) | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `134` | [국립민속박물관_현장조사DB 정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=134&category=B&gubun=A) | 무형유산 > 무형문화 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `133` | [국립민속박물관_소장유물](https://www.culture.go.kr/data/openapi/openapiView.do?id=133&category=B&gubun=A) | 유형유산 > 유물(소장품) | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `131` | [국립민속박물관_민속아카이브 사진자료](https://www.culture.go.kr/data/openapi/openapiView.do?id=131&category=B&gubun=A) | 유형유산 > 유물(소장품) | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `84` | [문화재청_문화재정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=84&category=B&gubun=A) | 유형유산 > 유물(소장품) | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `83` | [문화재청_문화재사진정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=83&category=B&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `82` | [국립중앙박물관_e뮤지엄 유물정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=82&category=B&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `73` | [한국문화예술위원회_사이버문학관문학공모전](https://www.culture.go.kr/data/openapi/openapiView.do?id=73&category=B&gubun=A) | REST / JSON XML | 제외 | 도서관 위치/운영 정보 아님 |
| `65` | [국립공주박물관_유물정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=65&category=B&gubun=A) | 유형유산 > 유물(소장품) | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `64` | [국립진주박물관_유물정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=64&category=B&gubun=A) | 유형유산 > 유물(소장품) | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `63` | [국립춘천박물관_유물정보3](https://www.culture.go.kr/data/openapi/openapiView.do?id=63&category=B&gubun=A) | 유형유산 > 유물(소장품) | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `62` | [국립제주박물관_유물정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=62&category=B&gubun=A) | 유형유산 > 유물(소장품) | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `61` | [국립김해박물관_유물정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=61&category=B&gubun=A) | 유형유산 > 유물(소장품) | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `60` | [국립청주박물관_유물정보6](https://www.culture.go.kr/data/openapi/openapiView.do?id=60&category=B&gubun=A) | 유형유산 > 유물(소장품) | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `59` | [국립대구박물관_유물정보7](https://www.culture.go.kr/data/openapi/openapiView.do?id=59&category=B&gubun=A) | 유형유산 > 유물(소장품) | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `58` | [국립부여박물관_유물정보8](https://www.culture.go.kr/data/openapi/openapiView.do?id=58&category=B&gubun=A) | 유형유산 > 유물(소장품) | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `57` | [국립전주박물관_유물정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=57&category=B&gubun=A) | 유형유산 > 유물(소장품) | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `56` | [국립광주박물관_유물정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=56&category=B&gubun=A) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `55` | [국립경주박물관_유물정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=55&category=B&gubun=A) | 유형유산 > 유물(소장품) | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `54` | [국립중앙박물관_유물정보12](https://www.culture.go.kr/data/openapi/openapiView.do?id=54&category=B&gubun=A) | 유형유산 > 유물(소장품) | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `43` | [국립민속박물관_민속대백과사전](https://www.culture.go.kr/data/openapi/openapiView.do?id=43&category=B&gubun=A) | 무형유산 > 무형문화 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `14` | [한국문화정보원_2D개별문양목록조회](https://www.culture.go.kr/data/openapi/openapiView.do?id=14&category=B&gubun=A) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |

</details>

<details>
<summary>C. 문화산업 OpenAPI 84건</summary>

| ID | 제목 | 하위분류/형식 | 구현 여부 | 비고 |
| --- | --- | --- | --- | --- |
| `660` | [한국영상자료원_한국영화박물관 교육](https://www.culture.go.kr/data/openapi/openapiView.do?id=660&category=C&gubun=A) | 창작물 > 교육 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `656` | [한국정책방송원_프로그램 특집](https://www.culture.go.kr/data/openapi/openapiView.do?id=656&category=C&gubun=A) | 창작물 > 방송 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `649` | [게임물관리위원회_자체등급분류정보서비스](https://www.culture.go.kr/data/openapi/openapiView.do?id=649&category=C&gubun=A) | 창작물 > 기타창작물 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `648` | [한국언론진흥재단_미디어정보-정기간행물-신문과방송-호수별보기](https://www.culture.go.kr/data/openapi/openapiView.do?id=648&category=C&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `647` | [한국영상자료원_영화글(연재/기획/기관지/종료연재)](https://www.culture.go.kr/data/openapi/openapiView.do?id=647&category=C&gubun=A) | 창작물 > 영화/영상 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `645` | [한국정책방송원_정책공공](https://www.culture.go.kr/data/openapi/openapiView.do?id=645&category=C&gubun=A) | 창작물 > 방송 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `643` | [한국언론진흥재단_미디어정보-기획취재아카이브-역대보도물](https://www.culture.go.kr/data/openapi/openapiView.do?id=643&category=C&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `641` | [한국언론진흥재단_미디어정보-정기간행물-신문과방송-전체기사](https://www.culture.go.kr/data/openapi/openapiView.do?id=641&category=C&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `640` | [한국도박문제예방치유원_예방/홍보/치유재활 콘텐츠](https://www.culture.go.kr/data/openapi/openapiView.do?id=640&category=C&gubun=A) | 창작물 > 기타창작물 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `629` | [게임물관리위원회_게임등급정보서비스](https://www.culture.go.kr/data/openapi/openapiView.do?id=629&category=C&gubun=A) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `628` | [한국저작권위원회_공유마당 사진](https://www.culture.go.kr/data/openapi/openapiView.do?id=628&category=C&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `627` | [한국저작권위원회_공유마당 만료저작물](https://www.culture.go.kr/data/openapi/openapiView.do?id=627&category=C&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `624` | [한국문화정보원_카페가 있는 서점데이터](https://www.culture.go.kr/data/openapi/openapiView.do?id=624&category=C&gubun=A) | 장소 > 장소 | 구현됨 | `cafe_bookstores` |
| `623` | [한국문화정보원_전국 독립서점 및 운영정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=623&category=C&gubun=A) | 장소 > 장소 | 구현됨 | `independent_bookstores` |
| `621` | [한국영상자료원_전단지정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=621&category=C&gubun=A) | 창작물 > 영화/영상 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `596` | [한국문화정보원_전국 회의 세미나 시설정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=596&category=C&gubun=A) | 장소 > 장소 | 구현됨 | `meeting_seminar_facilities` |
| `592` | [한국문화정보원_전국 가족 유아 동반 가능 문화시설](https://www.culture.go.kr/data/openapi/openapiView.do?id=592&category=C&gubun=A) | 장소 > 장소 | 구현됨 | `family_infant_culture_facilities` |
| `589` | [한국문화정보원_전국 공유 오피스 시설](https://www.culture.go.kr/data/openapi/openapiView.do?id=589&category=C&gubun=A) | 장소 > 장소 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `588` | [한국문화정보원_전국 문화 여가 활동 시설(캠핑)](https://www.culture.go.kr/data/openapi/openapiView.do?id=588&category=C&gubun=A) | 장소 > 장소 | 구현됨 | `leisure_camping_facilities` |
| `587` | [한국문화정보원_전국 문화 여가 활동 시설(액티비티)](https://www.culture.go.kr/data/openapi/openapiView.do?id=587&category=C&gubun=A) | REST / JSON XML | 구현됨 | `leisure_activity_facilities` |
| `586` | [한국문화정보원_전국 문화 여가 활동 시설(클래스)](https://www.culture.go.kr/data/openapi/openapiView.do?id=586&category=C&gubun=A) | 창작물 > 교육 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `555` | [문화체육관광부 외_기관 교육정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=555&category=C&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `554` | [문화체육관광부 외_기관 채용정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=554&category=C&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `543` | [한국영상자료원_D시네마 정보 서비스](https://www.culture.go.kr/data/openapi/openapiView.do?id=543&category=C&gubun=A) | 창작물 > 영화/영상 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `542` | [영상물등급위원회_비디오정보 서비스](https://www.culture.go.kr/data/openapi/openapiView.do?id=542&category=C&gubun=A) | 창작물 > 영화/영상 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `537` | [한국문화정보원_전국 아동서점 운영정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=537&category=C&gubun=A) | 창작물 > 영화/영상 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `502` | [예술경영지원센터_공고-기금-행사](https://www.culture.go.kr/data/openapi/openapiView.do?id=502&category=C&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `479` | [한국언론진흥재단_연구조사서](https://www.culture.go.kr/data/openapi/openapiView.do?id=479&category=C&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `477` | [한국언론진흥재단_언론산업통계-기타분석자료](https://www.culture.go.kr/data/openapi/openapiView.do?id=477&category=C&gubun=A) | 공지및통계 > 통계 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `474` | [한국언론진흥재단_신문과방송](https://www.culture.go.kr/data/openapi/openapiView.do?id=474&category=C&gubun=A) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `471` | [한국언론진흥재단_사업결과](https://www.culture.go.kr/data/openapi/openapiView.do?id=471&category=C&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `469` | [한국언론진흥재단_공모신청](https://www.culture.go.kr/data/openapi/openapiView.do?id=469&category=C&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `439` | [한국문화정보원_기관별동의어-핵심어-표제어정리](https://www.culture.go.kr/data/openapi/openapiView.do?id=439&category=C&gubun=A) | 공지및통계 > 공지 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `404` | [한국출판문화산업진흥원_출판지원도서 우수출판콘텐츠 제작 지원 정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=404&category=C&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `385` | [영상물등급위원회_영화 등급분류 목록](https://www.culture.go.kr/data/openapi/openapiView.do?id=385&category=C&gubun=A) | 창작물 > 영화/영상 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `384` | [한국영상자료원_전시정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=384&category=C&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `282` | [국제방송교류재단_뉴스](https://www.culture.go.kr/data/openapi/openapiView.do?id=282&category=C&gubun=A) | 창작물 > 방송 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `310` | [한국출판문화산업진흥원_전문자료](https://www.culture.go.kr/data/openapi/openapiView.do?id=310&category=C&gubun=A) | 공지및통계 > 공지 | 제외 | 도서관 소장자료/서지 계열 |
| `207` | [한국저작권위원회_프로젝트기본정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=207&category=C&gubun=A) | 공지및통계 > 공지 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `267` | [한국천문연구원_천문우주정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=267&category=C&gubun=A) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `203` | [영화진흥위원회_박스오피스](https://www.culture.go.kr/data/openapi/openapiView.do?id=203&category=C&gubun=A) | 창작물 > 영화/영상 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `200` | [영화진흥위원회_영화인정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=200&category=C&gubun=A) | 개인단체 > 개인 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `190` | [대한민국역사박물관_문화행사](https://www.culture.go.kr/data/openapi/openapiView.do?id=190&category=C&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `188` | [한국영상자료원_필름정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=188&category=C&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `185` | [한국저작권위원회_OLIS오픈소스라이센스](https://www.culture.go.kr/data/openapi/openapiView.do?id=185&category=C&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `183` | [한국출판문화산업진흥원_관련법규](https://www.culture.go.kr/data/openapi/openapiView.do?id=183&category=C&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `212` | [영화진흥위원회_영화사](https://www.culture.go.kr/data/openapi/openapiView.do?id=212&category=C&gubun=A) | 개인단체 > 단체 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `163` | [한국영상자료원_영화사연구도서](https://www.culture.go.kr/data/openapi/openapiView.do?id=163&category=C&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `162` | [한국영상자료원_영화사연구DVD](https://www.culture.go.kr/data/openapi/openapiView.do?id=162&category=C&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `527` | [한국체육산업개발(주)_채용공고2](https://www.culture.go.kr/data/openapi/openapiView.do?id=527&category=C&gubun=A) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `503` | [한국예술인복지재단_채용정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=503&category=C&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `491` | [문화체육관광부_채용 정보(통합)](https://www.culture.go.kr/data/openapi/openapiView.do?id=491&category=C&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `478` | [한국언론진흥재단_전체현황](https://www.culture.go.kr/data/openapi/openapiView.do?id=478&category=C&gubun=A) | 공지및통계 > 통계 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `475` | [한국언론진흥재단_공지사항](https://www.culture.go.kr/data/openapi/openapiView.do?id=475&category=C&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `473` | [한국언론진흥재단_보도자료](https://www.culture.go.kr/data/openapi/openapiView.do?id=473&category=C&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `472` | [한국언론진흥재단_채용공고](https://www.culture.go.kr/data/openapi/openapiView.do?id=472&category=C&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `462` | [한국문화예술회관연합회_구인게시판](https://www.culture.go.kr/data/openapi/openapiView.do?id=462&category=C&gubun=A) | 공지및통계 > 공지 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `438` | [한국문화정보원_기관별QI챗봇정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=438&category=C&gubun=A) | 공지및통계 > 공지 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `437` | [한국저작권보호원_채용정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=437&category=C&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `209` | [한국출판문화산업진흥원_공지사항](https://www.culture.go.kr/data/openapi/openapiView.do?id=209&category=C&gubun=A) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `205` | [대한민국역사박물관_채용](https://www.culture.go.kr/data/openapi/openapiView.do?id=205&category=C&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `195` | [문화체육관광부_e브리핑](https://www.culture.go.kr/data/openapi/openapiView.do?id=195&category=C&gubun=A) | 창작물 > 방송 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `172` | [문화체육관광부_아카이브전문자료 정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=172&category=C&gubun=A) | 공지및통계 > 공지 | 제외 | 도서관 소장자료/서지 계열 |
| `165` | [한국정책방송원_정책문화 교양](https://www.culture.go.kr/data/openapi/openapiView.do?id=165&category=C&gubun=A) | 창작물 > 방송 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `164` | [한국정책방송원_정책뉴스 사회 문화](https://www.culture.go.kr/data/openapi/openapiView.do?id=164&category=C&gubun=A) | 창작물 > 방송 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `161` | [한국영상자료원_시나리오정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=161&category=C&gubun=A) | 창작물 > 영화/영상 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `160` | [한국영상자료원_스틸정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=160&category=C&gubun=A) | 창작물 > 영화/영상 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `159` | [한국영상자료원_비디오정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=159&category=C&gubun=A) | 창작물 > 영화/영상 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `158` | [한국영상자료원_동영상정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=158&category=C&gubun=A) | 창작물 > 영화/영상 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `156` | [한국영상자료원_논문](https://www.culture.go.kr/data/openapi/openapiView.do?id=156&category=C&gubun=A) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `157` | [한국영상자료원_도서정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=157&category=C&gubun=A) | 공지및통계 > 공지 | 제외 | 도서관 소장자료/서지 계열 |
| `127` | [한국체육산업개발(주)_사회공헌](https://www.culture.go.kr/data/openapi/openapiView.do?id=127&category=C&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `110` | [문화체육관광부_문화칼럼](https://www.culture.go.kr/data/openapi/openapiView.do?id=110&category=C&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `109` | [문화체육관광부_정책기자마당](https://www.culture.go.kr/data/openapi/openapiView.do?id=109&category=C&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `108` | [한국저작권위원회_행사일정](https://www.culture.go.kr/data/openapi/openapiView.do?id=108&category=C&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `107` | [한국저작권위원회_보도자료](https://www.culture.go.kr/data/openapi/openapiView.do?id=107&category=C&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `91` | [영화진흥위원회_영화정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=91&category=C&gubun=A) | 창작물 > 영화/영상 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `89` | [한국영상자료원_상영정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=89&category=C&gubun=A) | 창작물 > 영화/영상 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `88` | [한국영상자료원_영화정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=88&category=C&gubun=A) | 창작물 > 영화/영상 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `87` | [한국영상자료원_포스터정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=87&category=C&gubun=A) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `72` | [한국문화예술위원회_행사정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=72&category=C&gubun=A) | 행사 > 행사 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `86` | [한국영상자료원_정기간행물](https://www.culture.go.kr/data/openapi/openapiView.do?id=86&category=C&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `50` | [한국콘텐츠진흥원_콘텐츠연구보고서](https://www.culture.go.kr/data/openapi/openapiView.do?id=50&category=C&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `49` | [한국저작권위원회_저작권동향](https://www.culture.go.kr/data/openapi/openapiView.do?id=49&category=C&gubun=A) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |

</details>

<details>
<summary>D. 관광 OpenAPI 28건</summary>

| ID | 제목 | 하위분류/형식 | 구현 여부 | 비고 |
| --- | --- | --- | --- | --- |
| `595` | [한국문화정보원_전국 연극장 및 소극장 정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=595&category=D&gubun=A) | 장소 > 장소 | 구현됨 | `small_theaters` |
| `594` | [한국문화정보원_전국 세계음식점](https://www.culture.go.kr/data/openapi/openapiView.do?id=594&category=D&gubun=A) | 장소 > 장소 | 구현됨 | `world_restaurants` |
| `593` | [한국문화정보원_전국 다국어 가이드 제공 문화시설](https://www.culture.go.kr/data/openapi/openapiView.do?id=593&category=D&gubun=A) | 장소 > 장소 | 구현됨 | `multilingual_guide_culture_facilities` |
| `585` | [한국문화정보원_전국 반려동물 동반가능 문화시설 위치](https://www.culture.go.kr/data/openapi/openapiView.do?id=585&category=D&gubun=A) | 장소 > 장소 | 구현됨 | `pet_friendly_culture_facilities` |
| `584` | [한국문화정보원_전국 문화예술관광지 배리어프리 정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=584&category=D&gubun=A) | 장소 > 장소 | 구현됨 | `barrier_free_places` |
| `583` | [한국문화정보원_미디어콘텐츠 영상 내 유명지](https://www.culture.go.kr/data/openapi/openapiView.do?id=583&category=D&gubun=A) | 장소 > 장소 | 구현됨 | `media_famous_places` |
| `581` | [문화체육관광부_추천여행지](https://www.culture.go.kr/data/openapi/openapiView.do?id=581&category=D&gubun=A) | 장소 > 장소 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `541` | [한국문화관광연구원_관광지식채널 정기간행물 정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=541&category=D&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `357` | [한국체육산업개발(주)_올림픽공원장미정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=357&category=D&gubun=A) | 장소 > 장소 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `348` | [홍천군_휴양지](https://www.culture.go.kr/data/openapi/openapiView.do?id=348&category=D&gubun=A) | REST / JSON XML | 제외 | 문화체육관광부 및 산하기관 범위 밖 |
| `319` | [한국문화관광연구원 외_관광지정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=319&category=D&gubun=A) | 장소 > 장소 | 제외 | 한국관광공사 제공서비스 |
| `299` | [한국문화관광연구원_한국관광정책](https://www.culture.go.kr/data/openapi/openapiView.do?id=299&category=D&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `275` | [한국농어촌공사_체험관광마을](https://www.culture.go.kr/data/openapi/openapiView.do?id=275&category=D&gubun=A) | 장소 > 장소 | 제외 | 문화체육관광부 및 산하기관 범위 밖 |
| `271` | [종로구_공연장정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=271&category=D&gubun=A) | 장소 > 장소 | 제외 | 문화체육관광부 및 산하기관 범위 밖 |
| `262` | [한국원자력환경공단_공단시설물 정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=262&category=D&gubun=A) | 장소 > 장소 | 제외 | 문화체육관광부 및 산하기관 범위 밖 |
| `242` | [인천문화재단_지역축제](https://www.culture.go.kr/data/openapi/openapiView.do?id=242&category=D&gubun=A) | 무형유산 > 축제 | 제외 | 문화체육관광부 및 산하기관 범위 밖 |
| `241` | [부산광역시청_관광정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=241&category=D&gubun=A) | 장소 > 장소 | 제외 | 문화체육관광부 및 산하기관 범위 밖 |
| `210` | [한국관광공사_해외이미지](https://www.culture.go.kr/data/openapi/openapiView.do?id=210&category=D&gubun=A) | 무형유산 > 축제 | 제외 | 한국관광공사 제공서비스 |
| `196` | [문화체육관광부_지역축제정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=196&category=D&gubun=A) | 무형유산 > 축제 | 제외 | 한국관광공사 제공서비스 |
| `130` | [한국지역진흥재단_축제정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=130&category=D&gubun=A) | REST / JSON XML | 제외 | 문화체육관광부 및 산하기관 범위 밖 |
| `126` | [한국체육산업개발(주)_올림픽공원장미광장](https://www.culture.go.kr/data/openapi/openapiView.do?id=126&category=D&gubun=A) | 장소 > 장소 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `112` | [한국체육산업개발(주)_포토갤러리](https://www.culture.go.kr/data/openapi/openapiView.do?id=112&category=D&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `111` | [한국체육산업개발(주)_올림픽공원생태공원갤러리](https://www.culture.go.kr/data/openapi/openapiView.do?id=111&category=D&gubun=A) | 장소 > 장소 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `99` | [한국관광공사_청사초롱서비스](https://www.culture.go.kr/data/openapi/openapiView.do?id=99&category=D&gubun=A) | 공지및통계 > 공지 | 제외 | 한국관광공사 제공서비스 |
| `98` | [한국관광공사_사진갤러리](https://www.culture.go.kr/data/openapi/openapiView.do?id=98&category=D&gubun=A) | 공지및통계 > 공지 | 제외 | 한국관광공사 제공서비스 |
| `97` | [한국관광공사_관광정보-테마관광](https://www.culture.go.kr/data/openapi/openapiView.do?id=97&category=D&gubun=A) | 장소 > 장소 | 제외 | 한국관광공사 제공서비스 |
| `93` | [한국문화관광연구원_세미나자료실](https://www.culture.go.kr/data/openapi/openapiView.do?id=93&category=D&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `92` | [한국문화관광연구원_문화정책논총](https://www.culture.go.kr/data/openapi/openapiView.do?id=92&category=D&gubun=A) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |

</details>

<details>
<summary>E. 체육 OpenAPI 38건</summary>

| ID | 제목 | 하위분류/형식 | 구현 여부 | 비고 |
| --- | --- | --- | --- | --- |
| `635` | [대한체육회_체육소식](https://www.culture.go.kr/data/openapi/openapiView.do?id=635&category=E&gubun=A) | 공지및통계 > 공지 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `591` | [문화체육관광부_문화광장-체육행사](https://www.culture.go.kr/data/openapi/openapiView.do?id=591&category=E&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `553` | [문화체육관광부 외_기관 (문화)행사정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=553&category=E&gubun=A) | 행사 > 행사 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `536` | [한국체육산업개발(주)_역대수상 및 인증기록정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=536&category=E&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `535` | [한국체육산업개발(주)_협력기관정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=535&category=E&gubun=A) | 개인단체 > 단체 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `420` | [한국체육산업개발(주)_올림픽공원유실물정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=420&category=E&gubun=A) | 공지및통계 > 공지 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `402` | [국민체육진흥공단_스포츠강좌이용권강좌정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=402&category=E&gubun=A) | 창작물 > 교육 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `401` | [국민체육진흥공단_스포츠강좌이용권시설정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=401&category=E&gubun=A) | 창작물 > 교육 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `400` | [국민체육진흥공단_88서울올림픽종목별동영상자료](https://www.culture.go.kr/data/openapi/openapiView.do?id=400&category=E&gubun=A) | 창작물 > 교육 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `398` | [한국체육산업개발(주)_평생교육원교육정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=398&category=E&gubun=A) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `361` | [대한체육회_체육시설정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=361&category=E&gubun=A) | 공지및통계 > 공지 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `352` | [한국체육산업개발(주)_스포츠센터운영현황](https://www.culture.go.kr/data/openapi/openapiView.do?id=352&category=E&gubun=A) | 공지및통계 > 통계 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `351` | [한국체육산업개발(주)_올림픽공원운영현황](https://www.culture.go.kr/data/openapi/openapiView.do?id=351&category=E&gubun=A) | 공지및통계 > 통계 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `315` | [한국체육산업개발(주) 외_15개 기관 보도자료](https://www.culture.go.kr/data/openapi/openapiView.do?id=315&category=E&gubun=A) | 공지및통계 > 공지 | 제외 | 한국관광공사 제공서비스 |
| `184` | [대한장애인체육회_전국장애학생체육대회 포토갤러리](https://www.culture.go.kr/data/openapi/openapiView.do?id=184&category=E&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `153` | [국민체육진흥공단_스포츠강좌이용권시설정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=153&category=E&gubun=A) | 창작물 > 교육 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `150` | [대한체육회_행사-대회](https://www.culture.go.kr/data/openapi/openapiView.do?id=150&category=E&gubun=A) | 행사 > 행사 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `148` | [대한체육회_포토갤러리](https://www.culture.go.kr/data/openapi/openapiView.do?id=148&category=E&gubun=A) | 공지및통계 > 공지 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `147` | [대한체육회_종목소개자료실](https://www.culture.go.kr/data/openapi/openapiView.do?id=147&category=E&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `146` | [대한체육회_생활체육문헌](https://www.culture.go.kr/data/openapi/openapiView.do?id=146&category=E&gubun=A) | REST / JSON XML | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `145` | [대한체육회_생활체육뉴스](https://www.culture.go.kr/data/openapi/openapiView.do?id=145&category=E&gubun=A) | 공지및통계 > 공지 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `144` | [대한체육회_명예기자활동](https://www.culture.go.kr/data/openapi/openapiView.do?id=144&category=E&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `143` | [대한체육회_동영상서비스](https://www.culture.go.kr/data/openapi/openapiView.do?id=143&category=E&gubun=A) | 창작물 > 기타창작물 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `142` | [대한체육회_종목용어사전](https://www.culture.go.kr/data/openapi/openapiView.do?id=142&category=E&gubun=A) | 공지및통계 > 공지 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `128` | [한국체육산업개발(주)_올팍축구장정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=128&category=E&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `125` | [한국체육산업개발(주)_올림픽공원보도자료](https://www.culture.go.kr/data/openapi/openapiView.do?id=125&category=E&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `124` | [한국체육산업개발(주)_올림픽공원스포츠센터정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=124&category=E&gubun=A) | 공지및통계 > 공지 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `123` | [한국체육산업개발(주)_올림픽공원 스케이트장 정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=123&category=E&gubun=A) | 공지및통계 > 공지 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `122` | [한국체육산업개발(주)_일산올림픽스포츠센터정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=122&category=E&gubun=A) | 공지및통계 > 공지 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `121` | [한국체육산업개발(주)_올림픽수영장정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=121&category=E&gubun=A) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `120` | [한국체육산업개발(주)_올림픽공원올팍소식](https://www.culture.go.kr/data/openapi/openapiView.do?id=120&category=E&gubun=A) | 공지및통계 > 공지 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `117` | [한국체육산업개발(주)_분당올림픽스포츠센터정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=117&category=E&gubun=A) | 공지및통계 > 공지 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `116` | [한국체육산업개발(주)_공지사항](https://www.culture.go.kr/data/openapi/openapiView.do?id=116&category=E&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `285` | [대한장애인체육회_공지사항](https://www.culture.go.kr/data/openapi/openapiView.do?id=285&category=E&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `151` | [국민체육진흥공단_공지사항](https://www.culture.go.kr/data/openapi/openapiView.do?id=151&category=E&gubun=A) | 창작물 > 교육 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `141` | [대한체육회_공지사항](https://www.culture.go.kr/data/openapi/openapiView.do?id=141&category=E&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `118` | [한국체육산업개발(주)_보도자료](https://www.culture.go.kr/data/openapi/openapiView.do?id=118&category=E&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `95` | [대한장애인체육회_행사-대회정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=95&category=E&gubun=A) | REST / JSON XML | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |

</details>

<details>
<summary>F. 도서 OpenAPI 31건</summary>

| ID | 제목 | 하위분류/형식 | 구현 여부 | 비고 |
| --- | --- | --- | --- | --- |
| `652` | [국립세종도서관_새로들어온책(일반/정책/어린이)](https://www.culture.go.kr/data/openapi/openapiView.do?id=652&category=F&gubun=A) | 창작물 > 도서 | 제외 | 도서관 소장자료/서지 계열 |
| `631` | [국립어린이청소년도서관_세계의 도서관](https://www.culture.go.kr/data/openapi/openapiView.do?id=631&category=F&gubun=A) | 장소 > 장소 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `625` | [국립어린이청소년도서관_다국어동화구연 전체동화](https://www.culture.go.kr/data/openapi/openapiView.do?id=625&category=F&gubun=A) | 창작물 > 기타창작물 | 제외 | 도서관 위치/운영 정보 아님 |
| `609` | [한국문학번역원_한국문학번역 전문도서관 소장자료](https://www.culture.go.kr/data/openapi/openapiView.do?id=609&category=F&gubun=A) | 창작물 > 도서 | 제외 | 도서관 소장자료/서지 계열 |
| `608` | [한국문학번역원_한국문학번역출간 도서정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=608&category=F&gubun=A) | 창작물 > 도서 | 제외 | 도서관 소장자료/서지 계열 |
| `607` | [한국문학번역원_한국문학 작가정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=607&category=F&gubun=A) | 창작물 > 도서 | 제외 | 도서관 위치/운영 정보 아님 |
| `516` | [국립세종도서관_국내DB](https://www.culture.go.kr/data/openapi/openapiView.do?id=516&category=F&gubun=A) | 창작물 > 도서 | 제외 | 도서관 소장자료/서지 계열 |
| `468` | [국립중앙도서관_소장자료](https://www.culture.go.kr/data/openapi/openapiView.do?id=468&category=F&gubun=A) | 창작물 > 도서 | 제외 | 도서관 소장자료/서지 계열 |
| `405` | [한국체육산업개발(주)_올림픽공원도서정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=405&category=F&gubun=A) | 창작물 > 도서 | 제외 | 도서관 소장자료/서지 계열 |
| `397` | [국립중앙도서관_OAK-PORTAL](https://www.culture.go.kr/data/openapi/openapiView.do?id=397&category=F&gubun=A) | REST / JSON XML | 제외 | 도서관 위치/운영 정보 아님 |
| `391` | [국립어린이청소년도서관_다국어동화구연-한국전래동화](https://www.culture.go.kr/data/openapi/openapiView.do?id=391&category=F&gubun=A) | 공지및통계 > 공지 | 제외 | 도서관 위치/운영 정보 아님 |
| `383` | [한국출판문화산업진흥원_세종도서-문화나눔](https://www.culture.go.kr/data/openapi/openapiView.do?id=383&category=F&gubun=A) | 공지및통계 > 공지 | 제외 | 도서관 소장자료/서지 계열 |
| `382` | [한국출판문화산업진흥원_세종도서-교양](https://www.culture.go.kr/data/openapi/openapiView.do?id=382&category=F&gubun=A) | 공지및통계 > 공지 | 제외 | 도서관 소장자료/서지 계열 |
| `381` | [한국출판문화산업진흥원_세종도서-학술](https://www.culture.go.kr/data/openapi/openapiView.do?id=381&category=F&gubun=A) | 공지및통계 > 공지 | 제외 | 도서관 소장자료/서지 계열 |
| `366` | [한국출판문화산업진흥원_추천도서-대학신입생추천도서](https://www.culture.go.kr/data/openapi/openapiView.do?id=366&category=F&gubun=A) | 공지및통계 > 공지 | 제외 | 도서관 소장자료/서지 계열 |
| `362` | [국립세종도서관_사서추천도서](https://www.culture.go.kr/data/openapi/openapiView.do?id=362&category=F&gubun=A) | 공지및통계 > 공지 | 제외 | 도서관 소장자료/서지 계열 |
| `360` | [국립중앙도서관_사서추천도서2](https://www.culture.go.kr/data/openapi/openapiView.do?id=360&category=F&gubun=A) | 공지및통계 > 공지 | 제외 | 도서관 소장자료/서지 계열 |
| `359` | [한국출판문화산업진흥원_추천도서-청소년권장도서](https://www.culture.go.kr/data/openapi/openapiView.do?id=359&category=F&gubun=A) | 공지및통계 > 공지 | 제외 | 도서관 소장자료/서지 계열 |
| `358` | [한국출판문화산업진흥원_추천도서-이달의읽을만한책](https://www.culture.go.kr/data/openapi/openapiView.do?id=358&category=F&gubun=A) | 공지및통계 > 공지 | 제외 | 도서관 소장자료/서지 계열 |
| `350` | [한국체육산업개발(주)_올림픽공원도서정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=350&category=F&gubun=A) | REST / JSON XML | 제외 | 도서관 소장자료/서지 계열 |
| `308` | [한국출판문화산업진흥원_동영상](https://www.culture.go.kr/data/openapi/openapiView.do?id=308&category=F&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `192` | [국립중앙도서관_조선총독부관보](https://www.culture.go.kr/data/openapi/openapiView.do?id=192&category=F&gubun=A) | 창작물 > 도서 | 제외 | 도서관 위치/운영 정보 아님 |
| `135` | [국립어린이청소년도서관_사서추천도서](https://www.culture.go.kr/data/openapi/openapiView.do?id=135&category=F&gubun=A) | 공지및통계 > 공지 | 제외 | 도서관 소장자료/서지 계열 |
| `132` | [국립민속박물관_발간도서](https://www.culture.go.kr/data/openapi/openapiView.do?id=132&category=F&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `106` | [한국출판문화산업진흥원_독서캘린더](https://www.culture.go.kr/data/openapi/openapiView.do?id=106&category=F&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `105` | [한국출판문화산업진흥원_내가권하는한권의책](https://www.culture.go.kr/data/openapi/openapiView.do?id=105&category=F&gubun=A) | 공지및통계 > 공지 | 제외 | 도서관 소장자료/서지 계열 |
| `104` | [한국출판문화산업진흥원_독서활동-이야기](https://www.culture.go.kr/data/openapi/openapiView.do?id=104&category=F&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `103` | [한국출판문화산업진흥원_손안애서](https://www.culture.go.kr/data/openapi/openapiView.do?id=103&category=F&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `490` | [국립어린이청소년도서관_공개모집](https://www.culture.go.kr/data/openapi/openapiView.do?id=490&category=F&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `489` | [국립어린이청소년도서관_공지사항](https://www.culture.go.kr/data/openapi/openapiView.do?id=489&category=F&gubun=A) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `45` | [국민체육진흥공단_전자도서관](https://www.culture.go.kr/data/openapi/openapiView.do?id=45&category=F&gubun=A) | REST / JSON XML | 제외 | 도서관 소장자료/서지 계열 |

</details>

<details>
<summary>G. 정책지원 OpenAPI 20건</summary>

| ID | 제목 | 하위분류/형식 | 구현 여부 | 비고 |
| --- | --- | --- | --- | --- |
| `632` | [국립국어원_한국어기초사전_NEW](https://www.culture.go.kr/data/openapi/openapiView.do?id=632&category=G&gubun=A) | 창작물 > 기타창작물 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `557` | [국립국어원_통합 수어정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=557&category=G&gubun=A) | 창작물 > 기타창작물 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `550` | [문화체육관광부 외_기관 공지사항](https://www.culture.go.kr/data/openapi/openapiView.do?id=550&category=G&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `549` | [문화체육관광부 외_기관 보도자료](https://www.culture.go.kr/data/openapi/openapiView.do?id=549&category=G&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `408` | [국립국어원_우리말샘](https://www.culture.go.kr/data/openapi/openapiView.do?id=408&category=G&gubun=A) | 창작물 > 기타창작물 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `407` | [한국저작권위원회_용어사전](https://www.culture.go.kr/data/openapi/openapiView.do?id=407&category=G&gubun=A) | 창작물 > 기타창작물 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `380` | [국립세종도서관_정책정보포털-최신정책동향국외](https://www.culture.go.kr/data/openapi/openapiView.do?id=380&category=G&gubun=A) | 공지및통계 > 공지 | 제외 | 도서관 소장자료/서지 계열 |
| `379` | [국립세종도서관_정책정보포털-최신정책동향국내](https://www.culture.go.kr/data/openapi/openapiView.do?id=379&category=G&gubun=A) | 공지및통계 > 공지 | 제외 | 도서관 소장자료/서지 계열 |
| `369` | [국립국어원_문화정보수어](https://www.culture.go.kr/data/openapi/openapiView.do?id=369&category=G&gubun=A) | 창작물 > 기타창작물 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `368` | [국립국어원_전문용어수어](https://www.culture.go.kr/data/openapi/openapiView.do?id=368&category=G&gubun=A) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `367` | [국립국어원_일상생활수어](https://www.culture.go.kr/data/openapi/openapiView.do?id=367&category=G&gubun=A) | 창작물 > 기타창작물 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `298` | [한국데이터진흥원_연구보고서](https://www.culture.go.kr/data/openapi/openapiView.do?id=298&category=G&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `297` | [한국데이터진흥원_블로그디비디비](https://www.culture.go.kr/data/openapi/openapiView.do?id=297&category=G&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `296` | [한국데이터진흥원_데이터베이스백서](https://www.culture.go.kr/data/openapi/openapiView.do?id=296&category=G&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `189` | [국립국어원_외래어표기법](https://www.culture.go.kr/data/openapi/openapiView.do?id=189&category=G&gubun=A) | 창작물 > 기타창작물 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `168` | [문화체육관광부_공감코리아-정책정보문화](https://www.culture.go.kr/data/openapi/openapiView.do?id=168&category=G&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `512` | [한국저작권보호원_입찰정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=512&category=G&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `511` | [한국저작권보호원_보도자료](https://www.culture.go.kr/data/openapi/openapiView.do?id=511&category=G&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `470` | [한국언론진흥재단_입찰공고1](https://www.culture.go.kr/data/openapi/openapiView.do?id=470&category=G&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `458` | [한국문화예술회관연합회_입찰공고2](https://www.culture.go.kr/data/openapi/openapiView.do?id=458&category=G&gubun=A) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |

</details>

<details>
<summary>H. 문화홍보 OpenAPI 7건</summary>

| ID | 제목 | 하위분류/형식 | 구현 여부 | 비고 |
| --- | --- | --- | --- | --- |
| `659` | [한국체육산업개발(주)_올림픽공원 2025 입출차정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=659&category=H&gubun=A) | 공지및통계 > 공지 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `638` | [국립중앙박물관_수어동영상](https://www.culture.go.kr/data/openapi/openapiView.do?id=638&category=H&gubun=A) | 유형유산 > 유물(소장품) | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `637` | [국립중앙박물관_국보보물 검색](https://www.culture.go.kr/data/openapi/openapiView.do?id=637&category=H&gubun=A) | 유형유산 > 유물(소장품) | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `636` | [국립중앙박물관_소장품 검색](https://www.culture.go.kr/data/openapi/openapiView.do?id=636&category=H&gubun=A) | 유형유산 > 유물(소장품) | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `548` | [예술경영지원센터_문화예술 일자리 정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=548&category=H&gubun=A) | 공지및통계 > 공지 | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `244` | [한국방문위원회_새소식](https://www.culture.go.kr/data/openapi/openapiView.do?id=244&category=H&gubun=A) | 공지및통계 > 공지 | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `119` | [한국체육산업개발(주)_홍보동영상](https://www.culture.go.kr/data/openapi/openapiView.do?id=119&category=H&gubun=A) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |

</details>

<details>
<summary>I. 맞춤형 API OpenAPI 39건</summary>

| ID | 제목 | 하위분류/형식 | 구현 여부 | 비고 |
| --- | --- | --- | --- | --- |
| `657` | [국립중앙박물관_문화행사(행사/공연)](https://www.culture.go.kr/data/openapi/openapiView.do?id=657&category=I&gubun=B) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `598` | [한국문화정보원 외_전시정보(통합)](https://www.culture.go.kr/data/openapi/openapiView.do?id=598&category=I&gubun=B) | REST / JSON XML | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `603` | [한국문화정보원_전국 시티투어 코스와 함께하는 맛집 정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=603&category=I&gubun=B) | REST / JSON XML | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `599` | [한국문화정보원_전국 관광지 주변_전기차 충전소](https://www.culture.go.kr/data/openapi/openapiView.do?id=599&category=I&gubun=B) | REST / JSON XML | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `602` | [한국문화정보원_전국 박물관 미술관_공연행사](https://www.culture.go.kr/data/openapi/openapiView.do?id=602&category=I&gubun=B) | REST / JSON XML | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `601` | [한국문화정보원_초중고등학교 주변 도서관 정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=601&category=I&gubun=B) | REST / JSON XML | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `600` | [한국문화정보원_전통시장 주변 공영주차장 정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=600&category=I&gubun=B) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `597` | [한국문화정보원 외_공연정보(통합)](https://www.culture.go.kr/data/openapi/openapiView.do?id=597&category=I&gubun=B) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `546` | [한국문화정보원_국립공원 주변 문화시설 POI 정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=546&category=I&gubun=B) | REST+ / JSON XML | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `526` | [한국문화정보원 외_공연과 함께하는 CO2 줄이기](https://www.culture.go.kr/data/openapi/openapiView.do?id=526&category=I&gubun=B) | REST+ / JSON XML | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `525` | [한국문화정보원 외_역사가 있는 여행 이야기](https://www.culture.go.kr/data/openapi/openapiView.do?id=525&category=I&gubun=B) | REST+ / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `524` | [국민체육진흥공단 외_어디서 운동할까](https://www.culture.go.kr/data/openapi/openapiView.do?id=524&category=I&gubun=B) | REST+ / JSON XML | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `522` | [국립국어원 외_한국이 좋아요](https://www.culture.go.kr/data/openapi/openapiView.do?id=522&category=I&gubun=B) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `521` | [제주특별자치도청 외_씽씽 자전거와 함께 하는 여행](https://www.culture.go.kr/data/openapi/openapiView.do?id=521&category=I&gubun=B) | REST+ / JSON XML | 제외 | 문화체육관광부 및 산하기관 범위 밖 |
| `520` | [한국문화정보원 외_가족과 함께하는 농어촌 체험일기](https://www.culture.go.kr/data/openapi/openapiView.do?id=520&category=I&gubun=B) | REST / JSON XML | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `519` | [서울특별시청_반려 동물을 위한 지역 생활정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=519&category=I&gubun=B) | REST+ / JSON XML | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `518` | [한국문화예술위원회 외_길 위의 작은 가게](https://www.culture.go.kr/data/openapi/openapiView.do?id=518&category=I&gubun=B) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `517` | [한국문화관광연구원 외_맑은 하늘과 함께 하는 여행](https://www.culture.go.kr/data/openapi/openapiView.do?id=517&category=I&gubun=B) | REST / JSON XML | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `414` | [문화체육관광부 외_사서의 책장](https://www.culture.go.kr/data/openapi/openapiView.do?id=414&category=I&gubun=B) | REST+ / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `413` | [해외문화홍보원 외_이벤트 알림이](https://www.culture.go.kr/data/openapi/openapiView.do?id=413&category=I&gubun=B) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `412` | [국립중앙박물관 외_문화교육의 시작](https://www.culture.go.kr/data/openapi/openapiView.do?id=412&category=I&gubun=B) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `411` | [인천문화재단 외_여행은 체험하는 것](https://www.culture.go.kr/data/openapi/openapiView.do?id=411&category=I&gubun=B) | REST+ / JSON XML | 제외 | 문화체육관광부 및 산하기관 범위 밖 |
| `410` | [서울문화재단 외_문화부문 채용정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=410&category=I&gubun=B) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `409` | [한국문화정보원_어린이를 위한 공연정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=409&category=I&gubun=B) | REST+ / JSON XML | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `415` | [한국문화정보원_소소하지만 확실한 여행](https://www.culture.go.kr/data/openapi/openapiView.do?id=415&category=I&gubun=B) | REST+ / JSON XML | 제외 | 한국관광공사 제공서비스 |
| `418` | [한국문화정보원_관광지 안전정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=418&category=I&gubun=B) | REST / JSON XML | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `416` | [한국문화정보원_문화기반시설 통계정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=416&category=I&gubun=B) | REST+ / JSON XML | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `417` | [한국문화정보원_공공미술 작품을 찾아서](https://www.culture.go.kr/data/openapi/openapiView.do?id=417&category=I&gubun=B) | REST / JSON XML | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `396` | [문화체육관광부_일자리정보-일자리뉴스](https://www.culture.go.kr/data/openapi/openapiView.do?id=396&category=I&gubun=B) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `395` | [문화체육관광부_일자리정보-시험정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=395&category=I&gubun=B) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `378` | [국립중앙박물관 외_지도로 보는 문화재 탐방](https://www.culture.go.kr/data/openapi/openapiView.do?id=378&category=I&gubun=B) | REST+ / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `377` | [한국문화정보원 외_도서정보조회 서비스](https://www.culture.go.kr/data/openapi/openapiView.do?id=377&category=I&gubun=B) | REST / JSON XML | 제외 | 도서관 소장자료/서지 계열 |
| `376` | [한국문화정보원_장애인을 위한 시설정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=376&category=I&gubun=B) | REST+ / JSON XML | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `375` | [국립국어원 외_외국인을 위한 우리말 배우기](https://www.culture.go.kr/data/openapi/openapiView.do?id=375&category=I&gubun=B) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `374` | [한국학중앙연구원 외_한국의 향토문화](https://www.culture.go.kr/data/openapi/openapiView.do?id=374&category=I&gubun=B) | REST+ / JSON XML | 제외 | 도서관 소장자료/서지 계열 |
| `373` | [영상물등급위원회 외_무비갤러리](https://www.culture.go.kr/data/openapi/openapiView.do?id=373&category=I&gubun=B) | REST+ / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `372` | [한국문화정보원_방방곳곳 트래킹 안내 서비스](https://www.culture.go.kr/data/openapi/openapiView.do?id=372&category=I&gubun=B) | REST+ / JSON XML | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `371` | [한국정책방송원_역사기록정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=371&category=I&gubun=B) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `354` | [문화체육관광부_일자리정보-채용정보](https://www.culture.go.kr/data/openapi/openapiView.do?id=354&category=I&gubun=B) | REST / JSON XML | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |

</details>

## 파일데이터 전체 목록

<details>
<summary>A. 문화예술 파일데이터 137건</summary>

| ID | 제목 | 하위분류/형식 | 구현 여부 | 비고 |
| --- | --- | --- | --- | --- |
| `00000000000000000481` | [국립현대미술관_이벤트 정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000481&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000478` | [국립현대미술관_입주작가자료](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000478&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000475` | [영상물등급위원회_영화예고편 등급분류](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000475&category=A&category=C&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000470` | [국립아시아문화전당_행사일정](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000470&category=A&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000464` | [국립현대미술관_레지던시작가소식](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000464&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000459` | [국립한글박물관_문화행사](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000459&category=A&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000454` | [한국문화예술위원회_채널문장](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000454&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000453` | [영상물등급위원회_자체등급분류 정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000453&category=A&category=C&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000446` | [한국문화예술위원회_글틴-쓰면서 뒹글](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000446&category=A&category=A&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000442` | [한국문화예술위원회_문장웹진](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000442&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000429` | [예술의전당_전시정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000429&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000428` | [예술의전당_종합 공연정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000428&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000424` | [한국문학번역원_한국고전문학 해외소개 칼럼](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000424&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000422` | [한국문학번역원_한국문학도서 해외소개 리뷰(에세이, 픽션)](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000422&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000024` | [한국문화예술회관연합회_공지사항](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000024&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000025` | [한국문화예술회관연합회_공연전시정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000025&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000027` | [예술경영지원센터_KOPIS-공연시설별통계](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000027&category=A&category=A&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000028` | [예술경영지원센터_KOPIS-공연별통계](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000028&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000029` | [예술경영지원센터_KOPIS-국내내한별통계](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000029&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000030` | [예술경영지원센터_KOPIS-장르별통계](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000030&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000031` | [예술경영지원센터_KOPIS-지역별통계](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000031&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000032` | [예술경영지원센터_KOPIS-일별예매수및매출액](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000032&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000033` | [예술경영지원센터_KOPIS-예매상황판](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000033&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000034` | [예술경영지원센터_KOPIS-극작가목록](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000034&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000035` | [예술경영지원센터_KOPIS-축제목록](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000035&category=A&category=A&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000036` | [예술경영지원센터_KOPIS-수상작목록](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000036&category=A&category=A&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000037` | [예술경영지원센터_KOPIS-기획제작사목록](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000037&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000038` | [예술경영지원센터_KOPIS-공연시설별상세정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000038&category=A&category=A&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000039` | [예술경영지원센터_KOPIS-공연시설목록](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000039&category=A&category=A&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000040` | [예술경영지원센터_KOPIS-공연상세정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000040&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000041` | [예술경영지원센터_KOPIS-공연목록](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000041&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000042` | [한국문화예술위원회_예술자료원 소장자료](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000042&category=A&category=A&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 소장자료/서지 계열 |
| `00000000000000000043` | [한국문화예술위원회_DA-Arts 공연예술정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000043&category=A&category=A&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000044` | [한국문화예술위원회_예술가 정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000044&category=A&category=A&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000045` | [한국문화예술위원회_공연장 공연정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000045&category=A&category=A&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000046` | [한국문화예술위원회_예술자료원 소장자료](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000046&category=A&category=A&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 소장자료/서지 계열 |
| `00000000000000000047` | [한국체육산업개발(주)_올림픽공원대관정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000047&category=A&category=E&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000048` | [강원문화재단_사진자료](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000048&category=A&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000049` | [예술의전당_공연-기타2](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000049&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000023` | [한국문화예술회관연합회_보도자료](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000023&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000022` | [한국문화예술회관연합회_사진자료](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000022&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000021` | [한국문화예술회관연합회_자료실](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000021&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000120` | [문화체육관광부_문화광장-추천도서](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000120&category=A&category=G&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 소장자료/서지 계열 |
| `00000000000000000411` | [예술의전당_나이대별 예매 건수](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000411&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000298` | [문화체육관광부_문화예술공연(통합)](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000298&category=A&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000294` | [문화체육관광부 외_기관 공연정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000294&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000001` | [한국예술인복지재단_자료실](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000001&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000002` | [한국예술인복지재단_보도자료](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000002&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000003` | [한국예술인복지재단_공지사항](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000003&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000004` | [한국예술인복지재단_입찰공고](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000004&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000005` | [한국예술인복지재단_사업공고](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000005&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000007` | [대한민국예술원_예술원 유고회원](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000007&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000008` | [대한민국예술원_예술원 회원](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000008&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000009` | [대한민국예술원_예술논문집](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000009&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000010` | [대한민국예술원_기타간행물](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000010&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000011` | [대한민국예술원_예술원보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000011&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000122` | [대한민국역사박물관_특별전시](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000122&category=A&category=B&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000127` | [국립한글박물관_전시정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000127&category=A&category=B&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000012` | [재단법인 정동극장_뉴스레터](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000012&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000013` | [재단법인 정동극장_공연정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000013&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000014` | [재단법인 정동극장_영상자료](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000014&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000015` | [재단법인 정동극장_프로모션](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000015&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000016` | [예술의전당_이벤트](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000016&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000017` | [예술의전당_아카데미](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000017&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000018` | [한국문화예술회관연합회_웹진](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000018&category=A&category=A&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000019` | [한국문화예술회관연합회_꿈다락토요문화학교](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000019&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000020` | [한국문화예술회관연합회_예술교육](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000020&category=A&category=A&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000050` | [예술의전당_공연-음악2](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000050&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000117` | [국립현대미술관_전시정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000117&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000052` | [예술의전당_공연-기타](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000052&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000098` | [한국문화예술위원회_나눔티켓-공연정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000098&category=A&category=A&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000097` | [국립어린이청소년도서관_전시실 정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000097&category=A&category=F&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000096` | [한국공예디자인문화진흥원_전시도록](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000096&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000095` | [한국공예디자인문화진흥원_연구보고서](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000095&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000094` | [한국공예디자인문화진흥원_출판물](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000094&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000093` | [한국공예디자인문화진흥원_매거진공예디자인](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000093&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000325` | [국립현대미술관_도서자료 서지정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000325&category=A&category=A&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 소장자료/서지 계열 |
| `00000000000000000092` | [대한민국역사박물관_학술행사](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000092&category=A&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000091` | [영상물등급위원회_공연추천](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000091&category=A&category=C&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000090` | [예술경영지원센터_국내DB](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000090&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000089` | [재단법인 정동극장_공지사항](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000089&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000088` | [한국문화예술위원회_아르코미술관전시](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000088&category=A&category=A&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000087` | [(재)서울시립교향악단_공연정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000087&category=A&category=&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000086` | [재단법인세종문화회관_공연메타정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000086&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000085` | [서귀포시_공연행사정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000085&category=A&category=&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000099` | [국립중앙극장_공연자료](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000099&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000100` | [한국체육산업개발(주)_올림픽공원공연정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000100&category=A&category=E&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000116` | [한국문화예술교육진흥원_기획리포트](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000116&category=A&category=A&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000115` | [국립중앙극장_공연예술자료아카이브](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000115&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000114` | [예술의전당_공연-음악회](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000114&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000113` | [한국예술종합학교_공연정보5](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000113&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000112` | [재단법인 정동극장_보도자료](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000112&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000111` | [한국문화예술위원회_공연정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000111&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000109` | [예술경영지원센터_브로드캐스트](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000109&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000108` | [예술경영지원센터_국내자료실](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000108&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000107` | [예술경영지원센터_보도자료](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000107&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000106` | [예술경영지원센터_웹진예술경영](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000106&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000105` | [국립국악원_공연정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000105&category=A&category=B&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000104` | [민속국악원_공연정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000104&category=A&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000103` | [남도국악원_공연정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000103&category=A&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000102` | [부산국악원_공연정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000102&category=A&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000101` | [한국문화관광연구원_연구보고서-문화예술](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000101&category=A&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000084` | [강원문화재단_문화예술자료](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000084&category=A&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000083` | [전주시_공연전시정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000083&category=A&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000065` | [한국문화예술교육진흥원_기타자료](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000065&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000064` | [한국문화예술교육진흥원_사진자료](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000064&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000063` | [한국문화예술교육진흥원_영상자료](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000063&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000062` | [한국문화예술교육진흥원_정책연구](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000062&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000061` | [한국문화예술교육진흥원_콘텐츠개발연구](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000061&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000060` | [한국문화예술교육진흥원_평가통계연구](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000060&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000281` | [한국문화관광연구원 외_학술연구](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000281&category=A&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000280` | [한국디자인진흥원 외_ebook 간행물](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000280&category=A&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000279` | [인천문화재단 외_소속 및 산하기관 교육정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000279&category=A&category=H&dataType=BATCH) | CSV / BATCH | 제외 | 문화체육관광부 및 산하기관 범위 밖 |
| `00000000000000000058` | [예술의전당_공연-연극](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000058&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000057` | [예술의전당_공연-발레](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000057&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000056` | [예술의전당_공연-무용](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000056&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000055` | [예술의전당_공연-뮤지컬](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000055&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000054` | [예술의전당_공연-미술](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000054&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000053` | [예술의전당_공연-서예](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000053&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000066` | [한국문화예술교육진흥원_기타](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000066&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000067` | [한국문화예술교육진흥원_기초연구](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000067&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000082` | [고양문화재단_공연일정](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000082&category=A&category=&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000081` | [한국디자인진흥원_디자인리포트-국내리포트](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000081&category=A&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000080` | [(재)마포문화재단_마포아트센터공연전시](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000080&category=A&category=A&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000079` | [구로문화재단_구로아트밸리공연](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000079&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000078` | [서울시립미술관_전시정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000078&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000077` | [재단법인국악방송_국악포커스](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000077&category=A&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000076` | [재단법인국악방송_공연안내](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000076&category=A&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000075` | [재단법인국악방송_알림](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000075&category=A&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000074` | [재단법인국악방송_보도자료](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000074&category=A&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000073` | [대한민국예술원_공지사항](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000073&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000072` | [대한민국예술원_사진갤러리](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000072&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000071` | [대한민국예술원_사진자료](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000071&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000070` | [대한민국예술원_예술원소식](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000070&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000069` | [대한민국예술원_자유게시판](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000069&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000068` | [예술의전당_공연-오페라](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000068&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000051` | [예술의전당_공연-디자인](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000051&category=A&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |

</details>

<details>
<summary>B. 문화유산 파일데이터 76건</summary>

| ID | 제목 | 하위분류/형식 | 구현 여부 | 비고 |
| --- | --- | --- | --- | --- |
| `00000000000000000474` | [국립광주박물관_소장품_리스트](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000474&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000473` | [국립경주박물관_발간자료](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000473&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000471` | [국립부여박물관_교육행사_전체프로그램 목록](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000471&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `99000000000000000009` | [한국문화정보원_수원화성 3D 디지털 에셋](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=99000000000000000009&category=B&category=B&dataType=FILE) | CSV / FILE | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `99000000000000000008` | [문화체육관광부_전통문양 3D 디지털 에셋](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=99000000000000000008&category=B&category=B&dataType=FILE) | CSV / FILE | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000466` | [국립국악원_소장자료(공공누리)](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000466&category=B&category=B&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 소장자료/서지 계열 |
| `00000000000000000462` | [국립청주박물관_소장품](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000462&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000450` | [국립민속박물관_한국민속대백과사전](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000450&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000418` | [국립경주박물관 외_국립지방박물관 통합 전시 정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000418&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000177` | [국립경주박물관_유물정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000177&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000132` | [국립국악원_국악아카이브](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000132&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000133` | [한국학중앙연구원_장서각디지털아카이브](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000133&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000134` | [한국학중앙연구원_한국학자료포털](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000134&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000135` | [국립한글박물관_아카이브](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000135&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000059` | [국립현대미술관_소장작품](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000059&category=B&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000136` | [국립국악원_학술연구-영인 번역](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000136&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000137` | [국립국악원_학술연구-국악원 논문집](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000137&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000138` | [국립국악원_학술연구-해외보급자료](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000138&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000139` | [국립국악원_학술연구-악보 및 무보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000139&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000140` | [국립국악원_학술연구-고서](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000140&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000346` | [국립국악원_교육연구-국악사전](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000346&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000141` | [국립국악원_학술연구-구술채록](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000141&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000142` | [국립국악원_학술연구-국악이론](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000142&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000131` | [한국정책방송원_국가기록영상](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000131&category=B&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000130` | [한국정책방송원_국가기록사진](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000130&category=B&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000129` | [한국정책방송원_대한뉴스관](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000129&category=B&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000128` | [국립한글박물관_문헌자료와해제](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000128&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000126` | [국립한글박물관_소장자료](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000126&category=B&category=B&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 소장자료/서지 계열 |
| `00000000000000000125` | [대한민국역사박물관_현대사아카이브](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000125&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000124` | [대한민국역사박물관_소장자료](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000124&category=B&category=B&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 소장자료/서지 계열 |
| `00000000000000000123` | [대한민국역사박물관_교육프로그램](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000123&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000006` | [한국예술인복지재단_문화소식](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000006&category=B&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000284` | [국립중앙박물관 외_국립지방박물관 문화행사 통합정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000284&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000181` | [국립국악원_국악연감 서비스](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000181&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000286` | [한국문화정보원_전국 중고서점 및 운영정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000286&category=B&category=H&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000289` | [국립중앙박물관 외_유물정보(주요유물)](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000289&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000290` | [국립광주박물관 외_전시도록](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000290&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000179` | [국립민속박물관_민속대백과사전](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000179&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000180` | [한국문화정보원_2D개별문양목록조회](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000180&category=B&category=H&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000276` | [국립중앙박물관 외_20개 기관 유물정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000276&category=B&category=B&dataType=BATCH) | CSV / BATCH | 제외 | 문화체육관광부 및 산하기관 범위 밖 |
| `00000000000000000143` | [한국콘텐츠진흥원_문화원형라이브러리-음악](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000143&category=B&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000144` | [유네스코한국위원회_유네스코와유산](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000144&category=B&category=H&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000163` | [국립민속박물관_민속아카이브 사진자료](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000163&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000164` | [문화재청_문화재정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000164&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000165` | [문화재청_문화재사진정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000165&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000166` | [국립중앙박물관_e뮤지엄 유물정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000166&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000110` | [한국문화예술위원회_사이버문학관문학공모전](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000110&category=B&category=A&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 위치/운영 정보 아님 |
| `00000000000000000167` | [국립공주박물관_유물정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000167&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000168` | [국립진주박물관_유물정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000168&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000169` | [국립춘천박물관_유물정보3](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000169&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000170` | [국립제주박물관_유물정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000170&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000171` | [국립김해박물관_유물정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000171&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000172` | [국립청주박물관_유물정보6](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000172&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000173` | [국립대구박물관_유물정보7](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000173&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000174` | [국립부여박물관_유물정보8](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000174&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000175` | [국립전주박물관_유물정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000175&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000176` | [국립광주박물관_유물정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000176&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000162` | [국립민속박물관_소장유물](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000162&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000161` | [국립민속박물관_현장조사DB 정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000161&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000160` | [한국문화정보원_디자인문양](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000160&category=B&category=H&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000145` | [한국고전번역원_고전번역서 서지정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000145&category=B&category=&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 소장자료/서지 계열 |
| `00000000000000000178` | [국립중앙박물관_유물정보12](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000178&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000147` | [전북대학교 박물관_호남기록문화정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000147&category=B&category=B&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 소장자료/서지 계열 |
| `00000000000000000148` | [한국국학진흥원_영남사림문집](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000148&category=B&category=&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000149` | [한국학중앙연구원_한국향토문화전자대전](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000149&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000150` | [민속자연사박물관_제주자연사박물관](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000150&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000151` | [서울역사박물관_유물정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000151&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000152` | [동학농민혁명기념재단_동학농민혁명종합정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000152&category=B&category=&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000153` | [지역문화교류호남재단_고문서](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000153&category=B&category=&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000154` | [동북아역사재단_동북아역사넷](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000154&category=B&category=&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000155` | [고려대장경연구소_고려대장경지식베이스](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000155&category=B&category=&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000156` | [충남대학교 도서관_기호유학고문헌정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000156&category=B&category=F&dataType=BATCH) | CSV / BATCH | 제외 | 문화체육관광부 및 산하기관 범위 밖 |
| `00000000000000000157` | [한국문화정보원_전통문화종합사이트문화상징](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000157&category=B&category=H&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000158` | [대한민국역사박물관_발간자료](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000158&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000159` | [국립고궁박물관_ICT유물안내](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000159&category=B&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000146` | [전쟁기념관_군사유물정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000146&category=B&category=&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |

</details>

<details>
<summary>C. 문화산업 파일데이터 84건</summary>

| ID | 제목 | 하위분류/형식 | 구현 여부 | 비고 |
| --- | --- | --- | --- | --- |
| `00000000000000000480` | [한국영상자료원_한국영화박물관 교육](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000480&category=C&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000476` | [한국정책방송원_프로그램 특집](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000476&category=C&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000469` | [게임물관리위원회_자체등급분류정보서비스](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000469&category=C&category=C&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000468` | [한국언론진흥재단_미디어정보-정기간행물-신문과방송-호수별보기](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000468&category=C&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000467` | [한국영상자료원_영화글(연재/기획/기관지/종료연재)](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000467&category=C&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000465` | [한국정책방송원_정책공공](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000465&category=C&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000463` | [한국언론진흥재단_미디어정보-기획취재아카이브-역대보도물](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000463&category=C&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000461` | [한국언론진흥재단_미디어정보-정기간행물-신문과방송-전체기사](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000461&category=C&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000460` | [한국도박문제예방치유원_예방/홍보/치유재활 콘텐츠](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000460&category=C&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000449` | [게임물관리위원회_게임등급정보서비스](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000449&category=C&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000448` | [한국저작권위원회_공유마당 사진](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000448&category=C&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000447` | [한국저작권위원회_공유마당 만료저작물](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000447&category=C&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000444` | [한국문화정보원_카페가 있는 서점데이터](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000444&category=C&category=H&dataType=BATCH) | CSV / BATCH | 구현됨 | `cafe_bookstores_csv` |
| `00000000000000000443` | [한국문화정보원_전국 독립서점 및 운영정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000443&category=C&category=H&dataType=BATCH) | CSV / BATCH | 구현됨 | `independent_bookstores_csv` |
| `00000000000000000441` | [한국영상자료원_전단지정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000441&category=C&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000196` | [한국문화정보원_기관별동의어-핵심어-표제어정리](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000196&category=C&category=H&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000195` | [한국문화예술회관연합회_구인게시판](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000195&category=C&category=A&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000194` | [한국언론진흥재단_공모신청](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000194&category=C&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000193` | [한국언론진흥재단_사업결과](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000193&category=C&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000192` | [한국언론진흥재단_채용공고](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000192&category=C&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000191` | [한국언론진흥재단_보도자료](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000191&category=C&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000190` | [한국언론진흥재단_신문과방송](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000190&category=C&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000189` | [한국언론진흥재단_공지사항](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000189&category=C&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000188` | [한국언론진흥재단_언론산업통계-기타분석자료](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000188&category=C&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000187` | [한국언론진흥재단_전체현황](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000187&category=C&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000186` | [한국언론진흥재단_연구조사서](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000186&category=C&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000185` | [문화체육관광부_채용 정보(통합)](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000185&category=C&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000184` | [예술경영지원센터_공고-기금-행사](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000184&category=C&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000183` | [한국예술인복지재단_채용정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000183&category=C&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000182` | [한국체육산업개발(주)_채용공고2](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000182&category=C&category=E&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000282` | [한국문화정보원_전국 아동서점 운영정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000282&category=C&category=H&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000239` | [영상물등급위원회_비디오정보 서비스](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000239&category=C&category=C&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000240` | [한국영상자료원_D시네마 정보 서비스](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000240&category=C&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000292` | [문화체육관광부 외_기관 채용정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000292&category=C&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000293` | [문화체육관광부 외_기관 교육정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000293&category=C&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000242` | [한국문화정보원_전국 문화 여가 활동 시설(클래스)](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000242&category=C&category=H&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000243` | [한국문화정보원_전국 문화 여가 활동 시설(액티비티)](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000243&category=C&category=H&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000244` | [한국문화정보원_전국 문화 여가 활동 시설(캠핑)](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000244&category=C&category=H&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000245` | [한국문화정보원_전국 공유 오피스 시설](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000245&category=C&category=H&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000246` | [한국문화정보원_전국 가족 유아 동반 가능 문화시설](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000246&category=C&category=H&dataType=BATCH) | CSV / BATCH | 구현됨 | `family_infant_culture_facilities_csv` |
| `00000000000000000247` | [한국문화정보원_전국 회의 세미나 시설정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000247&category=C&category=H&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000197` | [한국문화정보원_기관별QI챗봇정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000197&category=C&category=H&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000238` | [한국저작권위원회_저작권동향](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000238&category=C&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000221` | [한국영상자료원_영화사연구DVD](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000221&category=C&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000222` | [한국영상자료원_시나리오정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000222&category=C&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000223` | [한국영상자료원_스틸정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000223&category=C&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000224` | [한국영상자료원_비디오정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000224&category=C&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000225` | [한국영상자료원_동영상정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000225&category=C&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000226` | [한국영상자료원_도서정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000226&category=C&category=C&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 소장자료/서지 계열 |
| `00000000000000000227` | [한국영상자료원_논문](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000227&category=C&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000228` | [한국체육산업개발(주)_사회공헌](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000228&category=C&category=E&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000353` | [문화체육관광부_문화칼럼](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000353&category=C&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000354` | [문화체육관광부_정책기자마당](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000354&category=C&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000229` | [한국저작권위원회_행사일정](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000229&category=C&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000230` | [한국저작권위원회_보도자료](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000230&category=C&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000231` | [영화진흥위원회_영화정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000231&category=C&category=C&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000232` | [한국영상자료원_상영정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000232&category=C&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000233` | [한국영상자료원_영화정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000233&category=C&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000234` | [한국영상자료원_포스터정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000234&category=C&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000235` | [한국영상자료원_정기간행물](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000235&category=C&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000236` | [한국문화예술위원회_행사정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000236&category=C&category=A&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000237` | [한국콘텐츠진흥원_콘텐츠연구보고서](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000237&category=C&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000220` | [한국영상자료원_영화사연구도서](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000220&category=C&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000219` | [한국정책방송원_정책뉴스 사회 문화](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000219&category=C&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000312` | [한국출판문화산업진흥원_출판지원도서 우수출판콘텐츠 제작 지원 정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000312&category=C&category=F&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000201` | [영상물등급위원회_영화 등급분류 목록](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000201&category=C&category=C&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000202` | [한국영상자료원_전시정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000202&category=C&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000204` | [한국출판문화산업진흥원_전문자료](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000204&category=C&category=F&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 소장자료/서지 계열 |
| `00000000000000000205` | [국제방송교류재단_뉴스](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000205&category=C&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000206` | [한국천문연구원_천문우주정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000206&category=C&category=&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000207` | [영화진흥위원회_영화사](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000207&category=C&category=C&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000208` | [한국출판문화산업진흥원_공지사항](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000208&category=C&category=F&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000209` | [한국저작권위원회_프로젝트기본정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000209&category=C&category=G&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000210` | [대한민국역사박물관_채용](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000210&category=C&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000211` | [영화진흥위원회_박스오피스](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000211&category=C&category=C&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000212` | [영화진흥위원회_영화인정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000212&category=C&category=C&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000213` | [문화체육관광부_e브리핑](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000213&category=C&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000214` | [대한민국역사박물관_문화행사](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000214&category=C&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000215` | [한국영상자료원_필름정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000215&category=C&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000216` | [한국저작권위원회_OLIS오픈소스라이센스](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000216&category=C&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000217` | [한국출판문화산업진흥원_관련법규](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000217&category=C&category=F&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000351` | [문화체육관광부_아카이브전문자료 정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000351&category=C&category=G&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 소장자료/서지 계열 |
| `00000000000000000218` | [한국정책방송원_정책문화 교양](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000218&category=C&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000198` | [한국저작권보호원_채용정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000198&category=C&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |

</details>

<details>
<summary>D. 관광 파일데이터 28건</summary>

| ID | 제목 | 하위분류/형식 | 구현 여부 | 비고 |
| --- | --- | --- | --- | --- |
| `00000000000000000409` | [한국문화관광연구원_문화정책논총](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000409&category=D&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000416` | [한국문화정보원_전국 세계음식점](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000416&category=D&category=H&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000415` | [한국문화정보원_전국 다국어 가이드 제공 문화시설](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000415&category=D&category=H&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000414` | [한국문화정보원_전국 반려동물 동반가능 문화시설 위치](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000414&category=D&category=H&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000413` | [한국문화정보원_전국 문화예술관광지 배리어프리 정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000413&category=D&category=H&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000412` | [한국문화정보원_미디어콘텐츠 영상 내 유명지](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000412&category=D&category=H&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000299` | [문화체육관광부_추천여행지](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000299&category=D&category=G&dataType=BATCH) | CSV / BATCH | 링크 문서화 | `recommended_travel_places` |
| `00000000000000000410` | [한국문화관광연구원_관광지식채널 정기간행물 정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000410&category=D&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000391` | [한국체육산업개발(주)_올림픽공원장미정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000391&category=D&category=E&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000392` | [홍천군_휴양지](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000392&category=D&category=D&dataType=BATCH) | CSV / BATCH | 제외 | 문화체육관광부 및 산하기관 범위 밖 |
| `00000000000000000275` | [한국문화관광연구원 외_관광지정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000275&category=D&category=C&dataType=BATCH) | CSV / BATCH | 제외 | 한국관광공사 제공서비스 |
| `00000000000000000393` | [한국문화관광연구원_한국관광정책](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000393&category=D&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000394` | [한국농어촌공사_체험관광마을](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000394&category=D&category=D&dataType=BATCH) | CSV / BATCH | 제외 | 문화체육관광부 및 산하기관 범위 밖 |
| `00000000000000000395` | [종로구_공연장정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000395&category=D&category=&dataType=BATCH) | CSV / BATCH | 제외 | 문화체육관광부 및 산하기관 범위 밖 |
| `00000000000000000396` | [한국원자력환경공단_공단시설물 정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000396&category=D&category=&dataType=BATCH) | CSV / BATCH | 제외 | 문화체육관광부 및 산하기관 범위 밖 |
| `00000000000000000397` | [인천문화재단_지역축제](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000397&category=D&category=H&dataType=BATCH) | CSV / BATCH | 제외 | 문화체육관광부 및 산하기관 범위 밖 |
| `00000000000000000398` | [부산광역시청_관광정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000398&category=D&category=D&dataType=BATCH) | CSV / BATCH | 제외 | 문화체육관광부 및 산하기관 범위 밖 |
| `00000000000000000399` | [한국관광공사_해외이미지](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000399&category=D&category=D&dataType=BATCH) | CSV / BATCH | 제외 | 한국관광공사 제공서비스 |
| `00000000000000000400` | [문화체육관광부_지역축제정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000400&category=D&category=G&dataType=BATCH) | CSV / BATCH | 제외 | 한국관광공사 제공서비스 |
| `00000000000000000401` | [한국지역진흥재단_축제정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000401&category=D&category=D&dataType=BATCH) | CSV / BATCH | 제외 | 문화체육관광부 및 산하기관 범위 밖 |
| `00000000000000000402` | [한국체육산업개발(주)_올림픽공원장미광장](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000402&category=D&category=E&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000403` | [한국체육산업개발(주)_포토갤러리](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000403&category=D&category=E&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000404` | [한국체육산업개발(주)_올림픽공원생태공원갤러리](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000404&category=D&category=E&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000405` | [한국관광공사_청사초롱서비스](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000405&category=D&category=D&dataType=BATCH) | CSV / BATCH | 제외 | 한국관광공사 제공서비스 |
| `00000000000000000406` | [한국관광공사_사진갤러리](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000406&category=D&category=D&dataType=BATCH) | CSV / BATCH | 제외 | 한국관광공사 제공서비스 |
| `00000000000000000407` | [한국관광공사_관광정보-테마관광](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000407&category=D&category=D&dataType=BATCH) | CSV / BATCH | 제외 | 한국관광공사 제공서비스 |
| `00000000000000000408` | [한국문화관광연구원_세미나자료실](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000408&category=D&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000417` | [한국문화정보원_전국 연극장 및 소극장 정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000417&category=D&category=H&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |

</details>

<details>
<summary>E. 체육 파일데이터 38건</summary>

| ID | 제목 | 하위분류/형식 | 구현 여부 | 비고 |
| --- | --- | --- | --- | --- |
| `00000000000000000455` | [대한체육회_체육소식](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000455&category=E&category=E&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000366` | [국민체육진흥공단_공지사항](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000366&category=E&category=E&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000365` | [국민체육진흥공단_스포츠강좌이용권시설정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000365&category=E&category=E&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000364` | [대한장애인체육회_전국장애학생체육대회 포토갤러리](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000364&category=E&category=E&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000363` | [대한장애인체육회_공지사항](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000363&category=E&category=E&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000278` | [한국체육산업개발(주) 외_15개 기관 보도자료](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000278&category=E&category=E&dataType=BATCH) | CSV / BATCH | 제외 | 한국관광공사 제공서비스 |
| `00000000000000000362` | [한국체육산업개발(주)_올림픽공원운영현황](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000362&category=E&category=E&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000361` | [한국체육산업개발(주)_스포츠센터운영현황](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000361&category=E&category=E&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000360` | [대한체육회_체육시설정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000360&category=E&category=E&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000359` | [한국체육산업개발(주)_평생교육원교육정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000359&category=E&category=E&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000358` | [국민체육진흥공단_88서울올림픽종목별동영상자료](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000358&category=E&category=E&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000357` | [국민체육진흥공단_스포츠강좌이용권시설정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000357&category=E&category=E&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000356` | [국민체육진흥공단_스포츠강좌이용권강좌정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000356&category=E&category=E&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000355` | [한국체육산업개발(주)_올림픽공원유실물정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000355&category=E&category=E&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000388` | [한국체육산업개발(주)_협력기관정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000388&category=E&category=E&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000389` | [한국체육산업개발(주)_역대수상 및 인증기록정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000389&category=E&category=E&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000291` | [문화체육관광부 외_기관 (문화)행사정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000291&category=E&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000390` | [문화체육관광부_문화광장-체육행사](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000390&category=E&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000367` | [대한체육회_행사-대회](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000367&category=E&category=E&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000386` | [대한장애인체육회_행사-대회정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000386&category=E&category=E&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000385` | [한국체육산업개발(주)_공지사항](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000385&category=E&category=E&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000384` | [한국체육산업개발(주)_분당올림픽스포츠센터정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000384&category=E&category=E&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000383` | [한국체육산업개발(주)_보도자료](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000383&category=E&category=E&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000382` | [한국체육산업개발(주)_올림픽공원올팍소식](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000382&category=E&category=E&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000381` | [한국체육산업개발(주)_올림픽수영장정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000381&category=E&category=E&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000380` | [한국체육산업개발(주)_일산올림픽스포츠센터정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000380&category=E&category=E&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000379` | [한국체육산업개발(주)_올림픽공원 스케이트장 정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000379&category=E&category=E&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000378` | [한국체육산업개발(주)_올림픽공원스포츠센터정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000378&category=E&category=E&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000377` | [한국체육산업개발(주)_올림픽공원보도자료](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000377&category=E&category=E&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000376` | [한국체육산업개발(주)_올팍축구장정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000376&category=E&category=E&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000375` | [대한체육회_공지사항](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000375&category=E&category=E&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000374` | [대한체육회_종목용어사전](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000374&category=E&category=E&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000373` | [대한체육회_동영상서비스](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000373&category=E&category=E&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000372` | [대한체육회_명예기자활동](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000372&category=E&category=E&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000371` | [대한체육회_생활체육뉴스](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000371&category=E&category=E&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000370` | [대한체육회_생활체육문헌](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000370&category=E&category=E&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000369` | [대한체육회_종목소개자료실](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000369&category=E&category=E&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000368` | [대한체육회_포토갤러리](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000368&category=E&category=E&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |

</details>

<details>
<summary>F. 도서 파일데이터 31건</summary>

| ID | 제목 | 하위분류/형식 | 구현 여부 | 비고 |
| --- | --- | --- | --- | --- |
| `00000000000000000472` | [국립세종도서관_새로들어온책(일반/정책/어린이)](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000472&category=F&category=F&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 소장자료/서지 계열 |
| `00000000000000000451` | [국립어린이청소년도서관_세계의 도서관](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000451&category=F&category=F&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000445` | [국립어린이청소년도서관_다국어동화구연 전체동화](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000445&category=F&category=F&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 위치/운영 정보 아님 |
| `00000000000000000427` | [한국문학번역원_한국문학번역 전문도서관 소장자료](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000427&category=F&category=A&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 소장자료/서지 계열 |
| `00000000000000000426` | [한국문학번역원_한국문학번역출간 도서정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000426&category=F&category=A&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 소장자료/서지 계열 |
| `00000000000000000425` | [한국문학번역원_한국문학 작가정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000425&category=F&category=A&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 위치/운영 정보 아님 |
| `00000000000000000307` | [국립세종도서관_국내DB](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000307&category=F&category=F&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 소장자료/서지 계열 |
| `00000000000000000308` | [국립어린이청소년도서관_공개모집](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000308&category=F&category=F&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000309` | [국립어린이청소년도서관_공지사항](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000309&category=F&category=F&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000310` | [국립중앙도서관_소장자료](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000310&category=F&category=B&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 소장자료/서지 계열 |
| `00000000000000000311` | [한국체육산업개발(주)_올림픽공원도서정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000311&category=F&category=E&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 소장자료/서지 계열 |
| `00000000000000000313` | [국립중앙도서관_OAK-PORTAL](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000313&category=F&category=B&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 위치/운영 정보 아님 |
| `00000000000000000314` | [국립어린이청소년도서관_다국어동화구연-한국전래동화](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000314&category=F&category=F&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 위치/운영 정보 아님 |
| `00000000000000000315` | [한국출판문화산업진흥원_세종도서-문화나눔](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000315&category=F&category=F&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 소장자료/서지 계열 |
| `00000000000000000316` | [한국출판문화산업진흥원_세종도서-교양](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000316&category=F&category=F&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 소장자료/서지 계열 |
| `00000000000000000333` | [국민체육진흥공단_전자도서관](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000333&category=F&category=E&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 소장자료/서지 계열 |
| `00000000000000000318` | [한국출판문화산업진흥원_추천도서-대학신입생추천도서](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000318&category=F&category=F&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 소장자료/서지 계열 |
| `00000000000000000319` | [국립세종도서관_사서추천도서](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000319&category=F&category=F&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 소장자료/서지 계열 |
| `00000000000000000320` | [국립중앙도서관_사서추천도서2](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000320&category=F&category=B&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 소장자료/서지 계열 |
| `00000000000000000321` | [한국출판문화산업진흥원_추천도서-청소년권장도서](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000321&category=F&category=F&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 소장자료/서지 계열 |
| `00000000000000000322` | [한국출판문화산업진흥원_추천도서-이달의읽을만한책](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000322&category=F&category=F&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 소장자료/서지 계열 |
| `00000000000000000323` | [한국체육산업개발(주)_올림픽공원도서정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000323&category=F&category=E&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 소장자료/서지 계열 |
| `00000000000000000324` | [한국출판문화산업진흥원_동영상](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000324&category=F&category=F&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000326` | [국립중앙도서관_조선총독부관보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000326&category=F&category=B&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 위치/운영 정보 아님 |
| `00000000000000000327` | [국립어린이청소년도서관_사서추천도서](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000327&category=F&category=F&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 소장자료/서지 계열 |
| `00000000000000000328` | [국립민속박물관_발간도서](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000328&category=F&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000329` | [한국출판문화산업진흥원_독서캘린더](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000329&category=F&category=F&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000330` | [한국출판문화산업진흥원_내가권하는한권의책](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000330&category=F&category=F&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 소장자료/서지 계열 |
| `00000000000000000331` | [한국출판문화산업진흥원_독서활동-이야기](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000331&category=F&category=F&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000332` | [한국출판문화산업진흥원_손안애서](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000332&category=F&category=F&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000317` | [한국출판문화산업진흥원_세종도서-학술](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000317&category=F&category=F&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 소장자료/서지 계열 |

</details>

<details>
<summary>G. 정책지원 파일데이터 20건</summary>

| ID | 제목 | 하위분류/형식 | 구현 여부 | 비고 |
| --- | --- | --- | --- | --- |
| `00000000000000000452` | [국립국어원_한국어기초사전_NEW](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000452&category=G&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000295` | [국립국어원_통합 수어정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000295&category=G&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000288` | [문화체육관광부 외_기관 공지사항](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000288&category=G&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000287` | [문화체육관광부 외_기관 보도자료](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000287&category=G&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000334` | [한국저작권보호원_입찰정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000334&category=G&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000335` | [한국저작권보호원_보도자료](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000335&category=G&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000336` | [한국언론진흥재단_입찰공고1](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000336&category=G&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000337` | [한국문화예술회관연합회_입찰공고2](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000337&category=G&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000338` | [국립국어원_우리말샘](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000338&category=G&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000339` | [한국저작권위원회_용어사전](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000339&category=G&category=G&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000352` | [문화체육관광부_공감코리아-정책정보문화](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000352&category=G&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000341` | [국립세종도서관_정책정보포털-최신정책동향국내](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000341&category=G&category=F&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 소장자료/서지 계열 |
| `00000000000000000342` | [국립국어원_문화정보수어](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000342&category=G&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000343` | [국립국어원_전문용어수어](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000343&category=G&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000344` | [국립국어원_일상생활수어](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000344&category=G&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000347` | [한국데이터진흥원_연구보고서](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000347&category=G&category=&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000348` | [한국데이터진흥원_블로그디비디비](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000348&category=G&category=&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000349` | [한국데이터진흥원_데이터베이스백서](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000349&category=G&category=&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000350` | [국립국어원_외래어표기법](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000350&category=G&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000340` | [국립세종도서관_정책정보포털-최신정책동향국외](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000340&category=G&category=F&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 소장자료/서지 계열 |

</details>

<details>
<summary>H. 문화홍보 파일데이터 9건</summary>

| ID | 제목 | 하위분류/형식 | 구현 여부 | 비고 |
| --- | --- | --- | --- | --- |
| `00000000000000000479` | [한국체육산업개발(주)_올림픽공원 2025 입출차정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000479&category=H&category=E&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000458` | [국립중앙박물관_수어동영상](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000458&category=H&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000457` | [국립중앙박물관_국보보물 검색](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000457&category=H&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000456` | [국립중앙박물관_소장품 검색](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000456&category=H&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000306` | [한국체육산업개발(주)_홍보동영상](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000306&category=H&category=E&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000305` | [한국방문위원회_새소식](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000305&category=H&category=C&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000241` | [예술경영지원센터_문화예술 일자리 정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000241&category=H&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `99000000000000000007` | [한국문화정보원_큐레이팅 챗봇 도메인별 지식베이스-엔티티](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=99000000000000000007&category=H&category=H&dataType=FILE) | CSV / FILE | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `99000000000000000006` | [한국문화정보원_큐레이팅 챗봇 도메인별 지식베이스-인텐트](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=99000000000000000006&category=H&category=H&dataType=FILE) | CSV / FILE | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |

</details>

<details>
<summary>I. 맞춤형 API 파일데이터 39건</summary>

| ID | 제목 | 하위분류/형식 | 구현 여부 | 비고 |
| --- | --- | --- | --- | --- |
| `00000000000000000477` | [국립중앙박물관_문화행사(행사/공연)](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000477&category=I&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000421` | [한국문화정보원 외_전시정보(통합)](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000421&category=I&category=A&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000419` | [한국문화정보원_전국 관광지 주변_전기차 충전소](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000419&category=I&category=H&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000420` | [한국문화정보원_전국 시티투어 코스와 함께하는 맛집 정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000420&category=I&category=H&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000266` | [한국문화정보원_어린이를 위한 공연정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000266&category=I&category=H&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000260` | [한국문화정보원_소소하지만 확실한 여행](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000260&category=I&category=H&dataType=BATCH) | CSV / BATCH | 제외 | 한국관광공사 제공서비스 |
| `00000000000000000257` | [한국문화정보원_관광지 안전정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000257&category=I&category=H&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000259` | [한국문화정보원_문화기반시설 통계정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000259&category=I&category=H&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000285` | [한국문화정보원_국립공원 주변 문화시설 POI 정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000285&category=I&category=H&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000272` | [영상물등급위원회 외_무비갤러리](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000272&category=I&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000254` | [서울특별시청_반려 동물을 위한 지역 생활정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000254&category=I&category=H&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000271` | [한국학중앙연구원 외_한국의 향토문화](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000271&category=I&category=B&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 소장자료/서지 계열 |
| `00000000000000000274` | [한국정책방송원_역사기록정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000274&category=I&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000302` | [한국문화정보원_전통시장 주변 공영주차장 정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000302&category=I&category=H&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000303` | [한국문화정보원_초중고등학교 주변 도서관 정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000303&category=I&category=H&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000304` | [한국문화정보원_전국 박물관 미술관_공연행사](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000304&category=I&category=H&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000268` | [한국문화정보원 외_도서정보조회 서비스](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000268&category=I&category=H&dataType=BATCH) | CSV / BATCH | 제외 | 도서관 소장자료/서지 계열 |
| `00000000000000000121` | [한국문화정보원 외_공연정보(통합)](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000121&category=I&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000262` | [해외문화홍보원 외_이벤트 알림이](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000262&category=I&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000273` | [한국문화정보원_방방곳곳 트래킹 안내 서비스](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000273&category=I&category=H&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000269` | [한국문화정보원_장애인을 위한 시설정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000269&category=I&category=H&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000258` | [한국문화정보원_공공미술 작품을 찾아서](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000258&category=I&category=H&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000263` | [국립중앙박물관 외_문화교육의 시작](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000263&category=I&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000270` | [국립국어원 외_외국인을 위한 우리말 배우기](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000270&category=I&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000251` | [국립국어원 외_한국이 좋아요](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000251&category=I&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000261` | [문화체육관광부 외_사서의 책장](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000261&category=I&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000203` | [문화체육관광부_일자리정보-채용정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000203&category=I&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000200` | [문화체육관광부_일자리정보-시험정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000200&category=I&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000199` | [문화체육관광부_일자리정보-일자리뉴스](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000199&category=I&category=G&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000255` | [한국문화예술위원회 외_길 위의 작은 가게](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000255&category=I&category=A&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000252` | [제주특별자치도청 외_씽씽 자전거와 함께 하는 여행](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000252&category=I&category=D&dataType=BATCH) | CSV / BATCH | 제외 | 문화체육관광부 및 산하기관 범위 밖 |
| `00000000000000000256` | [한국문화관광연구원 외_맑은 하늘과 함께 하는 여행](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000256&category=I&category=C&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000264` | [인천문화재단 외_여행은 체험하는 것](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000264&category=I&category=H&dataType=BATCH) | CSV / BATCH | 제외 | 문화체육관광부 및 산하기관 범위 밖 |
| `00000000000000000250` | [국민체육진흥공단 외_어디서 운동할까](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000250&category=I&category=E&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000265` | [서울문화재단 외_문화부문 채용정보](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000265&category=I&category=C&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000253` | [한국문화정보원 외_가족과 함께하는 농어촌 체험일기](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000253&category=I&category=H&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000249` | [한국문화정보원 외_역사가 있는 여행 이야기](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000249&category=I&category=H&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |
| `00000000000000000248` | [한국문화정보원 외_공연과 함께하는 CO2 줄이기](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000248&category=I&category=H&dataType=BATCH) | CSV / BATCH | 확장 후보 | 여행앱의 위치/축제/여가 정보로 검토 가능 |
| `00000000000000000267` | [국립중앙박물관 외_지도로 보는 문화재 탐방](https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000267&category=I&category=B&dataType=BATCH) | CSV / BATCH | 미구현 | 현재 범위 밖 또는 세부 검토 필요 |

</details>

