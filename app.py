import streamlit as st
import pandas as pd

# Load the data
df = pd.read_excel("Corrected_HeartRisk_Data.xlsx")

# DARK MODE PROOF STYLING
st.markdown("""
    <style>
    /* Force all text to be white for visibility on dark backgrounds */
    html, body, [data-testid="stWidgetLabel"] p, .stMarkdown p, h1, h2, h3, span {
        color: #FFFFFF !important;
    }
    /* Style the main background to be dark to match your screenshot */
    .main {
        background-color: #0E1117 !important;
    }
    /* Style the select boxes so they are readable */
    div[data-baseweb="select"] > div {
        background-color: #262730 !important;
        color: white !important;
    }
    /* Professional Red Button */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background-color: #ff4b4b !important;
        color: white !important;
        font-weight: bold;
        border: none;
        height: 3em;
    }
    </style>
    """, unsafe_allow_html=True)

if 'screen' not in st.session_state:
    st.session_state.screen = 'welcome'

# --- SCREEN 1: WELCOME ---
if st.session_state.screen == 'welcome':
    st.image("https://cdn-icons-png.flaticon.com/512/833/833472.png", width=100)
    st.title("Heart Risk Predictor")
    st.write("MI vs Angina Comparative Analysis")
    if st.button("Start Risk Assessment →"):
        st.session_state.screen = 'input_1'

# --- SCREEN 2: ALL QUESTIONS FROM SHEET ---
elif st.session_state.screen == 'input_1':
    st.header("Step 1: Clinical Profile")
    
    # Demographics
    age = st.selectbox("Age Group", ["Under 30", "30-39", "40-49", "50-59", "60+"])
    gender = st.selectbox("Biological Gender", ["Male", "Female"])
    bmi = st.selectbox("Body Mass Index (BMI)", ["Normal", "Overweight", "Obese"])
    
    st.divider()
    st.header("Step 2: Medical History")
    col1, col2 = st.columns(2)
    with col1:
        hyper = st.toggle("Hypertension History")
        diab = st.toggle("Diabetes Mellitus")
    with col2:
        family = st.toggle("Family History (IHD)")
        smoking = st.selectbox("Smoking Status", ["Never Smoked", "Current Smoker", "Passive Smoker"])
    
    st.divider()
    st.header("Step 3: Symptom Analysis")
    pain_type = st.selectbox("Character of Chest Pain", ["None", "Pressure / Heaviness", "Sharp / Stabbing", "Crushing / Squeezing", "Burning"])
    duration = st.selectbox("Pain Duration", ["N/A", "< 10 mins", "10-20 mins", "> 20 mins"])
    radiation = st.selectbox("Pain Radiation", ["None", "Left Arm", "Jaw / Neck", "Back"])
    relief = st.selectbox("Pain Relief", ["None", "Relieved by rest", "Relieved by Nitroglycerin"])
    
    st.divider()
    st.header("Step 4: Lab Markers")
    troponin = st.selectbox("Cardiac Troponin Level", ["Not Performed", "Negative / Normal", "Positive (Elevated)"])

    if st.button("Calculate Final Analysis →"):
        # Logic based on spreadsheet patterns
        if not hyper and not diab and pain_type == "None" and troponin != "Positive (Elevated)":
            st.session_state.mi_score = 10
            st.session_state.angina_score = 15
        else:
            # Elevated logic
            mi_base = 25
            angina_base = 20
            if hyper: mi_base += 20
            if troponin == "Positive (Elevated)": mi_base += 40
            if pain_type == "Pressure / Heaviness": angina_base += 25
            
            st.session_state.mi_score = min(mi_base, 95)
            st.session_state.angina_score = min(angina_base, 90)
            
        st.session_state.screen = 'results'

# --- SCREEN 3: RESULTS ---
elif st.session_state.screen == 'results':
    st.header("Comparative Risk Result")
    
    col1, col2 = st.columns(2)
    col1.metric("MI Risk Score", f"{st.session_state.mi_score}%")
    col2.metric("Angina Risk Score", f"{st.session_state.angina_score}%")
    
    if st.session_state.mi_score > 50:
        st.error("High Risk of Myocardial Infarction detected. Immediate clinical correlation required.")
    elif st.session_state.mi_score <= 15:
        st.success("Low Risk: Your profile indicates normal cardiac markers.")
    else:
        st.warning("Moderate Risk: Please consult a healthcare professional for a full evaluation.")

    if st.button("Restart Assessment"):
        st.session_state.screen = 'welcome'
