import streamlit as st
import pandas as pd

# 1. THEME ADAPTATION: Removed hardcoded colors to allow auto-switching
st.markdown("""
    <style>
    .stApp { margin-top: -50px; }
    .stButton>button { 
        width: 100%; border-radius: 20px; height: 3.5em; 
        background-color: #d32f2f !important; color: white !important; font-weight: bold;
    }
    /* Simple styling for the result boxes */
    div[data-testid="marker-color"] { color: #d32f2f !important; }
    </style>
    """, unsafe_allow_html=True)

if 'screen' not in st.session_state:
    st.session_state.screen = 'welcome'

# --- SCREEN 1: WELCOME ---
if st.session_state.screen == 'welcome':
    st.title("❤️ Heart Risk Predictor")
    st.subheader("MI vs Angina Comparative Analysis")
    st.write("A research-based tool for clinical cardiac risk stratification.")
    
    st.info("**Instructions:** Please fill in all sections for an accurate comparative result.")
    if st.button("Begin Assessment"):
        st.session_state.screen = 'assessment'

# --- SCREEN 2: COMPREHENSIVE ASSESSMENT ---
elif st.session_state.screen == 'assessment':
    st.header("Cardiac Risk Profile")
    
    # Section A: Demographics & Lifestyle
    with st.expander("👤 Personal & Lifestyle Factors", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            age = st.selectbox("Age Group", ["Under 30", "30-39", "40-49", "50-59", "60-69", "70+"])
            gender = st.selectbox("Biological Gender", ["Male", "Female"])
            bmi = st.selectbox("BMI Category", ["Normal", "Overweight", "Obese"])
        with col2:
            location = st.selectbox("Location/Ethnicity", ["Urban", "Rural"])
            smoke = st.selectbox("Smoking Status", ["Never Smoked", "Current Smoker", "Passive Smoker"])
            activity = st.select_slider("Physical Activity", ["Sedentary", "Moderately Active", "Very Active"])

    # Section B: Medical History & Vitals
    with st.expander("🏥 Clinical History & Vitals", expanded=True):
        col3, col4 = st.columns(2)
        with col3:
            hyper = st.toggle("History of Hypertension")
            diab = st.toggle("Diabetes Mellitus")
            family = st.toggle("Family History (Premature IHD)")
        with col4:
            bp = st.selectbox("Blood Pressure Status", ["120/80 (Normal)", "Pre-hypertension", "Stage 1 High", "Stage 2 High"])
            lipid = st.selectbox("Lipid Profile Severity", ["Normal", "Borderline High", "High (Total >240 mg/dL)"])

    # Section C: Acute Symptom Analysis
    with st.expander("⚡ Symptom Characterization", expanded=True):
        pain_type = st.selectbox("Chest Pain Character", ["None", "Sharp / Stabbing", "Pressure / Heaviness", "Crushing / Squeezing", "Burning"])
        duration = st.selectbox("Pain Duration", ["N/A", "< 10 mins", "10-20 mins", "20-30 mins", "> 30 mins"])
        radiation = st.multiselect("Pain Radiation", ["Left Arm", "Right Arm", "Jaw / Neck", "Back / Shoulders"])
        trigger = st.selectbox("Pain Trigger", ["At Rest", "During Physical Activity", "Emotional Stress"])
        relief = st.radio("Pain Relief", ["None", "Relieved by rest", "Relieved by Nitroglycerin"], horizontal=True)
        
        associated = st.multiselect("Associated Symptoms", ["Shortness of Breath", "Nausea/Vomiting", "Sweating", "Palpitations", "Dizziness"])

    # Section D: Laboratory Markers
    with st.expander("🧪 Laboratory Findings", expanded=True):
        troponin = st.selectbox("Cardiac Troponin Level", ["Not Performed", "Negative / Normal", "Positive (Mildly Elevated)", "Positive (Significantly Elevated)"])

    if st.button("Generate Final Analysis"):
        # LOGIC CALCULATION (Based on your Research Data)
        mi_points = 10
        angina_points = 15
        
        # Risk Multipliers
        if hyper or bp != "120/80 (Normal)": mi_points += 15
        if diab: mi_points += 10; angina_points += 10
        if troponin == "Positive (Significantly Elevated)": mi_points += 50
        if pain_type == "Crushing / Squeezing": mi_points += 15
        if pain_type == "Pressure / Heaviness": angina_points += 20
        if "Left Arm" in radiation: mi_points += 10
        if relief == "Relieved by Nitroglycerin": angina_points += 15
        
        st.session_state.mi_res = min(mi_points, 98)
        st.session_state.angina_res = min(angina_points, 92)
        st.session_state.screen = 'results'

# --- SCREEN 3: RESULTS ---
elif st.session_state.screen == 'results':
    st.header("Comparative Analysis Result")
    
    st.metric("MI (Myocardial Infarction) Risk", f"{st.session_state.mi_res}%")
    st.progress(st.session_state.mi_res / 100)
    
    st.metric("Angina Pectoris Risk", f"{st.session_state.st.session_state.angina_res}%")
    st.progress(st.session_state.angina_res / 100)

    st.divider()
    if st.session_state.mi_res > 60:
        st.error("🚨 **High MI Risk:** Clinical markers strongly suggest acute coronary syndrome. Immediate medical attention and ECG/Troponin correlation required.")
    elif st.session_state.angina_res > 40:
        st.warning("⚠️ **Stable/Unstable Angina Risk:** Profile suggests ischemia likely related to exertion or coronary artery disease.")
    else:
        st.success("✅ **Low Risk:** Clinical markers are within the normal range for major cardiac events.")

    if st.button("New Assessment"):
        st.session_state.screen = 'welcome'
