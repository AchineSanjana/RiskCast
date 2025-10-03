import streamlit as st
import requests

st.set_page_config(page_title='Storm Damage Predictor', layout='wide', page_icon='⚡')

# CSS styling
st.markdown(""" 
    <style>
    .stApp {
        background: linear-gradient(180deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
    }
    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.98);
        padding: 2.5rem;
        border-radius: 8px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    h1 {
        color: #ffffff !important;
        text-align: center;
        font-size: 3.5rem !important;
        font-weight: 700 !important;
        letter-spacing: 3px;
        margin-bottom: 0.5rem !important;
        text-transform: uppercase;
        background: linear-gradient(135deg, #ffffff 0%, #a8c0ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        filter: drop-shadow(0 2px 10px rgba(255, 255, 255, 0.3));
    }
    .subtitle {
        color: #ffffff;
        text-align: center;
        font-size: 1.15rem;
        font-weight: 400;
        letter-spacing: 2px;
        margin-bottom: 3rem;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
        padding: 0.5rem;
        border-bottom: 2px solid rgba(255, 255, 255, 0.3);
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    .prediction-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 8px;
        color: white;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
    }
    .prediction-amount {
        font-size: 3.5rem;
        font-weight: 700;
        margin: 1rem 0;
        letter-spacing: -1px;
    }
    .prediction-label {
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        opacity: 0.9;
        font-weight: 300;
    }
    .severity-box {
        padding: 1.2rem;
        border-radius: 6px;
        margin: 1.5rem 0;
        border-left: 4px solid;
        font-weight: 500;
    }
    .severe { background: rgba(220, 53, 69, 0.1); border-color: #dc3545; color: #dc3545; }
    .high { background: rgba(255, 193, 7, 0.1); border-color: #ffc107; color: #f39c12; }
    .moderate { background: rgba(23, 162, 184, 0.1); border-color: #17a2b8; color: #17a2b8; }
    .low { background: rgba(40, 167, 69, 0.1); border-color: #28a745; color: #28a745; }
    .info-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.5rem;
        margin: 2rem 0;
    }
    .info-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 1.5rem;
        border-radius: 6px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.title('RISKCAST')
st.markdown('<center><p class="subtitle">Storm Damage Cost Predictor</p></center>', unsafe_allow_html=True)

# Info section
st.markdown("""
    <div class="info-grid">
        <div class="info-card">
            <h3>Data-Driven Analytics</h3>
            <p>Machine learning models trained on historical weather data</p>
        </div>
        <div class="info-card">
            <h3>Real-Time Assessment</h3>
            <p>Instant damage predictions based on event parameters</p>
        </div>
        <div class="info-card">
            <h3>Comprehensive Coverage</h3>
            <p>Multiple weather event types and geographic regions</p>
        </div>
    </div>
""", unsafe_allow_html=True)

with st.form('form'):
    col1, col2 = st.columns(2)

    with col1:
        event_type = st.selectbox("Event Type", ['Hail', 'Thunderstorm Wind', 'Tornado', 'Flood', 'Winter Storm'])
        state = st.text_input("State (e.g. TEXAS)")
        month = st.slider("Month", 1, 12, 6)

    with col2:
        season = st.selectbox("Season", ['DJF', 'MAM', 'JJA', 'SON'])
        magnitude = st.number_input("Magnitude", value=0.0)
        magnitude_type = st.selectbox("Magnitude Type", ['', 'EG', 'ES', 'MS', 'MG'])

    col3, col4 = st.columns(2)
    with col3:
        begin_lat = st.number_input("Latitude", value=0.0, format="%.4f")
    with col4:
        begin_lon = st.number_input("Longitude", value=0.0, format="%.4f")

    submit = st.form_submit_button("Generate Prediction", use_container_width=True)

if submit:
    with st.spinner("Processing prediction model..."):
        payload = {
            "EVENT_TYPE": event_type,
            "STATE": state,
            "MONTH": int(month),
            "SEASON": season,
            "MAGNITUDE": float(magnitude),
            "MAGNITUDE_TYPE": magnitude_type or None,
            "BEGIN_LAT": float(begin_lat),
            "BEGIN_LON": float(begin_lon),
        }
        try:
            r = requests.post("http://127.0.0.1:8000/predict", json=payload, timeout=15)
            r.raise_for_status()
            res = r.json()

            property_damage = res["property_damage"]
            crop_damage = res["crop_damage"]
            total_damage = res["total_damage"]

            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Property Damage", f"${property_damage:,.0f}")
            with col2:
                st.metric("Crop Damage", f"${crop_damage:,.0f}")
            with col3:
                st.metric("Total Damage", f"${total_damage:,.0f}")

            # Severity
            if total_damage > 1_000_000:
                st.error("🚨 CRITICAL ALERT: Losses exceed $1M")
            elif total_damage > 100_000:
                st.warning("⚠️ HIGH RISK: Losses exceed $100K")
            elif total_damage > 10_000:
                st.info("ℹ️ MODERATE RISK: Considerable losses possible")
            else:
                st.success("✅ LOW RISK: Minimal damage expected")

        except Exception as e:
            st.error(f"Error: {str(e)}")
