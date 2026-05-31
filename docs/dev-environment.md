# DEV ENVIRONMENT — 로컬 개발 환경 가이드

본 문서는 `python-mcst-api` 저장소의 로컬 개발 환경 구성 방법과 품질 검증 도구 활용법을 다룹니다.

---

## 1. 파이썬 개발 셋업

이 패키지는 Python 3.11 이상 환경에서 작동을 보장합니다.

### 1.1 가상환경 구축 (추천)
로컬에 종속성이 오염되지 않도록 `.venv` 가상환경을 생성하여 구동할 것을 적극 권장합니다.

```powershell
# 1. 가상환경 생성
python -m venv .venv

# 2. 가상환경 활성화 (PowerShell)
.venv\Scripts\Activate.ps1

# 3. 개발 의존성을 포함한 패키지 설치
pip install -e .[dev]
```

---

## 2. Windows PowerShell 한글 인코딩 설정

Windows 환경에서는 기본 PowerShell 인코딩으로 인해 한글 로그나 CLI 에러 메시지가 깨져 보일 수 있습니다.
따라서, 터미널 세션을 시작할 때마다 혹은 `.bash_profile`이나 PowerShell 프로필에 아래 인코딩 강제 지정을 우선 추가해주십시오.

```powershell
$OutputEncoding = [System.Text.UTF8Encoding]::new()
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
```

---

## 3. Windows Git 사용 원칙

이 저장소의 worktree는 `.git` 포인터가 Windows 경로(`F:\...`)를 가리킬 수 있으므로, WSL 기본 `git`은 상태 조회나 브랜치 작업에서 실패할 수 있습니다.
따라서 Git 관련 명령은 Windows Git (`git.exe`)를 기준으로 실행합니다.

```powershell
& "C:\Program Files\Git\cmd\git.exe" status
& "C:\Program Files\Git\cmd\git.exe" switch -c agent/example master
```

---

## 4. 품질 검증 파이프라인 (로컬 게이트)

PR을 원격 저장소에 Push하기 전에 작업자가 직접 아래 4가지 품질 게이트를 실행해 결함 유무를 체크합니다 (CI Actions는 보조 수단입니다).

### 4.1 1단계: 컴파일 검증
파이썬 소스 코드에 구문 에러(Syntax Error)가 없는지 빠르게 검사합니다.
```bash
python -m compileall src/mcst tests
```

### 4.2 2단계: 오프라인 단위 테스트
네트워크 호출 없이 `tests/fixtures/`의 mockup 응답들만을 활용해 파서 동작을 1.5초 이내에 빠르게 검증합니다.
```bash
python -m pytest
```

### 4.3 3단계: 코드 스타일 및 린트 검사
`ruff`를 가동하여 코드 스타일 정합성과 사용하지 않는 import, 불필요한 구문 등을 자동 검출합니다.
```bash
python -m ruff check .
```

### 4.4 4단계: 엄격한 타입 정적 검사
`mypy` strict 모드를 활용해 라이브러리 인터페이스의 모든 타입 어노테이션이 어긋나지 않는지 빈틈없이 체크합니다.
```bash
python -m mypy src/mcst
```

---

## 5. 실서버 통합 테스트 (Live Test)

실제 문화체육관광부 API 서버나 공공데이터포털 서버의 응답 규격이 깨지지 않았는지 가끔씩 live 상태로 확인해보고 싶을 때 구동합니다.
이 테스트를 수행하려면 공공데이터포털(`data.go.kr`)에서 발급받은 서비스 일반 키가 OS 환경 변수에 등록되어 있어야 합니다.

```powershell
# 1. API 키 설정 (임시)
$env:DATA_GO_KR_SERVICE_KEY = "발급받은_실제_서비스_키"

# 2. live 마커가 붙은 통합 테스트만 선별 실행
python -m pytest -m live
```

> [!CAUTION]
> 실서버 통합 테스트 도중 발생하는 에러 메시지나 URL 출력 로그에 API 키 값이 마스킹되지 않은 채 평문으로 유출되지 않도록 각별히 유의하십시오.
