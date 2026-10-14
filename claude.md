# 프로젝트 개요
공공데이터 csv를,지도 보여주는 Streamlit웹앱기획서는plan.md참고

## 파일 구조
- rider.py:메인앱(ui+로직)
- ai.helper.py:Cluade API를 사용하는 ask_ai() 함수 정의
- PLAN.md: 프로젝트기획서
- .env:ANTHROPIC_API_KEY보관

## 규칙
- 항상 PLAN.md 기획서를 기준으로 구현할 것
- API 호출은 반드시 ask_ai()함수를 거칠 것

- API Key는 .env에서 읽고 코드에 직접 쓰지 말것
- 주석은 한국어로 작성할 것