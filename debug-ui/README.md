# python-mcst-api 디버그 UI

이 폴더는 `mcst` 라이브러리를 호출해 응답을 확인하고 fixture JSON을 저장하는
Streamlit UI입니다. 라이브러리 본체는 Streamlit에 의존하지 않습니다.

## 실행

```bash
python -m pip install -r debug-ui/requirements.txt
python -m streamlit run debug-ui/app.py
```

개발 checkout에서 바로 실행할 수 있도록 `app.py`는 저장소의 `src/` 경로를 먼저
import 경로에 추가합니다. 패키지를 wheel 또는 editable install한 환경에서도 같은
앱을 사용할 수 있습니다.
