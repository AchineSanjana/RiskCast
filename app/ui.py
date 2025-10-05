import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title='Storm Damage Predictor', layout='wide', page_icon='⚡')

# ---------------------------
# LOAD MODEL
# ---------------------------
@st.cache_resource
def load_model():
    try:
        model = joblib.load("models/storm_damage_model.joblib")
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

model = load_model()

# ---------------------------
# STYLING
# ---------------------------
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
    .info-card h3 {
        color: white !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        margin-bottom: 0.5rem !important;
    }
    .info-card p {
        font-size: 0.9rem;
        opacity: 0.8;
        margin: 0;
    }
    .input-label {
        font-weight: 600;
        color: #2c3e50;
        font-size: 0.95rem;
        margin-bottom: 0.3rem;
        display: block;
    }
    .footer {
        text-align: center;
        color: rgba(255, 255, 255, 0.6);
        padding: 2rem 1rem;
        font-size: 0.85rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 3rem;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------
# HEADER
# ---------------------------
st.title('RISKCAST')
st.markdown('<center><p class="subtitle">USA Storm Damage Cost Predictor</p></center>', unsafe_allow_html=True)

# ---------------------------
# INFO CARDS
# ---------------------------
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

# ---------------------------
# FORM (unchanged)
# ---------------------------
with st.form('form'):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<span class="input-label">Event Type</span>', unsafe_allow_html=True)
        event_type = st.selectbox("Event Type", ['Hail', 'Thunderstorm Wind', 'Tornado', 'Flood', 'Winter Storm'], label_visibility="collapsed")

        st.markdown('<span class="input-label">State</span>', unsafe_allow_html=True)
        states_list = ['ALABAMA', 'ALASKA', 'AMERICAN SAMOA', 'ARIZONA', 'ARKANSAS', 'ATLANTIC NORTH',
                       'ATLANTIC SOUTH', 'CALIFORNIA', 'COLORADO', 'CONNECTICUT', 'DELAWARE',
                       'DISTRICT OF COLUMBIA', 'E PACIFIC', 'FLORIDA', 'GEORGIA', 'GUAM',
                       'GULF OF MEXICO', 'HAWAII', 'IDAHO', 'ILLINOIS', 'INDIANA', 'IOWA', 'KANSAS',
                       'KENTUCKY', 'LAKE ERIE', 'LAKE HURON', 'LAKE MICHIGAN', 'LAKE ONTARIO',
                       'LAKE ST CLAIR', 'LAKE SUPERIOR', 'LOUISIANA', 'MAINE', 'MARYLAND',
                       'MASSACHUSETTS', 'MICHIGAN', 'MINNESOTA', 'MISSISSIPPI', 'MISSOURI', 'MONTANA',
                       'NEBRASKA', 'NEVADA', 'NEW HAMPSHIRE', 'NEW JERSEY', 'NEW MEXICO', 'NEW YORK',
                       'NORTH CAROLINA', 'NORTH DAKOTA', 'OHIO', 'OKLAHOMA', 'OREGON', 'PENNSYLVANIA',
                       'PUERTO RICO', 'RHODE ISLAND', 'SOUTH CAROLINA', 'SOUTH DAKOTA', 'TENNESSEE',
                       'TEXAS', 'UTAH', 'VERMONT', 'VIRGINIA', 'WASHINGTON', 'WEST VIRGINIA',
                       'WISCONSIN', 'WYOMING']
        state = st.selectbox("State", states_list, label_visibility="collapsed")

        st.markdown('<span class="input-label">Month</span>', unsafe_allow_html=True)
        month = st.slider("Month", 1, 12, 6, label_visibility="collapsed")

    with col2:
        st.markdown('<span class="input-label">Magnitude (Optional)</span>', unsafe_allow_html=True)
        magnitude = st.number_input("Magnitude", value=0.0, label_visibility="collapsed")

        col_label, col_icon = st.columns([0.9, 0.1])
        with col_label:
            st.markdown('<span class="input-label">Magnitude Type</span>', unsafe_allow_html=True)
        with col_icon:
            with st.popover("ℹ️"):
                st.markdown("""
                **Magnitude Type Definitions:**
                - **EG** = Wind Estimated Gust
                - **ES** = Estimated Sustained Wind
                - **MS** = Measured Sustained Wind
                - **MG** = Measured Wind Gust
                *Note: No magnitude is included for instances of hail.*
                """)
        magnitude_type = st.selectbox("Magnitude Type", ['', 'EG', 'ES', 'MS', 'MG'], label_visibility="collapsed")

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<span class="input-label">Latitude</span>', unsafe_allow_html=True)
        begin_lat = st.number_input("Latitude", value=0.0, format="%.4f", label_visibility="collapsed")
    with col4:
        st.markdown('<span class="input-label">Longitude</span>', unsafe_allow_html=True)
        begin_lon = st.number_input("Longitude", value=0.0, format="%.4f", label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    submit = st.form_submit_button("Generate Prediction", use_container_width=True, type="primary")

# ---------------------------
# PREDICTION LOGIC (LOCAL)
# ---------------------------
if submit and model:
    with st.spinner("Processing prediction model..."):
        input_df = pd.DataFrame([{
            "EVENT_TYPE": event_type.upper(),
            "STATE": state.upper(),
            "MONTH": int(month),
            "MAGNITUDE": float(magnitude),
            "MAGNITUDE_TYPE": magnitude_type.upper() if magnitude_type else None,
            "BEGIN_LAT": float(begin_lat),
            "BEGIN_LON": float(begin_lon)
        }])

        try:
            preds = model.predict(input_df)[0]
            property_damage = max(0, float(preds[0]))
            crop_damage = max(0, float(preds[1]))
            total_damage = property_damage + crop_damage

            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            col1.metric("Property Damage", f"${property_damage:,.0f}")
            col2.metric("Crop Damage", f"${crop_damage:,.0f}")
            col3.metric("Total Damage", f"${total_damage:,.0f}")

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
            st.error(f"Prediction failed: {str(e)}")

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("""
    <div class="footer">
        <p>Powered by Advanced Machine Learning Algorithms | Historical Weather Data Analysis</p>
        <p>This system provides estimates only. Always follow official weather warnings and emergency management guidelines.</p>
    </div>
""", unsafe_allow_html=True)
