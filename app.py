import streamlit as st
import pandas as pd

# 1. UI CONFIG & THEME (Auto-adjusts to Light/Dark mode)
st.set_page_config(page_title="Heart Risk Analyzer", page_icon="❤️", layout="centered")

st.markdown("""
    <style>
    /* Professional styling that works in both themes */
    .main { padding-top: 2rem; }
    .stMetric { 
        background-color: rgba(211, 47, 47, 0.05); 
        padding: 20px; 
        border-radius: 15px; 
        border: 1px solid #d32f2f;
    }
    .stButton>button {
        width: 100%; border-radius: 25px; height: 3.5em;
        background-color: #d32f2f !important; color: white !important;
        font-weight: bold; font-size: 18px; border: none;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

if 'screen' not in st.session_state:
    st.session_state.screen = 'welcome'

# --- SCREEN 1: WELCOME (EYE-CATCHING) ---
if st.session_state.screen == 'welcome':
    st.image("https://cdn-icons-png.flaticon.com/512/833/833472.png", width=100)
    st.title("Heart Risk Predictor")
    st.markdown("### **MI vs Angina Comparative Analysis**")
    st.write("Enter clinical data to generate a dual-risk assessment report.")
    
    with st.container():
        st.info("🎯 **Exhibition Mode Active**: This tool uses clinical markers to differentiate between Myocardial Infarction and Angina Pectoris.")
        if st.button("Start New Assessment →"):
            st.session_state.screen = 'assessment'

# --- SCREEN 2: COMPREHENSIVE CLINICAL INPUTS ---
elif st.session_state.screen == 'assessment':
    st.header("📋 Clinical Assessment")
    
    with st.form("risk_form"):
        # Section 1: Vitals & Lab Markers (The "More Questions" part)
        st.subheader("🧪 Laboratory & Clinical Markers")
        c1, c2 = st.columns(2)
        with c1:
            bp = st.selectbox("Blood Pressure (mmHg)", ["120/80 (Normal)", "140/90 (Stage 1)", "160/100 (Stage 2)", "Crisis (>180)"])
            sugar = st.selectbox("Fasting Sugar / HbA1c", ["Normal (<100mg/dL)", "Pre-diabetic", "Diabetic (>126mg/dL)"])
        with c2:
            ldl = st.selectbox("LDL Cholesterol (mg/dL)", ["Desirable (<100)", "Borderline (130-159)", "High (>160)"])
            troponin = st.selectbox("Cardiac Troponin Level", ["Negative / Normal", "Positive (Mildly Elevated)", "Positive (Significantly Elevated)"])

        # Section 2: Symptoms
        st.subheader("⚡ Symptom Analysis")
        pain_type = st.selectbox("Character of Chest Pain", ["None", "Sharp / Stabbing", "Pressure / Heaviness", "Crushing / Squeezing"])
        radiation = st.multiselect("Pain Radiation", ["None", "Left Arm", "Jaw / Neck", "Back", "Right Arm"])
        duration = st.selectbox("Pain Duration", ["< 5 mins", "5-20 mins", "20-30 mins", "> 30 mins"])
        
        # Section 3: History
        st.subheader("🏥 Patient History")
        colA, colB, colC = st.columns(3)
        h_bp = colA.checkbox("Hypertension")
        h_dm = colB.checkbox("Diabetes")
        h_fh = colC.checkbox("Family History")

        submit = st.form_submit_button("Generate Comparative Analysis")

        if submit:
            # DYNAMIC LOGIC CALCULATOR
            mi = 10
            angina = 15
            
            # MI Points
            if troponin == "Positive (Significantly Elevated)": mi += 60
            if "Left Arm" in radiation: mi += 15
            if duration == "> 30 mins": mi += 10
            if bp == "Crisis (>180)": mi += 5
            
            # Angina Points
            if pain_type == "Pressure / Heaviness": angina += 30
            if duration == "5-20 mins": angina += 20
            if ldl == "High (>160)": angina += 10
            
            # Cap at 98%
            st.session_state.mi_res = min(mi, 98)
            st.session_state.angina_res = min(angina, 95)
            st.session_state.screen = 'results'
            st.rerun()

# --- SCREEN 3: RESULTS (EYE-CATCHING DASHBOARD) ---
elif st.session_state.screen == 'results':
    st.title("📊 Analysis Report")
    st.write("---")
    
    # Dual Display (Fixes your 2nd problem)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### **MI Risk**")
        st.metric(label="Myocardial Infarction", value=f"{st.session_state.mi_res}%")
        st.progress(st.session_state.mi_res / 100)
        
    with col2:
        st.markdown("### **Angina Risk**")
        st.metric(label="Angina Pectoris", value=f"{st.session_state.angina_res}%")
        st.progress(st.session_state.angina_res / 100)

    st.write("---")
    
    # Interpretation
    if st.session_state.mi_res > st.session_state.angina_res and st.session_state.mi_res > 50:
        st.error("🚨 **CLINICAL ALERT**: High probability of Myocardial Infarction. Urgent ECG and cardiac consult recommended.")
    elif st.session_state.angina_res > 40:
        st.warning("⚠️ **ISCHEMIA DETECTED**: Risk profile is more consistent with Stable/Unstable Angina. Lipid management advised.")
    else:
        st.success("✅ **STABLE PROFILE**: Low risk detected for acute coronary events.")

    if st.button("← Back to Home"):
        st.session_state.screen = 'welcome'
        st.rerun()
