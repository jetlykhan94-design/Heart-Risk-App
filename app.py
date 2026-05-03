import streamlit as st
import pandas as pd

# Load the data for reference values
df = pd.read_excel("Corrected_HeartRisk_Data.xlsx")

# --- CUSTOM CSS FOR THE SKETCH LOOK ---
st.markdown("""
    <style>
    .stApp { background-color: #f8faff; }
    .main-card { background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #c62828; color: white; font-weight: bold; }
    .metric-card { background: white; padding: 15px; border-radius: 10px; border: 1px solid #eee; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

if 'screen' not in st.session_state:
    st.session_state.screen = 'welcome'
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

# --- SCREEN 1: WELCOME ---
if st.session_state.screen == 'welcome':
    st.image("https://cdn-icons-png.flaticon.com/512/833/833472.png", width=100)
    st.title("Heart Risk Predictor")
    st.write("### MI vs Angina Comparative Analysis")
    st.write("Assess your risk of Myocardial Infarction (MI) and Angina based on your health profile.")
    if st.button("Start Risk Assessment →"):
        st.session_state.screen = 'input_1'

# --- SCREEN 2: PERSONAL & LIFESTYLE ---
elif st.session_state.screen == 'input_1':
    st.header("1. Personal & Lifestyle")
    with st.container():
        st.session_state.user_data['age'] = st.selectbox("Age Group", df['Age Group'].unique())
        st.session_state.user_data['gender'] = st.radio("Biological Gender", ["Male", "Female"])
        st.session_state.user_data['smoking'] = st.selectbox("Smoking Status", df['Smoking Status'].unique())
        st.session_state.user_data['activity'] = st.selectbox("Physical Activity Level", df['Physical Activity Level'].unique())
        
        if st.button("Next Step →"):
            st.session_state.screen = 'input_2'

# --- SCREEN 3: MEDICAL & SYMPTOMS ---
elif st.session_state.screen == 'input_2':
    st.header("2. Medical & Symptoms")
    st.session_state.user_data['hyper'] = st.toggle("History of Hypertension")
    st.session_state.user_data['diab'] = st.toggle("Diabetes Mellitus")
    st.session_state.user_data['fam'] = st.toggle("Family History of Heart Disease")
    
    st.divider()
    st.session_state.user_data['pain'] = st.selectbox("Character of Chest Pain", df['Character of Chest Pain'].unique())
    st.session_state.user_data['symptoms'] = st.multiselect("Associated Symptoms", df['Associated Symptoms'].unique())
    
    if st.button("Calculate Risk →"):
        # SIMPLE SCORING LOGIC
        mi_score = 10 # Base score
        angina_score = 15 # Base score
        
        # Add points based on inputs (Matching your project logic)
        if st.session_state.user_data['hyper']: mi_score += 20; angina_score += 10
        if st.session_state.user_data['diab']: mi_score += 20; angina_score += 5
        if "Crushing" in st.session_state.user_data['pain']: mi_score += 30
        if "Pressure" in st.session_state.user_data['pain']: angina_score += 25
        
        st.session_state.mi_final = min(mi_score, 99)
        st.session_state.angina_final = min(angina_score, 99)
        st.session_state.screen = 'results'

# --- SCREEN 4: RESULTS ---
elif st.session_state.screen == 'results':
    st.header("Your Results")
    
    col1, col2 = st.columns(2)
    with col1:
        color = "red" if st.session_state.mi_final > 50 else "orange"
        st.markdown(f"<div class='metric-card'><h4>MI Risk</h4><h2 style='color:{color}'>{st.session_state.mi_final}%</h2></div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"<div class='metric-card'><h4>Angina Risk</h4><h2 style='color:blue'>{st.session_state.angina_final}%</h2></div>", unsafe_allow_html=True)

    st.write("### Interpretation")
    if st.session_state.mi_final > st.session_state.angina_final:
        st.error("Your profile indicates a higher correlation with Myocardial Infarction (MI). Seek medical advice.")
    else:
        st.warning("Your profile indicates a higher correlation with Stable/Unstable Angina symptoms.")
    
    if st.button("Restart"):
        st.session_state.screen = 'welcome'
