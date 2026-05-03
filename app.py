import streamlit as st
import pandas as pd

# Load the data
df = pd.read_excel("Corrected_HeartRisk_Data.xlsx")

# App Styling
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #d32f2f; color: white; }
    </style>
    """, unsafe_allow_html=True)

if 'screen' not in st.session_state:
    st.session_state.screen = 'welcome'

# --- SCREEN 1: WELCOME ---
if st.session_state.screen == 'welcome':
    st.image("https://cdn-icons-png.flaticon.com/512/833/833472.png", width=120)
    st.title("Heart Risk Predictor")
    st.write("### MI vs Angina Comparative Analysis")
    st.info("Assess your risk of Myocardial Infarction (MI) and Angina based on your health profile.")
    if st.button("Start Risk Assessment →"):
        st.session_state.screen = 'input_1'

# --- SCREEN 2: INPUTS ---
elif st.session_state.screen == 'input_1':
    st.header("Risk Assessment")
    age = st.selectbox("Age Group", df['Age Group'].unique())
    gender = st.radio("Biological Gender", df['Biological Gender'].unique())
    bmi = st.selectbox("BMI Category", df['Body Mass Index (BMI) Category'].unique())
    
    st.divider()
    st.subheader("Medical History")
    hyper = st.toggle("Hypertension History")
    diab = st.toggle("Diabetes Mellitus")
    
    if st.button("Next →"):
        st.session_state.screen = 'results'

# --- SCREEN 3: RESULTS ---
elif st.session_state.screen == 'results':
    st.header("Your Comparative Risk Results")
    col1, col2 = st.columns(2)
    
    # Using sample result logic based on your Sketch
    col1.metric("MI (Heart Attack) Risk", "72%", "High Risk", delta_color="inverse")
    col2.metric("Angina Risk", "45%", "Moderate Risk", delta_color="normal")
    
    st.write("### Interpretation")
    st.warning("Your symptom profile and risk factors are more aligned with Myocardial Infarction (MI) risk. Please consult a cardiologist.")
    
    if st.button("Restart Assessment"):
        st.session_state.screen = 'welcome'
