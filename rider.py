import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from ai_helper import ask_ai
from geopy.geocoders import Nominatim
import json

st.set_page_config(page_title="🚴 Rider - AI 자전거 경로 추천", layout="wide")

# 주소 -> 좌표 변환 캐시
@st.cache_data
def geocode_address(address):
    try:
        geolocator = Nominatim(user_agent="rider_app")
        location = geolocator.geocode(address + " 한국", timeout=5)
        if location:
            return (location.latitude, location.longitude)
    except Exception as e:
        st.warning(f"지오코딩 실패: {address} - {e}")
    return None

# CSV 데이터 로드
@st.cache_data
def load_bicycle_routes():
    df = pd.read_csv("SIXSEVEN.csv")
    return df

# 기본 자전거 종류별 특성
BIKE_TYPES = {
    "입문용 (편안함 중시)": {
        "width_min": 2.0,  # 최소 폭 2m 이상 (안전)
        "safety_score": "평탄하고 넓은 길",
        "description": "초보자도 안전하게 탈 수 있는 길"
    },
    "도시 자전거": {
        "width_min": 1.5,
        "safety_score": "도시 인프라 중심",
        "description": "도시 내 빠른 이동"
    },
    "로드 자전거": {
        "width_min": 1.0,
        "safety_score": "장거리 주행 최적화",
        "description": "긴 거리를 빠르게"
    },
    "산악 자전거": {
        "width_min": 2.0,
        "safety_score": "오프로드 주행",
        "description": "다양한 노면 대응"
    }
}

st.title("🚴 Rider - AI 자전거 경로 추천 시스템")
st.markdown("CSV 데이터 기반 경로 분석 + AI 추천")

# 데이터 로드
routes_df = load_bicycle_routes()

# 사이드바 설정
st.sidebar.header("⚙️ 경로 검색 설정")

# 자전거 종류 선택
bike_type = st.sidebar.selectbox(
    "자전거 종류 선택",
    list(BIKE_TYPES.keys())
)

# 출발지/도착지 입력
start_location = st.sidebar.text_input(
    "출발지 (예: 복정역, 판교역)",
    "복정역"
)

end_location = st.sidebar.text_input(
    "도착지 (예: 판교역, 낙생대공원)",
    "판교역"
)

# 안전성 우선순위
safety_priority = st.sidebar.slider(
    "안전성 우선순위 (1~5)",
    min_value=1,
    max_value=5,
    value=4,
    help="5일수록 안전한 길을 우선"
)

# AI로 경로 추천 받기
if st.sidebar.button("🤖 경로 추천 받기"):
    st.sidebar.info("AI가 경로를 분석 중입니다...")

    # CSV 데이터에서 관련 경로 필터링
    relevant_routes = routes_df[
        (routes_df['노선명'].str.contains('|'.join([start_location, end_location]), na=False, case=False)) |
        (routes_df['시점'].str.contains(start_location, na=False, case=False)) |
        (routes_df['종점'].str.contains(end_location, na=False, case=False))
    ]

    # AI 프롬프트 구성
    bike_info = BIKE_TYPES[bike_type]
    prompt = f"""
다음 자전거 도로 데이터를 분석하여 경로를 추천해주세요.

## 사용자 정보
- 자전거 종류: {bike_type}
- 출발지: {start_location}
- 도착지: {end_location}
- 안전성 우선순위: {safety_priority}/5

## 자전거 특성
- 권장 도로 폭: {bike_info['width_min']}m 이상
- 특징: {bike_info['safety_score']}

## 사용 가능한 도로 데이터
{relevant_routes[['노선명', '시점', '종점', '연장(킬로미터)', '폭(미터)', '포장종류', '도로종류']].to_string()}

## 요청
1. {bike_type}에 가장 적합한 경로를 2-3개 추천
2. 각 경로별 안전성 평가 (포장 상태, 도로 폭, 도로 종류 기반)
3. 총 거리 및 예상 시간
4. 각 경로의 장점/단점 정리

응답은 마크다운 형식으로 명확하게 구성해주세요.
"""

    # AI 호출
    try:
        recommendation = ask_ai(prompt)
        st.session_state.recommendation = recommendation
        st.session_state.start = start_location
        st.session_state.end = end_location
    except Exception as e:
        st.error(f"AI 추천 실패: {e}")

# 메인 콘텐츠 영역
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📍 자전거 도로 지도")

    # 지도 생성 (성남/판교 중심)
    m = folium.Map(
        location=[37.4, 127.1],
        zoom_start=12,
        tiles="OpenStreetMap"
    )

    # CSV 데이터에서 추출한 경로들을 지도에 표시
    # 주소 -> 좌표가 필요하지만, 여기서는 간단하게 일부 경로만 표시
    sample_locations = {
        "복정역": (37.4383, 127.1064),
        "판교역": (37.3937, 127.1110),
        "낙생대공원": (37.3650, 127.1150),
        "판교테크노14사거리": (37.3943, 127.1037),
    }

    # 출발지/도착지 마커 추가
    if start_location in sample_locations:
        lat, lon = sample_locations[start_location]
        folium.Marker(
            location=[lat, lon],
            popup=f"출발: {start_location}",
            icon=folium.Icon(color="green", icon="play")
        ).add_to(m)

    if end_location in sample_locations:
        lat, lon = sample_locations[end_location]
        folium.Marker(
            location=[lat, lon],
            popup=f"도착: {end_location}",
            icon=folium.Icon(color="red", icon="stop")
        ).add_to(m)

    # 모든 경로의 시작점 표시 (원형, 희미함)
    for idx, row in routes_df.head(20).iterrows():
        folium.CircleMarker(
            location=[37.3 + idx*0.01, 127.1 + (idx%10)*0.01],
            radius=3,
            popup=f"{row['노선명']}",
            color="blue",
            fill=True,
            fillOpacity=0.3
        ).add_to(m)

    # 지도 표시
    st_folium(m, width=700, height=500)

with col2:
    st.subheader("🎯 도로 데이터 요약")

    st.metric("전체 도로 수", len(routes_df))
    st.metric("평균 도로 폭", f"{routes_df['폭(미터)'].mean():.2f}m")
    st.metric("평균 연장", f"{routes_df['연장(킬로미터)'].mean():.2f}km")

    st.markdown("---")
    st.subheader("📊 도로 종류 분포")
    road_type_counts = routes_df['도로종류'].value_counts()
    st.bar_chart(road_type_counts)

    st.markdown("---")
    st.subheader("🛣️ 포장 종류 분포")
    paving_counts = routes_df['포장종류'].value_counts()
    for paving, count in paving_counts.items():
        st.write(f"• {paving}: {count}개")

# AI 추천 결과 표시
st.markdown("---")
if "recommendation" in st.session_state:
    st.subheader("🤖 AI 경로 추천 결과")
    st.info(f"📤 출발: {st.session_state.start} → 📥 도착: {st.session_state.end}")
    st.markdown(st.session_state.recommendation)
else:
    st.info("💡 왼쪽 사이드바에서 자전거 종류, 출발지, 도착지를 선택 후 '경로 추천 받기' 버튼을 클릭하세요.")

# 상세 데이터 보기
with st.expander("📋 전체 도로 데이터 보기"):
    st.dataframe(routes_df, use_container_width=True)
