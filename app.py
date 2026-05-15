import streamlit as st
import pandas as pd

# 1. SESSION STATE INITIALIZATION (Prevents All AttributeErrors)
if 'screen' not in st.session_state:
    st.session_state.screen = 'welcome'
if 'patient_data' not in st.session_state:
    st.session_state.patient_data = {}
if 'mi_res' not in st.session_state:
    st.session_state.mi_res = 0
if 'angina_res' not in st.session_state:
    st.session_state.angina_res = 0

# 2. THEME & UI STYLING
st.set_page_config(page_title="HeartRisk Pro Dashboard", page_icon="❤️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: transparent; }
    .metric-card {
        background-color: rgba(211, 47, 47, 0.08);
        padding: 30px; border-radius: 20px;
        border: 2px solid #d32f2f; text-align: center;
    }
    .stButton>button {
        width: 100%; border-radius: 25px; height: 3.5em;
        background-color: #d32f2f !important; color: white !important;
        font-weight: bold; border: none; font-size: 18px;
    }
    /* Ensure table text is visible in all themes */
    .stTable { background-color: transparent; }
    </style>
    """, unsafe_allow_html=True)

# --- SCREEN 1: WELCOME ---
if st.session_state.screen == 'welcome':
    st.markdown("<h1 style='text-align: center; color: #d32f2f;'>❤️ Heart Risk Predictor</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>MI vs Angina Differential Diagnosis Support</h4>", unsafe_allow_html=True)
    
    _, col_btn, _ = st.columns([1, 2, 1])
    with col_btn:
        st.image("https://cdn-icons-png.flaticon.com/512/833/833472.png", width=150)
        st.write("")
        if st.button("🚀 Start Clinical Assessment"):
            st.session_state.screen = 'assessment'
            st.rerun()

# --- SCREEN 2: ALL CLINICAL QUESTIONS ---
elif st.session_state.screen == 'assessment':
    st.header("📋 Clinical Assessment Form")
    
    with st.form("clinical_form"):
        # Section 1: Demographics & Lifestyle
        st.subheader("1. Personal Profile")
        c1, c2, c3, c4 = st.columns(4)
        age = c1.selectbox("Age Group", ["Under 30", "30-39", "40-49", "50-59", "60+"])
        gender = c2.selectbox("Gender", ["Male", "Female"])
        bmi = c3.selectbox("BMI", ["Normal", "Overweight", "Obese"])
        smoke = c4.selectbox("Smoking", ["Never", "Current", "Passive"])

        # Section 2: Clinical History
        st.subheader("2. Medical History")
        c5, c6, c7, c8 = st.columns(4)
        h_bp = c5.checkbox("Hypertension")
        h_dm = c6.checkbox("Diabetes")
        h_fh = c7.checkbox("Family History")
        loc = c8.selectbox("Location", ["Urban", "Rural"])

        # Section 3: Vitals & Labs
        st.subheader("3. Vital Signs & Advanced Lab Markers")
        c9, c10, c11, c12 = st.columns(4)
        bp_val = c9.selectbox("Blood Pressure", ["Normal", "Stage 1", "Stage 2", "Crisis"])
        sugar = c10.selectbox("Glucose/HbA1c", ["Normal", "Borderline", "Diabetic"])
        ldl = c11.selectbox("LDL Level", ["Desirable", "Borderline", "High"])
        trop = c12.selectbox("Troponin", ["Negative", "Mildly Elevated", "Highly Elevated"])

        # Section 4: Acute Symptoms
        st.subheader("4. Symptom Characteristics")
        c13, c14, c15 = st.columns(3)
        pain = c13.selectbox("Chest Pain Type", ["None", "Sharp", "Pressure", "Crushing"])
        radiate = c14.selectbox("Radiation", ["None", "Left Arm", "Jaw", "Back"])
        ecg = c15.selectbox("ECG Findings", ["Normal", "T-Wave Inversion", "ST-Elevation"])

        if st.form_submit_button("Generate Comparative Report"):
            # 1. SAVE HISTORY
            st.session_state.patient_data = {
                "Age": age, "Gender": gender, "BMI": bmi, "Smoking": smoke,
                "Hypertension": "Yes" if h_bp else "No", "Diabetes": "Yes" if h_dm else "No",
                "Troponin": trop, "ECG": ecg, "Pain Type": pain, "Radiation": radiate
            }
            
            # 2. CALCULATE LOGIC
            mi, ang = 10, 15
            if trop == "Highly Elevated" or ecg == "ST-Elevation": mi += 60
            if pain == "Crushing" or radiate == "Left Arm": mi += 20
            if pain == "Pressure" or ldl == "High": ang += 35
            
            st.session_state.mi_res = min(mi, 98)
            st.session_state.angina_res = min(ang, 95)
            st.session_state.screen = 'results'
            st.rerun()

# --- SCREEN 3: RESULTS & SAVED HISTORY ---
elif st.session_state.screen == 'results':
    st.title("📊 Clinical Report Summary")
    
    # DISPLAY SAVED HISTORY FIRST (As requested)
    with st.expander("📝 View Submitted Patient History", expanded=True):
        if st.session_state.patient_data:
            hist_df = pd.DataFrame(st.session_state.patient_data.items(), columns=["Clinical Parameter", "Entry"])
            st.table(hist_df)
        else:
            st.warning("No history data found.")

    st.divider()

    # DUAL RISK DISPLAY
    col_mi, col_ang = st.columns(2)
    
    with col_mi:
        st.markdown(f"""<div class="metric-card">
            <h2 style='color:#d32f2f;'>MI Risk</h2>
            <h1>{st.session_state.mi_res}%</h1>
            <p>Myocardial Infarction</p>
        </div>""", unsafe_allow_html=True)
        st.progress(st.session_state.mi_res / 100)
        
    with col_ang:
        st.markdown(f"""<div class="metric-card">
            <h2 style='color:#d32f2f;'>Angina Risk</h2>
            <h1>{st.session_state.angina_res}%</h1>
            <p>Angina Pectoris</p>
        </div>""", unsafe_allow_html=True)
        st.progress(st.session_state.angina_res / 100)

    st.write("---")
    
    # CLINICAL ADVISORY
    if st.session_state.mi_res > 60:
        st.error("🚨 **EMERGENCY**: Risk profile highly suggestive of Acute Myocardial Infarction.")
    elif st.session_state.angina_res > 40:
        st.warning("⚠️ **ISCHEMIA**: Results consistent with coronary artery disease (Angina).")
    else:
        st.success("✅ **STABLE**: Low risk for acute coronary events based on current markers.")

    if st.button("New Patient Assessment"):
        st.session_state.screen = 'welcome'
        st.rerun()
