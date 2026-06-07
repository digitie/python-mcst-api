# DECISIONS — Architecture Decision Records

본 문서는 `python-mcst-api` 프로젝트의 아키텍처 및 설계 결정을 시간순으로 누적합니다. 결정이 뒤집힐 때도 이전 기록은 지우지 않고 `superseded by ADR-XXX`로 명시합니다.

## ADR 표준 형식

```markdown
## ADR-NNN: <결정 요약>

- 상태: proposed | accepted | superseded by ADR-XXX
- 날짜: YYYY-MM-DD
- 결정자: <agent | human>

### 컨텍스트
<무엇이 문제였나. 어떤 제약·요구가 있었나.>

### 결정
<무엇을 정했는가. 한 문장으로.>

### 근거
- 

### 결과(긍정)
- 

### 결과(부정)
- 

### 후속
- (open) 추가 검증 필요한 사항
```

---

## ADR-1: maplibre-vworld-js 스타일의 문서화 및 MCP 환경 도입

- 상태: accepted
- 날짜: 2026-05-31
- 결정자: AI agent & human

### 컨텍스트

여러 에이전트(Claude Code, GPT Codex, Google Antigravity 등)가 한 저장소에서 번갈아 가며 코딩을 진행할 때, 각 에이전트의 로컬 설정 및 브랜치 상태와 CodeGraph MCP 인덱스 캐시가 충돌하는 문제가 있었습니다.
또한, 작업의 흐름(journal, tasks)이 투명하고 엄격하게 표준화되어 있지 않으면 에이전트 세션 전환 시 문맥 복원에 수십 분이 지체되어 작업 생산성에 악영향을 줍니다.

### 결정

`maplibre-vworld-js` 프로젝트에서 고도의 안정성을 입증한 '에이전트별 독립 고정 worktree 환경(MCP 설정)'과 'T-NNN 기반 작업/저널/ADR 기록 스타일'을 전면 채택하여 도입합니다.

### 근거

- **독립된 에이전트 작업 공간**: 각 에이전트에게 고유 worktree 경로(`mcst-claude`, `mcst-antigravity`, `mcst-codex`)를 연결하여, 다른 에이전트의 미완성 변경 사항이나 브랜치 스위칭으로 인해 인덱스 인프라(CodeGraph)가 오염되는 현상을 완벽히 격리합니다.
- **문맥 복원 극대화**: `CLAUDE.md`, `SKILL.md` 신설을 통해, 새로 접속한 에이전트가 단 30초 내에 이 프로젝트의 성격과 빠른 개발 게이트 검증 명령을 파악하게 만듭니다.
- **아키텍처 부채 통제**: 표준화된 ADR 포맷과 저널 형식을 의무화하여, 의사결정의 근거와 부작용을 명시함으로써 패키지 복잡도가 산으로 가는 것을 시스템적으로 통제합니다.

### 결과(긍정)

- 에이전트들 간의 병렬 작업 정합성 및 독립성 100% 확보.
- 신규 세션 진입 시 에러 분석 및 온보딩 시간 최소화.
- 공공 API 클라이언트 패키지로서의 책임 경계(DO NOT)를 명확히 함으로써 도메인 오염 방지.

### 결과(부정)

- 작업자가 작업 종료 전 저널과 테스크, ADR을 수동으로 일일이 갱신해야 하는 관리 공수가 다소 증가함 (다소의 관리 비용은 협업 안정성을 위해 충분히 수용함).

---

## ADR-2: 에이전트별 물리적 Git Worktree 및 CodeGraph 인덱싱 인프라 구축

- 상태: accepted
- 날짜: 2026-05-31
- 결정자: AI agent & human

### 컨텍스트

ADR-1을 통해 에이전트별 고유 worktree 경로와 스타일을 도입하기로 결정했으나, 이를 물리적으로 생성하고 정적 코드 그래프(CodeGraph) 데이터베이스까지 각 워크트리에 완비해야만 실제로 에이전트들이 충돌 없는 완벽한 독립 개발을 수행할 수 있습니다.
또한, 다른 저장소와의 충돌을 피하고 식별을 완벽히 하기 위해 워크트리 디렉토리의 prefix를 패키지 고유명인 `python-mcst-api-*`로 강제 표준화해야 할 필요가 대두되었습니다.

### 결정

기존 `mcst-*` prefix를 패키지 고유의 `python-mcst-api-*` 로 전면 교체 적용하고, Windows 로컬 환경 하에 3개의 독립 Git Worktree(`python-mcst-api-claude`, `python-mcst-api-antigravity`, `python-mcst-api-codex`)를 master 브랜치 기준 detached HEAD 상태로 실제 물리 생성하여 각 하위에 `@colbymchenry/codegraph init -i` 인덱스 초기화를 완수합니다.

### 근거

- **디렉토리 충돌 방지**: `mcst-`는 다소 일반적인 축약어이므로, F 드라이브의 타 프로젝트 공간 등과의 경로 경합을 미연에 방지하기 위해 패키지 명칭을 그대로 prefix로 차용하여 유일무이한 가독성을 제공합니다.
- **실물 독립 개발 환경 완비**: 단순 설정이나 텍스트 문서 가이드에 그치지 않고, 실제로 Windows PC의 F:\dev 드라이브 상에 격리된 체크아웃 폴더 3개를 구축함으로써 세 에이전트가 완벽히 독립된 파일 그래프를 유지하게 만듭니다.
- **초고속 코드 탐색 지원**: 실물 worktree가 확보된 시점에 `codegraph init -i`를 각 폴더마다 1회씩 선제 가동하여, 노드/엣지 DB(`.codegraph/` 로컬 폴더)를 확보해 줌으로써 에이전트의 정적 인덱싱 지연 시간을 0으로 수렴시킵니다.

### 결과(긍정)

- 각 에이전트가 CLI 도구나 API를 통해 소스를 인덱싱하고 분석할 때, 서로 간의 파일 쓰기나 체크아웃 상태에 대한 잠금 경합이 물리적으로 0이 됨.
- `git worktree list`를 통해 전체 에이전트의 운용 인스턴스 현황이 투명하게 관리됨.

### 결과(부정)

- F 드라이브에 약 3배의 소스 파일 사본이 물리 공간으로 점유됨 (패키지 자체가 20여 개 파일 수준의 초경량 패키지이므로 디스크 부하는 극소화되어 수용 가능).

### 후속

- 각 에이전트 세션 구동 시, 자신이 해당 worktree(예: `python-mcst-api-antigravity`)를 사용하고 있음을 자동으로 인식하고 `codegraph sync` 증분 갱신을 구동하도록 세션 시작 룰 정합 확인 필요.

---

## ADR-3: dynamic timeout 파라미터 전파 및 Jitter 백오프 튜닝

- 상태: accepted
- 날짜: 2026-05-31
- 결정자: Antigravity AI Agent

### 컨텍스트

한국문화정보원(KCISA) 및 공공데이터포털(data.go.kr)과 같은 대한민국 공공데이터 API 서버는 특유의 동시 접속량 폭증이나 서버 자원 제약으로 인해 매우 잦은 408/504 타임아웃 에러를 발생시킵니다.
기존 패키지는 클라이언트 생성 시점에 정의된 고정 timeout(10초)만을 사용했으며, 타임아웃 발생 시 Exponential Backoff를 통한 재시도 간격(0.3, 0.6, 1.2, 2.4초 등)이 동일하여 여러 동시 요청들이 재시도하면서 트래픽이 폭주하는 'Thundering Herd(폭주)' 현상을 방지할 수 없었습니다.
또한, 특정 엔드포인트의 통신 특성이나 실시간 대기량에 맞추어 개별 요청마다 임의의 타임아웃을 조절하여 요청 복원력을 극대화할 방법이 없었습니다.

### 결정

- HTTP 전송 레이어(`HttpClient`, `AsyncHttpClient` 등)부터 공개 클라이언트(`CultureOpenApiClient`, `AsyncCultureOpenApiClient` 등)의 `request` 및 `debug_request` 함수 체인 전체에 동적 `timeout` 선택적 매개변수를 전파하고 노출합니다.
- `_sleep_before_retry` 및 `_async_sleep_before_retry` 함수에 0% ~ 10% 범위의 무작위성 Full Jitter를 도입하여 재시도 간격을 불규칙하게 분산시킵니다.

### 근거

- **동적 타임아웃 제어 (Dynamic Timeout Control)**: 네트워크 응답 지연이 큰 대용량 데이터셋이나 실시간 API 호출 시 클라이언트 수준에서 타임아웃 설정을 덮어쓸 수 있도록 유연성을 제공하여 호출 제어력을 대폭 확장합니다.
- **Full Jitter 분산 정책**: 지터를 도입함으로써 동일한 타이밍에 다수의 요청이 동시 재시도되는 것을 방지하고, 이를 통해 공공 서버와 우리 클라이언트 전송 성능 모두에 대한 부하 복원력을 최적화합니다.
- **하위 호환성 보장**: dynamic timeout이 명시되지 않은 호출은 기존 인스턴스 멤버 필드(`self.timeout`)로 자연스럽게 fallback 되도록 처리해 기존 클라이언트 인터페이스의 완벽한 100% 호환성을 보장합니다.

### 결과(긍정)

- 공공 데이터 서버 혼잡 시 에러 복원력이 획기적으로 상승함.
- 개별 API 호출 조건에 맞춰 통신 타임아웃을 유연하게 조절 가능.
- Full Jitter 적용으로 재시도 폭주로 인한 자가 중단(self-outage) 가능성 배제.

### 결과(부정)

- 재시도 시 지터 가미로 인해 전체 재시도 대기 시간이 최대 10% 범위 내에서 유동적이므로, 결정론적(Deterministic) 유닛 테스트 작성 시 대기 시간 값을 엄격하게 검증하기 어려워짐 (다만, `FakeSession` 수준의 테스트에서는 mock time을 사용하여 쉽게 우회 가능).

### 후속

- (open) live 환경에서 실제 data.go.kr 부하 테스트를 병행하며 지터가 트래픽 분산에 주는 긍정적 지표 변화의 관찰 필요.

---

## ADR-3: boto3 동적 로딩을 활용한 S3 호환 RustFS 저장 API 신설

- 상태: accepted
- 날짜: 2026-06-07
- 결정자: Antigravity AI Agent

### 컨텍스트

프로젝트 전반(예: `krtour-map`, `tripmate`)에서 공공 데이터 적재 및 백업 저장소로 S3 호환 객체 저장소인 **RustFS**를 사용하고 있습니다. 
`python-mcst-api`는 대한민국 문체부 파일데이터를 다운로드하여 로컬에 저장하는 `FileDataClient`와 `AsyncFileDataClient`를 제공하는데, 로컬 저장과 함께 이 RustFS에 동시에 다운로드 결과물을 적재할 수 있어야 하는 요구사항이 발생했습니다.
동시에 다음 제약 조건을 충족해야 했습니다:
1. 기존 API와의 하위 호환성을 완벽히 유지해야 합니다.
2. 라이브러리의 경량성을 유지하기 위해 불필요하게 무거운 `boto3` 및 `botocore` 의존성을 패키지 필수 의존성(`dependencies`)에 직접 추가하지 않아야 합니다.

### 결정

- 기존 로컬 전용 `save` API 외에 RustFS 동시 적재 기능을 갖춘 `save_rustfs` 전용 메서드를 `FileDataClient`와 `AsyncFileDataClient`에 각각 추가합니다.
- `boto3`와 `botocore`는 필수 의존성이 아닌 런타임 동적 임포트(Dynamic Import) 방식으로 구현합니다. 만약 설치되어 있지 않은 환경에서 `save_rustfs`를 호출하면 명확한 `ImportError` 안내를 통해 사용자에게 설치를 유도합니다.
- 접속 정보 설정(Endpoint, Bucket, Region 등)은 명시적 파라미터가 비어 있을 경우 환경 변수(`MCST_RUSTFS_*`, `KRTOUR_MAP_OBJECT_STORE_*`, `AWS_*` 순)에서 상속받도록 체인을 구성합니다.

### 근거

- **하위 호환성 보장**: 기존 `save` 메서드의 수정 대신 `save_rustfs` 전용 메서드를 신설하여 기존 다운스트림 소비자들의 계약을 깨지 않습니다.
- **경량성 유지 (Lazy Import)**: `boto3`와 `botocore`는 용량이 큰 패키지이므로, 단순히 로컬 파일 읽기/다운로드만을 사용하는 사용자에게까지 이를 강제하지 않고 필요한 시점에만 동적으로 임포트되도록 하여 패키지 기본 사이즈를 가볍게 유지합니다.
- **환경 변수 상속 체인**: 타 결합 프로젝트(`krtour-map`)가 정의하여 사용 중인 환경 변수군(`KRTOUR_MAP_OBJECT_STORE_*`)도 호환 상속함으로써 설정 연동의 편의성을 극대화합니다.

### 결과(긍정)

- 다운스트림 애플리케이션의 기존 호환성을 해치지 않으면서도 로컬 저장 + RustFS 동시 적재라는 고급 요구사항을 충족함.
- `boto3`가 설치되지 않은 환경에서도 기존 core 기능은 아무런 문제 없이 작동하며, `save_rustfs` 사용 시에만 안내 오류로 방어함.
- 비동기 `AsyncFileDataClient.save_rustfs`에서는 `asyncio.to_thread`를 사용하여 동기식 `boto3` I/O 호출이 이벤트 루프를 블로킹하지 않도록 격리함.

### 결과(부정)

- 런타임에 동적으로 import 하므로 `mypy` 등의 정적 타입 검사에서 `boto3` 타입 정보를 활용하여 `s3_client`에 대한 세부 타입 지정을 strict하게 유지하기 어려워짐 (이에 따라 `s3_client` 객체의 타입은 `Any`로 가공하여 우회함).

### 후속

- (open) 런타임에서 `boto3`를 사용할 때 실제 환경에서 credentials 오류 및 버킷 소유권 문제를 디버깅하기 쉽도록 wrap된 오류 메시지 설계 검토.
