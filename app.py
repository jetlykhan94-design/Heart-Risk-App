import streamlit as st
import pandas as pd

# 1. INITIALIZE ALL DATA (Prevents AttributeErrors)
if 'screen' not in st.session_state:
    st.session_state.screen = 'welcome'
if 'patient_data' not in st.session_state:
    st.session_state.patient_data = {}
if 'mi_res' not in st.session_state:
    st.session_state.mi_res = 0
if 'angina_res' not in st.session_state:
    st.session_state.angina_res = 0

# 2. UI CONFIG & THEME
st.set_page_config(page_title="HeartRisk Pro", page_icon="🏥", layout="wide")

st.markdown("""
    <style>
    /* Global Styles */
    .stApp { background-color: transparent; }
    .main-title { color: #d32f2f; font-size: 45px; font-weight: bold; text-align: center; margin-bottom: 0px; }
    .sub-title { text-align: center; color: #555; margin-bottom: 30px; }
    
    /* Box Styling */
    .metric-box {
        background-color: rgba(211, 47, 47, 0.1);
        padding: 25px; border-radius: 15px; border-left: 5px solid #d32f2f;
        text-align: center; margin-bottom: 10px;
    }
    
    /* Button Styling */
    .stButton>button {
        width: 100%; border-radius: 30px; height: 3.5em;
        background-color: #d32f2f !important; color: white !important;
        font-weight: bold; border: none; font-size: 18px; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); }
    </style>
    """, unsafe_allow_html=True)

# --- SCREEN 1: WELCOME ---
if st.session_state.screen == 'welcome':
    st.markdown('<p class="main-title">❤️ Heart Risk Predictor</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Advanced MI vs Angina Differential Analysis Tool</p>', unsafe_allow_html=True)
    
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        st.image("https://cdn-icons-png.flaticon.com/512/833/833472.png", width=150)
        st.info("💡 **Exhibition Notice**: This tool evaluates myocardial injury risk vs coronary artery ischemia based on the Pharm-D research dataset.")
        if st.button("🚀 Start Clinical Evaluation"):
            st.session_state.screen = 'assessment'
            st.rerun()

# --- SCREEN 2: ALL QUESTIONS (PHARM-D GRADE) ---
elif st.session_state.screen == 'assessment':
    st.markdown("## 📋 Comprehensive Patient Assessment")
    
    with st.form("main_form"):
        # ROW 1: Demographics
        st.subheader("👤 1. Personal & Lifestyle Profile")
        c1, c2, c3 = st.columns(3)
        age = c1.selectbox("Age Group", ["Under 30", "30-39", "40-49", "50-59", "60-69", "70+"])
        gender = c2.selectbox("Biological Gender", ["Male", "Female"])
        bmi = c3.selectbox("BMI Category", ["Underweight", "Normal weight", "Overweight", "Obese"])
        
        c4, c5, c6 = st.columns(3)
        smoke = c4.selectbox("Smoking Status", ["Never", "Current", "Passive"])
        activity = c5.selectbox("Activity Level", ["Sedentary", "Active", "Highly Active"])
        loc = c6.selectbox("Location", ["Urban", "Rural"])

        st.divider()
        
        # ROW 2: Medical & History
        st.subheader("🏥 2. Clinical History & Vitals")
        c7, c8, c9 = st.columns(3)
        h_bp = c7.checkbox("Hypertension History")
        h_dm = c8.checkbox("Diabetes Mellitus")
        h_fh = c9.checkbox("Family History (IHD)")
        
        c10, c11, c12 = st.columns(3)
        bp_val = c10.selectbox("Blood Pressure Status", ["Normal", "High (Stage 1)", "High (Stage 2)", "Crisis"])
        sugar_val = c11.selectbox("Blood Sugar Level", ["Normal", "Borderline", "Diabetic"])
        lipid_val = c12.selectbox("Lipid Profile", ["Normal", "Borderline High", "High"])

        st.divider()

        # ROW 3: Symptoms & Advanced Labs
        st.subheader("🧪 3. Acute Symptoms & Lab Markers")
        c13, c14 = st.columns(2)
        pain = c13.selectbox("Chest Pain Character", ["None", "Sharp / Stabbing", "Pressure / Heaviness", "Crushing / Squeezing", "Burning"])
        radiate = c14.selectbox("Pain Radiation", ["None", "Left Arm", "Jaw / Neck", "Back"])
        
        c15, c16, c17 = st.columns(3)
        trop = c15.selectbox("Tro
