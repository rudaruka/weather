import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# ---------------------- 1. 환경 설정 및 API 키 ----------------------
API_KEY = "4ac968497ca2e23e5be43af605f80058" 
# City ID 기반 요청을 위해 URL을 조금 변경합니다.
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
# 서울의 City ID
SEOUL_CITY_ID = 1835848

# ---------------------- 2. API 통신 함수 (ID 기반으로 변경) ----------------------
def get_weather_data_by_id(city_id):
    """지정된 도시 ID의 현재 날씨 데이터를 OpenWeatherMap에서 가져옵니다."""
    params = {
        'id': city_id, # <-- 도시 이름을 쓰는 'q' 대신 'id'를 사용합니다.
        'appid': API_KEY,
        'units': 'metric', 
        'lang': 'kr' 
    }
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data by ID: {response.status_code}")
        return None

# ---------------------- 3. Streamlit 인터페이스 함수 (변경 없음) ----------------------
# (display_weather 함수는 이전과 동일합니다.)

def display_weather(data):
    """가져온 날씨 데이터를 Streamlit에 표시하고 시각화합니다."""
    
    st.header(f"📍 {data['name']}의 현재 날씨")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="🌡️ 현재 기온", value=f"{data['main']['temp']:.1f} °C")
    with col2:
        st.metric(label="💧 습도", value=f"{data['main']['humidity']} %")
    with col3:
        st.metric(label="💨 바람 속도", value=f"{data['wind']['speed']} m/s")

    st.markdown(f"**날씨 상태:** {data['weather'][0]['description'].capitalize()}")
    
    temp_df = pd.DataFrame({
        '측정 항목': ['현재 기온', '최고 기온', '최저 기온'],
        '값': [data['main']['temp'], data['main']['temp_max'], data['main']['temp_min']]
    })
    
    fig = px.bar(temp_df, x='측정 항목', y='값', 
                 title='🌡️ 기온 변화', 
                 color='측정 항목', 
                 color_discrete_sequence=['red', 'darkred', 'blue'])
    st.plotly_chart(fig, use_container_width=True)


# ---------------------- 4. 메인 앱 실행 로직 (ID 요청으로 변경) ----------------------
st.title("🌎 실시간 도시별 날씨 정보 앱 (City ID)")
st.sidebar.header("설정")

# City ID 입력 필드 추가 (기본값 서울 ID)
city_id_input = st.sidebar.text_input("도시 ID를 입력하세요 (예: 서울: 1835848)", str(SEOUL_CITY_ID))

if st.sidebar.button("날씨 정보 가져오기"):
    try:
        # 입력된 문자열을 정수로 변환 시도
        selected_city_id = int(city_id_input)
        
        with st.spinner(f'ID {selected_city_id}의 날씨 데이터 로딩 중...'):
            weather_data = get_weather_data_by_id(selected_city_id) # ID 기반 함수 호출
            
        if weather_data:
            display_weather(weather_data)
        else:
            st.error(f"ID {selected_city_id}에 대한 날씨 정보를 가져올 수 없습니다. ID 또는 API 키를 점검하세요.")
            
    except ValueError:
        st.error("유효한 숫자 형태의 City ID를 입력해 주세요.")
