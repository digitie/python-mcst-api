# 지원 데이터 카탈로그

## 포함 원칙

- 문화체육관광부 또는 산하기관/유관 공공기관 제공 자료만 포함합니다.
- 여행, 여가, 숙박, 문화시설, 위치/운영, 축제/행사 앱에 쓸 수 있는 자료만 포함합니다.
- 도서관은 위치/운영 정보만 포함하고, 소장자료/서지/ISBN/추천도서는 제외합니다.
- 한국관광공사 제공 서비스는 제외합니다.

현재 구현은 위 원칙에 맞춘 선별 구현입니다. 추후 `culture.go.kr`의 다른 OpenAPI와 파일데이터도 `mcst.catalog`에 원천 항목을 등록한 뒤 클라이언트 메서드를 추가하는 방식으로 확장할 수 있습니다.

전체 웹사이트 목록과 카테고리별 구현 여부는 [culture.go.kr 전체 목록 조사표](culture-go-kr-full-catalog.md)를 참고합니다.

디버그 UI에서 저장한 replay fixture의 구조와 테스트 방식은 [디버그 UI fixture와 replay 테스트](debug-fixtures.md)를 참고합니다.

## 카탈로그 함수

라이브러리에서 현재 선별 카탈로그를 JSON 직렬화 가능한 형태로 꺼낼 수 있습니다.

```python
from mcst import DatasetKind, get_api_catalog

for item in get_api_catalog(kind=DatasetKind.KCISA_OPEN_API):
    print(item["label"], item["endpoint_url"])
```

`label`은 `한국문화정보원_카페가 있는 서점데이터 (cafe_bookstores)`처럼
사람이 읽는 데이터셋명과 slug를 함께 담습니다.

문체부/KCISA API는 API별 활용 신청과 서비스키가 다를 수 있습니다. 단일
키를 모든 API에 쓰려면 `service_key="..."`를 넘기고, API별 키가 필요하면
slug를 기준으로 `service_keys`를 넘깁니다.

```python
import asyncio
from mcst import AsyncTokenBucket, McstClient


async def main():
    bucket = AsyncTokenBucket(max_rps=2, capacity=1)
    async with McstClient(rate_limiter=bucket) as client:
        page = await client.culture.cafe_bookstores(num_of_rows=10)
        print(page.total_count, page.items)
        libraries = await client.data_go.public_libraries(per_page=5)
        print(libraries.items)


if __name__ == "__main__":
    asyncio.run(main())
```

파일 CSV 조회는 다음과 같습니다.

```python
import asyncio
from mcst import McstClient


async def main():
    async with McstClient(max_rps=5) as client:
        rows = await client.file_data.read_csv("cafe_bookstores_csv")
        print(len(rows), rows[:1])
        async for row in client.file_data.iter_csv("public_libraries"):
            print(row)
            break


if __name__ == "__main__":
    asyncio.run(main())
```

## KCISA OpenAPI

| slug | 공식 데이터셋명 | 제공기관 | 원천 |
| --- | --- | --- | --- |
| `media_famous_places` | 한국문화정보원_미디어콘텐츠 영상 내 유명지 | 한국문화정보원 | https://www.culture.go.kr/data/openapi/openapiView.do?id=583&gubun=A |
| `barrier_free_places` | 한국문화정보원_전국 문화예술관광지 배리어프리 정보 | 한국문화정보원 | https://www.culture.go.kr/data/openapi/openapiView.do?id=584&gubun=A |
| `pet_friendly_culture_facilities` | 한국문화정보원_전국 반려동물 동반가능 문화시설 위치 | 한국문화정보원 | https://www.culture.go.kr/data/openapi/openapiView.do?id=585&gubun=A |
| `leisure_activity_facilities` | 한국문화정보원_전국 문화 여가 활동 시설(액티비티) | 한국문화정보원 | https://www.culture.go.kr/data/openapi/openapiView.do?id=587&gubun=A |
| `leisure_camping_facilities` | 한국문화정보원_전국 문화 여가 활동 시설(캠핑) | 한국문화정보원 | https://www.culture.go.kr/data/openapi/openapiView.do?id=588&gubun=A |
| `family_infant_culture_facilities` | 한국문화정보원_전국 가족 유아 동반 가능 문화시설 | 한국문화정보원 | https://www.culture.go.kr/data/openapi/openapiView.do?id=592&gubun=A |
| `world_restaurants` | 한국문화정보원_전국 세계음식점 | 한국문화정보원 | https://www.culture.go.kr/data/openapi/openapiView.do?id=594&gubun=A |
| `independent_bookstores` | 한국문화정보원_전국 독립서점 및 운영정보 | 한국문화정보원 | https://www.culture.go.kr/data/openapi/openapiView.do?id=623&gubun=A |
| `cafe_bookstores` | 한국문화정보원_카페가 있는 서점데이터 | 한국문화정보원 | https://www.culture.go.kr/data/openapi/openapiView.do?id=624&gubun=A |
| `used_bookstores` | 한국문화정보원_전국 중고서점 및 운영정보 | 한국문화정보원 | https://www.culture.go.kr/data/openapi/openapiView.do?id=547&gubun=A |
| `leisure_classes` | 한국문화정보원_전국 문화 여가 활동 시설(클래스) | 한국문화정보원 | https://www.culture.go.kr/data/openapi/openapiView.do?id=586&gubun=A |
| `recommended_travel_destinations` | 문화체육관광부_추천여행지 | 문화체육관광부 | https://www.culture.go.kr/data/openapi/openapiView.do?id=581&gubun=A |

## 파일 다운로드

| slug | 공식 데이터셋명 | 제공기관 | 원천 |
| --- | --- | --- | --- |
| `recommended_travel_destinations_csv` | 문화체육관광부_추천여행지 | 문화체육관광부 | https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000299&category=D&orderBy=dwldCnt&category=G&dataType=BATCH |
| `independent_bookstores_csv` | 한국문화정보원_전국 독립서점 및 운영정보 | 한국문화정보원 | https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000443&category=C&orderBy=dwldCnt&category=H&dataType=BATCH |
| `media_famous_places_csv` | 한국문화정보원_미디어콘텐츠 영상 내 유명지 | 한국문화정보원 | https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000412&category=D&orderBy=dwldCnt&category=H&dataType=BATCH |
| `tourism_attractions_csv` | 한국문화관광연구원 외_관광지정보 | 한국문화관광연구원 외 | https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000275&keyword=%EA%B4%80%EA%B4%91%EC%A7%80%EC%A0%95%EB%B3%B4&category=C&dataType=BATCH |
| `world_restaurants_csv` | 한국문화정보원_전국 세계음식점 | 한국문화정보원 | https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000416&category=D&orderBy=dwldCnt&category=H&dataType=BATCH |
| `pet_friendly_culture_facilities_csv` | 한국문화정보원_전국 반려동물 동반가능 문화시설 위치 | 한국문화정보원 | https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000414&category=D&orderBy=dwldCnt&category=H&dataType=BATCH |
| `barrier_free_places_csv` | 한국문화정보원_전국 문화예술관광지 배리어프리 정보 | 한국문화정보원 | https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000413&category=D&orderBy=dwldCnt&category=H&dataType=BATCH |
| `cafe_bookstores_csv` | 한국문화정보원_카페가 있는 서점데이터 | 한국문화정보원 | https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000444&category=C&orderBy=dwldCnt&category=H&dataType=BATCH |
| `leisure_activity_facilities_csv` | 한국문화정보원_전국 문화 여가 활동 시설(액티비티) | 한국문화정보원 | https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000243&category=C&orderBy=dwldCnt&category=H&dataType=BATCH |
| `leisure_classes_csv` | 한국문화정보원_전국 문화 여가 활동 시설(클래스) | 한국문화정보원 | https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000242&category=C&orderBy=dwldCnt&category=H&dataType=BATCH |
| `family_infant_culture_facilities_csv` | 한국문화정보원_전국 가족 유아 동반 가능 문화시설 | 한국문화정보원 | https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000246&category=C&orderBy=dwldCnt&category=H&dataType=BATCH |
| `children_bookstores_csv` | 한국문화정보원_전국 아동서점 운영정보 | 한국문화정보원 | https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000282&category=C&orderBy=dwldCnt&category=H&dataType=BATCH |
| `used_bookstores_csv` | 한국문화정보원_전국 중고서점 및 운영정보 | 한국문화정보원 | https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000286&category=B&category=H&dataType=BATCH |
| `leisure_camping_facilities_csv` | 한국문화정보원_전국 문화 여가 활동 시설(캠핑) | 한국문화정보원 | https://www.culture.go.kr/data/filedat/filedatDtl.do?fileDataNo=00000000000000000244&category=C&orderBy=dwldCnt&category=H&dataType=BATCH |
| `golf_courses_status` | 문화체육관광부_전국 골프장 현황 | 문화체육관광부 | https://www.data.go.kr/data/15118920/fileData.do |
| `public_libraries` | 문화체육관광부_국가도서관통계_전국공공도서관정보 | 문화체육관광부 | https://www.data.go.kr/data/15072611/fileData.do |

## ODCloud 파일 API

| slug | 공식 데이터셋명 | 제공기관 | 원천 |
| --- | --- | --- | --- |
| `tourism_lodging_status` | 문화체육관광부_전국 관광숙박시설 현황 | 문화체육관광부 | https://www.data.go.kr/data/3075666/fileData.do |
| `hotels_status` | 문화체육관광부_전국호텔현황 | 문화체육관광부 | https://www.data.go.kr/data/15118900/fileData.do |
| `public_sports_facilities` | 문화체육관광부_전국공공체육시설 현황 | 문화체육관광부 | https://www.data.go.kr/data/15119078/fileData.do |
| `registered_sports_businesses` | 문화체육관광부_전국 등록신고 체육시설업 현황 | 문화체육관광부 | https://www.data.go.kr/data/15123280/fileData.do |
| `marathon_events` | 문화체육관광부_국내마라톤대회 정보 | 문화체육관광부 | https://www.data.go.kr/data/15138980/fileData.do |

## 외부 연결 항목

| slug | 공식 데이터셋명 | 제공기관 | 원천 |
| --- | --- | --- | --- |
| `tourism_complexes` | 문화체육관광부_관광지 관광단지 현황 | 문화체육관광부 | https://www.data.go.kr/data/3075662/fileData.do |
| `tourism_special_zones` | 문화체육관광부_관광특구 현황 | 문화체육관광부 | https://www.data.go.kr/data/3075663/fileData.do |
| `recommended_travel_places` | 문화체육관광부_추천관광지 | 문화체육관광부 | https://www.data.go.kr/data/3070143/fileData.do |
| `traditional_temples` | 문화체육관광부_전통사찰 현황 | 문화체육관광부 | https://www.data.go.kr/data/3075623/fileData.do |
| `culture_infrastructure_status` | 문화체육관광부 전국문화기반시설 현황 | 문화체육관광부 | https://www.data.go.kr/data/3075558/fileData.do |
| `registered_performance_halls` | 문화체육관광부_전국 등록공연장 현황 | 문화체육관광부 | https://www.data.go.kr/data/3075660/fileData.do |

## 보류/제외

- `문화체육관광부_지역축제정보`: 문체부 명의지만 한국관광공사 대한민국 구석구석 연동 설명이 있어 제외했습니다.
- 국립중앙도서관 `소장자료`, `ISBN서지정보`, `국가자료종합목록`, `사서추천도서`: 도서관 위치/운영 정보가 아니라 제외했습니다.
- 한국관광공사 전체 서비스: 사용자 조건에 따라 제외했습니다.
- 지자체/행정안전부/농어촌공사 등 비문체부 제공 자료: 제외했습니다.


## 2026-09-14 파일 형식 확인

`public_sports_facilities` 원본은 XLSX, `registered_sports_businesses` 원본은
HWPX이다. `FileDataClient.download()`로 원본을 받고 각각의 형식에 맞게 처리한다.
`read_csv()`는 이 두 문서 형식의 파싱을 제공하지 않는다.
`public_libraries`는 기본 kind가 FILE_DOWNLOAD이므로 최상위 debug_fetch 대신
ODCloud 경로의 `client.data_go.debug_request("public_libraries")`를 사용한다.
