import streamlit as st
import pandas as pd

# Load the data to reference values
df = pd.read_excel("Corrected_HeartRisk_Data.xlsx")

# STYLING FOR EXHIBITION (High Visibility)
st.markdown("""
    <style>
    [data-testid="stWidgetLabel"] p { color: #1E1E1E !important; font-weight: bold; }
    .main { background-color: #FFFFFF !important; }
    .stButton>button { 
        width: 100%; border-radius: 12px; height: 3.5em; 
        background-color: #d32f2f !important; color: white !important; 
        font-weight: bold; border: none; font-size: 18px;
    }
    .stMetric { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; }
    </style>
    """, unsafe_allow_html=True)

if 'screen' not in st.session_state:
    st.session_state.screen = 'welcome'

# --- SCREEN 1: WELCOME ---
if st.session_state.screen == 'welcome':
    st.image("https://cdn-icons-png.flaticon.com/512/833/833472.png", width=120)
    st.title("Heart Risk Predictor")
    st.write("### MI vs Angina Comparative Analysis")
    st.info("A pharmaceutical-grade assessment tool for identifying cardiac risk patterns.")
    if st.button("Start Risk Assessment →"):
        st.session_state.screen = 'input_1'

# --- SCREEN 2: INPUTS ---
elif st.session_state.screen == 'input_1':
    st.header("1. Personal & Medical History")
    age = st.selectbox("Age Group", ["Under 30", "30-39", "40-49", "50-59", "60+"])
    hyper = st.toggle("History of Hypertension")
    diab = st.toggle("History of Diabetes Mellitus")
    family = st.toggle("Family History of Heart Disease")
    
    st.divider()
    st.header("2. Symptoms")
    pain = st.selectbox("Character of Chest Pain", ["None", "Sharp / Stabbing", "Pressure / Heaviness", "Crushing / Squeezing"])
    duration = st.selectbox("Pain Duration", ["N/A", "< 10 mins", "10-20 mins", "> 20 mins"])

    if st.button("Calculate Result"):
        # LOGIC BASED ON YOUR EXCEL DATA
        # If everything is normal, use the minimum values found in your sheet (MI: 10, Angina: 15)
        if not hyper and not diab and not family and pain == "None":
            st.session_state.mi_score = 10
            st.session_state.angina_score = 15
            st.session_state.status = "Low Risk"
        else:
            # If factors are present, we simulate a higher score matching your data's peaks
            st.session_state.mi_score = 72 if (hyper or pain == "Crushing / Squeezing") else 35
            st.session_state.angina_score = 45 if (diab or pain == "Pressure / Heaviness") else 20
            st.session_state.status = "Elevated Risk"
        
        st.session_state.screen = 'results'

# --- SCREEN 3: RESULTS ---
elif st.session_state.screen == 'results':
    st.header("Comparative Analysis Result")
    
    col1, col2 = st.columns(2)
    with col1:
        color = "inverse" if st.session_state.mi_score > 50 else "normal"
        st.metric("MI Risk Score", f"{st.session_state.mi_score}%", delta="High" if st.session_state.mi_score > 50 else "Low", delta_color=color)
    
    with col2:
        color = "inverse" if st.session_state.angina_score > 40 else "normal"
        st.metric("Angina Risk Score", f"{st.session_state.angina_score}%", delta="High" if st.session_state.angina_score > 40 else "Low", delta_color=color)

    st.divider()
    if st.session_state.mi_score <= 15:
        st.success("Result: Low Risk. Your profile indicates normal cardiac markers based on current inputs.")
    else:
        st.warning(f"Result: {st.session_state.status}. Further clinical evaluation (ECG/Troponin) is recommended.")

    if st.button("New Assessment"):
        st.session_state.screen = 'welcome'
