import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# ---------------------- 1. API 통신 함수 ----------------------
# **주의: YOUR_API_KEY를 실제 발급받은 키로 교체해야 합니다.**
API_KEY = "YOUR_API_KEY" 
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather_data(city):
    """지정된 도시의 현재 날씨 데이터를 OpenWeatherMap에서 가져옵니다."""
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric', 
        'lang': 'kr' 
    }
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        # 오류 처리
        print(f"Error fetching data: {response.status_code}")
        return None

# ---------------------- 2. Streamlit 인터페이스 함수 ----------------------
def display_weather(data):
    """가져온 날씨 데이터를 Streamlit에 표시합니다."""
    
    # 주요 정보 표시
    st.header(f"📍 {data['name']}의 현재 날씨")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="🌡️ 현재 기온", value=f"{data['main']['temp']:.1f} °C")
    with col2:
        st.metric(label="💧 습도", value=f"{data['main']['humidity']} %")
    with col3:
        st.metric(label="💨 바람 속도", value=f"{data['wind']['speed']} m/s")

    st.markdown(f"**날씨 상태:** {data['weather'][0]['description'].capitalize()}")
    
    # 간단한 시각화 (예: 온도/습도 바 그래프)
    temp_df = pd.DataFrame({
        '측정 항목': ['현재 기온', '최고 기온', '최저 기온'],
        '값': [data['main']['temp'], data['main']['temp_max'], data['main']['temp_min']]
    })
    
    fig = px.bar(temp_df, x='측정 항목', y='값', 
                 title='🌡️ 기온 변화', 
                 color='측정 항목', 
                 color_discrete_sequence=['red', 'darkred', 'blue'])
    st.plotly_chart(fig, use_container_width=True)

# ---------------------- 3. 메인 앱 실행 로직 ----------------------
st.title("🌎 실시간 도시별 날씨 정보 앱")
st.sidebar.header("설정")

city_name = st.sidebar.text_input("도시 이름을 입력하세요 (예: Seoul, Tokyo)", "Seoul")

if st.sidebar.button("날씨 정보 가져오기"):
    if city_name:
        with st.spinner('날씨 데이터 로딩 중...'):
            weather_data = get_weather_data(city_name)
            
        if weather_data:
            display_weather(weather_data)
        else:
            st.error(f"'{city_name}'에 대한 날씨 정보를 가져올 수 없습니다. 도시 이름을 다시 확인하거나 API 키를 점검하세요.")
    else:
        st.warning("도시 이름을 입력해 주세요.")
