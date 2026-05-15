import streamlit as st
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Heart Risk Pro", page_icon="❤️", layout="centered")

# 2. ADVANCED UI CUSTOMIZATION
st.markdown("""
    <style>
    .main { background-color: transparent; }
    /* Metric styling */
    [data-testid="stMetricValue"] { font-size: 40px; color: #d32f2f; }
    /* Button styling */
    .stButton>button {
        width: 100%; border-radius: 15px; height: 3.5em;
        background-color: #d32f2f !important; color: white !important;
        font-weight: bold; border: none; font-size: 16px;
    }
    /* Section dividers */
    .section-head {
        color: #d32f2f; font-size: 20px; font-weight: bold;
        margin-top: 20px; border-bottom: 2px solid #d32f2f;
    }
    </style>
    """, unsafe_allow_html=True)

if 'screen' not in st.session_state:
    st.session_state.screen = 'welcome'

# --- SCREEN 1: WELCOME ---
if st.session_state.screen == 'welcome':
    st.image("https://cdn-icons-png.flaticon.com/512/833/833472.png", width=80)
    st.title("Heart Risk Predictor")
    st.write("#### Pharmaceutical Research Exhibition Tool")
    st.write("This app provides a comparative analysis between **Myocardial Infarction (MI)** and **Angina Pectoris** risk based on clinical markers.")
    if st.button("Start New Clinical Assessment →"):
        st.session_state.screen = 'assessment'

# --- SCREEN 2: ALL QUESTIONS (PERSONAL + CLINICAL + LAB) ---
elif st.session_state.screen == 'assessment':
    st.header("📋 Clinical Input Form")
    
    with st.form("full_assessment"):
        # PERSONAL PROFILE
        st.markdown('<p class="section-head">1. Personal & Lifestyle Profile</p>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            age = st.selectbox("Age Group", ["Under 30", "30-39", "40-49", "50-59", "60+"])
            gender = st.selectbox("Biological Gender", ["Male", "Female"])
            weight_status = st.selectbox("BMI Category", ["Normal weight", "Overweight", "Obese"])
        with c2:
            smoke = st.selectbox("Smoking Status", ["Never Smoked", "Current Smoker", "Passive Smoker"])
            activity = st.selectbox("Activity Level", ["Sedentary", "Moderately Active", "Very Active"])
            location = st.selectbox("Location", ["Urban", "Rural"])

        # CLINICAL HISTORY
        st.markdown('<p class="section-head">2. Medical History & Vitals</p>', unsafe_allow_html=True)
        c3, c4 = st.columns(2)
        with c3:
            h_bp = st.checkbox("History of Hypertension")
            h_dm = st.checkbox("History of Diabetes Mellitus")
            h_fh = st.checkbox("Family History of IHD")
        with c4:
            bp_val = st.selectbox("Current Blood Pressure", ["Normal", "Stage 1", "Stage 2", "Crisis"])
            sugar_val = st.selectbox("Glucose / HbA1c", ["Normal", "Pre-Diabetic", "Diabetic"])

        # SYMPTOMS & LABS
        st.markdown('<p class="section-head">3. Symptoms & Laboratory Markers</p>', unsafe_allow_html=True)
        pain = st.selectbox("Character of Chest Pain", ["None", "Sharp / Stabbing", "Pressure / Heaviness", "Crushing / Squeezing"])
        radiate = st.selectbox("Pain Radiation", ["None", "Left Arm", "Jaw / Neck", "Back"])
        trop = st.selectbox("Cardiac Troponin Level", ["Not Performed", "Negative", "Positive (Elevated)"])
        ldl = st.selectbox("LDL Cholesterol Level", ["Desirable", "Borderline", "High"])

        submit = st.form_submit_button("Generate Report")

        if submit:
            # SAVE HISTORY TO SESSION
            st.session_state.patient_data = {
                "Age": age, "Gender": gender, "BMI": weight_status, 
                "Smoking": smoke, "Hypertension": h_bp, "Diabetes": h_dm,
                "Pain": pain, "Radiation": radiate, "Troponin": trop
            }
            
            # CALCULATION LOGIC
            mi, ang = 10, 15
            if trop == "Positive (Elevated)": mi += 60
            if radiate == "Left Arm": mi += 15
            if h_bp or bp_val != "Normal": mi += 10; ang += 10
            if pain == "Pressure / Heaviness": ang += 30
            if pain == "Crushing / Squeezing": mi += 20
            
            st.session_state.mi_res = min(mi, 98)
            st.session_state.angina_res = min(ang, 95)
            st.session_state.screen = 'results'
            st.rerun()

# --- SCREEN 3: RESULTS + HISTORY SAVED ---
elif st.session_state.screen == 'results':
    st.title("📊 Clinical Analysis Report")
    
    # TABS FOR CLEAN UI
    tab1, tab2 = st.tabs(["🎯 Risk Analysis", "📝 Patient History"])
    
    with tab1:
        st.write("### Comparative Scoring")
        colA, colB = st.columns(2)
        colA.metric("MI Risk Score", f"{st.session_state.mi_res}%")
        colB.metric("Angina Risk Score", f"{st.session_state.angina_res}%")
        
        st.divider()
        if st.session_state.mi_res > 50:
            st.error("🚨 **High MI Risk:** Clinical markers suggest Myocardial Infarction.")
        elif st.session_state.angina_res > 40:
            st.warning("⚠️ **Angina Risk:** Symptoms consistent with Coronary Artery Disease.")
        else:
            st.success("✅ **Normal Profile:** No acute cardiac markers detected.")

    with tab2:
        st.write("### Recorded Clinical History")
        # Display the saved history in a neat table
        history_df = pd.DataFrame(st.session_state.patient_data.items(), columns=["Parameter", "Response"])
        st.table(history_df)

    st.divider()
    if st.button("Restart for New Patient"):
        st.session_state.screen = 'welcome'
        st.rerun()
