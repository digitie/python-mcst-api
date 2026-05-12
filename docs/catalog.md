# 지원 데이터 카탈로그

## 포함 원칙

- 문화체육관광부 또는 산하기관/유관 공공기관 제공 자료만 포함합니다.
- 여행, 여가, 숙박, 문화시설, 위치/운영, 축제/행사 앱에 쓸 수 있는 자료만 포함합니다.
- 도서관은 위치/운영 정보만 포함하고, 소장자료/서지/ISBN/추천도서는 제외합니다.
- 한국관광공사 제공 서비스는 제외합니다.

현재 구현은 위 원칙에 맞춘 선별 구현입니다. 추후 `culture.go.kr`의 다른 OpenAPI와 파일데이터도 `mcst.catalog`에 원천 항목을 등록한 뒤 클라이언트 메서드를 추가하는 방식으로 확장할 수 있습니다.

전체 웹사이트 목록과 카테고리별 구현 여부는 [culture.go.kr 전체 목록 조사표](culture-go-kr-full-catalog.md)를 참고합니다.

## 구현된 API

| slug | 제공기관 | 원천 |
| --- | --- | --- |
| `leisure_activity_facilities` | 한국문화정보원 | https://www.culture.go.kr/data/openapi/openapiView.do?id=587&gubun=A |
| `leisure_camping_facilities` | 한국문화정보원 | https://www.culture.go.kr/data/openapi/openapiView.do?id=588&gubun=A |
| `family_infant_culture_facilities` | 한국문화정보원 | https://www.culture.go.kr/data/openapi/openapiView.do?id=592&gubun=A |
| `independent_bookstores` | 한국문화정보원 | https://www.culture.go.kr/data/openapi/openapiView.do?id=623&gubun=A |
| `cafe_bookstores` | 한국문화정보원 | https://www.culture.go.kr/data/openapi/openapiView.do?id=624&gubun=A |
| `barrier_free_places` | 한국문화정보원 | https://www.culture.go.kr/data/openapi/openapiView.do?id=584&gubun=A |
| `pet_friendly_culture_facilities` | 한국문화정보원 | https://www.culture.go.kr/data/openapi/openapiView.do?id=585&gubun=A |
| `media_famous_places` | 한국문화정보원 | https://www.culture.go.kr/data/openapi/openapiView.do?id=583&gubun=A |
| `multilingual_guide_culture_facilities` | 한국문화정보원 | https://www.culture.go.kr/data/openapi/openapiView.do?id=593&gubun=A |
| `world_restaurants` | 한국문화정보원 | https://www.culture.go.kr/data/openapi/openapiView.do?id=594&gubun=A |
| `small_theaters` | 한국문화정보원 | https://www.culture.go.kr/data/openapi/openapiView.do?id=595&gubun=A |
| `meeting_seminar_facilities` | 한국문화정보원 | https://www.culture.go.kr/data/openapi/openapiView.do?id=596&gubun=A |

## 구현된 파일 데이터

| slug | 제공기관 | 원천 |
| --- | --- | --- |
| `family_infant_culture_facilities_csv` | 한국문화정보원 | https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000246&category=C&orderBy=dwldCnt&category=H&dataType=BATCH |
| `independent_bookstores_csv` | 한국문화정보원 | https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000443&category=C&orderBy=dwldCnt&category=H&dataType=BATCH |
| `cafe_bookstores_csv` | 한국문화정보원 | https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000444&category=C&orderBy=dwldCnt&category=H&dataType=BATCH |
| `leisure_activity_facilities_csv` | 한국문화정보원 | https://www.data.go.kr/data/15111393/fileData.do |
| `leisure_camping_facilities_csv` | 한국문화정보원 | https://www.data.go.kr/data/15111395/fileData.do |
| `leisure_classes_csv` | 한국문화정보원 | https://www.data.go.kr/data/15111397/fileData.do |
| `world_restaurants_csv` | 한국문화정보원 | https://www.data.go.kr/data/15111398/fileData.do |
| `tourism_lodging_status` | 문화체육관광부 | https://www.data.go.kr/data/3075666/fileData.do |
| `hotels_status` | 문화체육관광부 | https://www.data.go.kr/data/15118900/fileData.do |
| `public_libraries` | 문화체육관광부 | https://www.data.go.kr/data/15072611/fileData.do |
| `small_libraries` | 문화체육관광부 | https://www.data.go.kr/data/15152519/fileData.do |

## 보류/제외

- `문화체육관광부_지역축제정보`: 문체부 명의지만 한국관광공사 대한민국 구석구석 연동 설명이 있어 제외했습니다.
- 국립중앙도서관 `소장자료`, `ISBN서지정보`, `국가자료종합목록`, `사서추천도서`: 도서관 위치/운영 정보가 아니라 제외했습니다.
- 한국관광공사 전체 서비스: 사용자 조건에 따라 제외했습니다.
- 지자체/행정안전부/농어촌공사 등 비문체부 제공 자료: 제외했습니다.
