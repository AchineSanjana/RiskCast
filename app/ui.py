import streamlit as st
import requests

st.set_page_config(page_title='Storm Damage Predictor', layout='centered')
st.title('🌩️ Storm Damage Predictor')

with st.form('form'):
    event_type = st.selectbox('Event Type', ['Hail','Thunderstorm Wind','Tornado','Flood','Winter Storm'])
    state = st.text_input('State (e.g., TEXAS)')
    month = st.slider('Month', 1, 12, 6)
    season = st.selectbox('Season', ['DJF','MAM','JJA','SON'])
    magnitude = st.number_input('Magnitude (optional)', value=0.0)
    magnitude_type = st.selectbox('Magnitude Type', ['', 'EG','ES','MS','MG'])
    begin_lat = st.number_input('Begin Lat', value=0.0)
    begin_lon = st.number_input('Begin Lon', value=0.0)
    submit = st.form_submit_button('Predict')

if submit:
    payload = {
        'event_type': event_type,
        'state': state,
        'month': int(month),
        'season': season,
        'magnitude': float(magnitude) if magnitude else None,
        'magnitude_type': magnitude_type or None,
        'begin_lat': float(begin_lat) if begin_lat else None,
        'begin_lon': float(begin_lon) if begin_lon else None,
    }
    try:
        r = requests.post('http://127.0.0.1:8000/predict', json=payload, timeout=15)
        r.raise_for_status()
        pred = r.json()['predicted_damage_property']
        st.success(f'Estimated property damage: ${pred:,.0f}')
    except Exception as e:
        st.error(f'API Error: {e} — Is FastAPI running at http://127.0.0.1:8000 ?')
