import streamlit as st
import pandas as pd

# Load the data
df = pd.read_excel("Corrected_HeartRisk_Data.xlsx")

# Styling
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 25px; height: 3em; background-color: #d32f2f; color: white; }
    </style>
    """, unsafe_allow_html=True)

if 'screen' not in st.session_state:
    st.session_state.screen = 'welcome'
if 'data' not in st.session_state:
    st.session_state.data = {}

# --- SCREEN 1: WELCOME ---
if st.session_state.screen == 'welcome':
    st.image("https://cdn-icons-png.flaticon.com/512/833/833472.png", width=100)
    st.title("Heart Risk Predictor")
    st.write("### MI vs Angina Comparative Analysis")
    if st.button("Start Risk Assessment →"):
        st.session_state.screen = 'input_1'

# --- SCREEN 2: LIFESTYLE & HISTORY ---
elif st.session_state.screen == 'input_1':
    st.header("Step 1: Personal & History")
    st.session_state.data['age'] = st.selectbox("Age Group", df['Age Group'].dropna().unique())
    st.session_state.data['smoke'] = st.selectbox("Smoking Status", df['Smoking Status'].dropna().unique())
    st.session_state.data['hba1c'] = st.selectbox("Fasting Sugar / HbA1c", ["Normal", "Pre-Diabetic", "Diabetic"])
    st.session_state.data['ldl'] = st.selectbox("LDL Cholesterol Level", ["Normal", "Borderline High", "High"])
    
    if st.button("Next Step →"):
        st.session_state.screen = 'input_2'

# --- SCREEN 3: CLINICAL SYMPTOMS & BIOMARKERS ---
elif st.session_state.screen == 'input_2':
    st.header("Step 2: Clinical Details")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.data['radiation'] = st.selectbox("Pain Radiation", ["None", "Left Arm", "Jaw", "Back"])
        st.session_state.data['relief'] = st.selectbox("Pain Relief", ["Relieved by rest", "Not relieved by rest"])
    with col2:
        st.session_state.data['nitro'] = st.radio("Relieved by Nitroglycerin?", ["Yes", "No"])
        st.session_state.data['troponin'] = st.selectbox("Troponin Level", df['Cardiac Troponin Level'].dropna().unique())

    if st.button("Calculate Final Analysis →"):
        # CALCULATE SCORES
        mi = 10
        angina = 15
        
        # Logic for MI
        if "Positive" in st.session_state.data['troponin']: mi += 40
        if st.session_state.data['radiation'] == "Left Arm": mi += 20
        if st.session_state.data['relief'] == "Not relieved by rest": mi += 15
        
        # Logic for Angina
        if st.session_state.data['nitro'] == "Yes": angina += 30
        if st.session_state.data['relief'] == "Relieved by rest": angina += 20
        if "Borderline" in st.session_state.data['ldl']: angina += 10

        st.session_state.mi_res = min(mi, 95)
        st.session_state.angina_res = min(angina, 95)
        st.session_state.screen = 'results'

# --- SCREEN 4: RESULTS ---
elif st.session_state.screen == 'results':
    st.header("Comparative Risk Analysis")
    st.metric("MI (Heart Attack) Risk", f"{st.session_state.mi_res}%")
    st.metric("Angina Risk", f"{st.session_state.angina_res}%")
    
    if st.session_state.mi_res > st.session_state.angina_res:
        st.error("Higher correlation with Acute Myocardial Infarction.")
    else:
        st.warning("Higher correlation with Angina Pectoris.")
        
    if st.button("New Assessment"):
        st.session_state.screen = 'welcome'
