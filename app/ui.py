import streamlit as st
import requests

st.set_page_config(page_title='Storm Damage Predictor', layout='wide', page_icon='⚡')

# Professional CSS styling
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
    .stAlert {
        border-radius: 6px;
        border-left: 4px solid;
        font-size: 1rem;
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
    .prediction-context {
        font-size: 1rem;
        opacity: 0.85;
        margin-top: 0.5rem;
    }
    .severity-box {
        padding: 1.2rem;
        border-radius: 6px;
        margin: 1.5rem 0;
        border-left: 4px solid;
        font-weight: 500;
    }
    .severe { 
        background: rgba(220, 53, 69, 0.1); 
        border-color: #dc3545;
        color: #dc3545;
    }
    .high { 
        background: rgba(255, 193, 7, 0.1); 
        border-color: #ffc107;
        color: #f39c12;
    }
    .moderate { 
        background: rgba(23, 162, 184, 0.1); 
        border-color: #17a2b8;
        color: #17a2b8;
    }
    .low { 
        background: rgba(40, 167, 69, 0.1); 
        border-color: #28a745;
        color: #28a745;
    }
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
    .section-header {
        color: #2c3e50;
        font-size: 1.2rem;
        font-weight: 600;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e0e0e0;
    }
    .input-label {
        font-weight: 600;
        color: #2c3e50;
        font-size: 0.95rem;
        margin-bottom: 0.3rem;
        display: block;
    }
    .stSelectbox label, .stTextInput label, .stSlider label, .stNumberInput label {
        font-weight: 600 !important;
        color: #2c3e50 !important;
        font-size: 0.95rem !important;
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
    st.markdown('<div class="section-header">Event Parameters</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<span class="input-label">Event Type</span>', unsafe_allow_html=True)
        event_type = st.selectbox(
            'Event Type', 
            ['Hail','Thunderstorm Wind','Tornado','Flood','Winter Storm'],
            help="Select the type of severe weather event",
            label_visibility="collapsed"
        )
        st.markdown('<span class="input-label">State</span>', unsafe_allow_html=True)
        state = st.text_input(
            'State', 
            placeholder="e.g., TEXAS",
            help="Enter state name in capital letters",
            label_visibility="collapsed"
        )
        st.markdown('<span class="input-label">Month</span>', unsafe_allow_html=True)
        month = st.slider(
            'Month', 
            1, 12, 6,
            help="Select the month when the event occurred",
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown('<span class="input-label">Season</span>', unsafe_allow_html=True)
        season = st.selectbox(
            'Season', 
            ['DJF','MAM','JJA','SON'],
            help="DJF (Winter), MAM (Spring), JJA (Summer), SON (Fall)",
            label_visibility="collapsed"
        )
        st.markdown('<span class="input-label">Magnitude (Optional)</span>', unsafe_allow_html=True)
        magnitude = st.number_input(
            'Magnitude (Optional)', 
            value=0.0,
            help="Event magnitude measurement",
            label_visibility="collapsed"
        )
        st.markdown('<span class="input-label">Magnitude Type</span>', unsafe_allow_html=True)
        magnitude_type = st.selectbox(
            'Magnitude Type', 
            ['', 'EG','ES','MS','MG'],
            help="Classification of magnitude measurement",
            label_visibility="collapsed"
        )
    
    st.markdown('<div class="section-header">Geographic Coordinates</div>', unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown('<span class="input-label">Latitude</span>', unsafe_allow_html=True)
        begin_lat = st.number_input(
            'Latitude', 
            value=0.0,
            format="%.4f",
            help="Starting latitude coordinate",
            label_visibility="collapsed"
        )
    
    with col4:
        st.markdown('<span class="input-label">Longitude</span>', unsafe_allow_html=True)
        begin_lon = st.number_input(
            'Longitude', 
            value=0.0,
            format="%.4f",
            help="Starting longitude coordinate",
            label_visibility="collapsed"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    submit = st.form_submit_button('Generate Prediction', use_container_width=True, type="primary")

if submit:
    with st.spinner('Processing prediction model...'):
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
            pred = r.json()['predicted_damage']
            
            st.markdown("---")
            
            # Display result
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                st.markdown(f"""
                    <div class="prediction-container">
                        <div class="prediction-label">Estimated Property Damage</div>
                        <div class="prediction-amount">${pred:,.0f}</div>
                        <div class="prediction-context">{event_type} Event | {state}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Severity assessment
            if pred > 1000000:
                st.markdown("""
                    <div class="severity-box severe">
                        <strong>CRITICAL ALERT:</strong> Catastrophic damage predicted. Immediate evacuation protocols should be initiated. Expected losses exceed $1M.
                    </div>
                """, unsafe_allow_html=True)
            elif pred > 100000:
                st.markdown("""
                    <div class="severity-box high">
                        <strong>HIGH RISK:</strong> Significant structural damage anticipated. Implement emergency preparedness measures and secure critical infrastructure.
                    </div>
                """, unsafe_allow_html=True)
            elif pred > 10000:
                st.markdown("""
                    <div class="severity-box moderate">
                        <strong>MODERATE RISK:</strong> Considerable property damage possible. Recommended to secure loose items and prepare emergency response plans.
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div class="severity-box low">
                        <strong>LOW RISK:</strong> Minimal property damage expected. Standard precautionary measures advised.
                    </div>
                """, unsafe_allow_html=True)
                
        except requests.exceptions.ConnectionError:
            st.error('**Connection Error:** Unable to establish connection with the prediction API. Verify that FastAPI service is running at http://127.0.0.1:8000')
        except requests.exceptions.Timeout:
            st.error('**Timeout Error:** The prediction service did not respond within the expected timeframe. Please retry your request.')
        except requests.exceptions.HTTPError as e:
            st.error(f'**API Error:** HTTP {e.response.status_code} - {e.response.text}')
        except Exception as e:
            st.error(f'**System Error:** An unexpected error occurred - {str(e)}')

# Footer
st.markdown("""
    <div class="footer">
        <p>Powered by Advanced Machine Learning Algorithms | Historical Weather Data Analysis</p>
        <p>This system provides estimates only. Always follow official weather warnings and emergency management guidelines.</p>
    </div>
""", unsafe_allow_html=True)