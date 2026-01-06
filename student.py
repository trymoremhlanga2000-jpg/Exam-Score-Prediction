import streamlit as st
import numpy as np
import pandas as pd
import tensorflow as tf
import joblib
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Trymore's ExamScore AI Predictor", 
    page_icon="🎓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    div.stButton > button:first-child {
        background-color: #4CAF50; color: white; height: 3em; width: 100%; border-radius: 10px; border: none; font-size: 1.2rem;
    }
    .recommendation-card {
        padding: 20px; border-radius: 10px; background-color: #e8f4ea; border-left: 5px solid #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOAD ASSETS ---
@st.cache_resource
def load_assets():
    model = tf.keras.models.load_model('exam_model.h5')
    scaler = joblib.load('scaler.pkl')
    return model, scaler

try:
    model, scaler = load_assets()
except Exception as e:
    st.error(f"Error loading assets: {e}")

# --- MAPPINGS (Exact alphabetical order from LabelEncoder) ---
MAPPINGS = {
    'gender': {'female': 0, 'male': 1, 'other': 2},
    'course': {'b.com': 0, 'b.sc': 1, 'b.tech': 2, 'ba': 3, 'bba': 4, 'bca': 5, 'diploma': 6},
    'internet_access': {'no': 0, 'yes': 1},
    'study_method': {'coaching': 0, 'group study': 1, 'mixed': 2, 'online videos': 3, 'self-study': 4},
    'facility_rating': {'high': 0, 'low': 1, 'medium': 2},
    'exam_difficulty': {'easy': 0, 'hard': 1, 'moderate': 2},
    'sleep_quality': {'average': 0, 'good': 1, 'poor': 2}
}

# --- SIDEBAR INPUTS ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3413/3413535.png", width=100)
st.sidebar.title("Student Profile")
st.sidebar.markdown("Adjust parameters to predict the exam score.")

with st.sidebar:
    st.subheader("Personal & Academic")
    age = st.number_input("Age", 15, 30, 20)
    gender = st.selectbox("Gender", list(MAPPINGS['gender'].keys()))
    course = st.selectbox("Course Type", list(MAPPINGS['course'].keys()))
    
    st.subheader("Study Habits")
    study_hours = st.slider("Daily Study Hours", 0.0, 15.0, 5.0, help="Average hours spent studying per day")
    attendance = st.slider("Class Attendance (%)", 0, 100, 85)
    study_method = st.selectbox("Primary Study Method", list(MAPPINGS['study_method'].keys()))
    
    st.subheader("Environment & Health")
    internet = st.radio("Internet Access", ["yes", "no"], horizontal=True)
    sleep_hours = st.slider("Sleep Hours", 4.0, 12.0, 7.5)
    sleep_quality = st.select_slider("Sleep Quality", options=list(MAPPINGS['sleep_quality'].keys()), value='good')
    facility = st.select_slider("Facility Rating", options=list(MAPPINGS['facility_rating'].keys()), value='medium')
    difficulty = st.selectbox("Exam Difficulty", list(MAPPINGS['exam_difficulty'].keys()), index=2)

# --- PREDICTION LOGIC ---
def get_prediction():
    # Construct feature array in specific order:
    # age, gender, course, study_hours, class_attendance, internet_access, sleep_hours, sleep_quality, study_method, facility_rating, exam_difficulty
    input_data = np.array([[
        age, 
        MAPPINGS['gender'][gender],
        MAPPINGS['course'][course],
        study_hours,
        attendance,
        MAPPINGS['internet_access'][internet],
        sleep_hours,
        MAPPINGS['sleep_quality'][sleep_quality],
        MAPPINGS['study_method'][study_method],
        MAPPINGS['facility_rating'][facility],
        MAPPINGS['exam_difficulty'][difficulty]
    ]])
    
    # Scale and Predict
    scaled_data = scaler.transform(input_data)
    prediction = model.predict(scaled_data)[0][0]
    return max(0, min(100, prediction)) # Bound between 0-100

# --- MAIN DASHBOARD ---
st.title("🎓 ExamScore AI Predictor")
st.markdown("Predict student performance using Deep Learning based on 20,000+ student records.")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("Engineer: Trymore Mhlanga")
    st.write("Current Configuration Summary:")
    
    summary_df = pd.DataFrame({
        "Attribute": ["Study Hours", "Attendance", "Course", "Difficulty"],
        "Value": [f"{study_hours} hrs", f"{attendance}%", course.upper(), difficulty.capitalize()]
    })
    st.table(summary_df)
    
    if st.button("Generate Prediction"):
        score = get_prediction()
        st.session_state['score'] = score
    
with col2:
    if 'score' in st.session_state:
        score = st.session_state['score']
        
        # Plotly Gauge Chart
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = score,
            title = {'text': "Predicted Exam Score"},
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "#4CAF50"},
                'steps': [
                    {'range': [0, 40], 'color': "#ffcfcf"},
                    {'range': [40, 75], 'color': "#fdfdcf"},
                    {'range': [75, 100], 'color': "#cfdfcf"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig.update_layout(height=350, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig, use_container_width=True)

# --- RECOMMENDATIONS ---
if 'score' in st.session_state:
    st.divider()
    score = st.session_state['score']
    
    st.subheader("💡 Recommendations for Improvement")
    
    rec_col1, rec_col2 = st.columns(2)
    
    with rec_col1:
        if score < 60:
            st.warning("**Target Analysis**: Current prediction suggests you are below the average performance threshold.")
        else:
            st.success("**Target Analysis**: You are on track for a strong result!")
            
    with rec_col2:
        if study_hours < 4:
            st.info("📌 **Tip**: Increasing study time by just 1 hour daily could significantly boost your score.")
        if attendance < 75:
            st.error("📌 **Critical**: Attendance is low. Attending more classes is the fastest way to improve understanding.")
        if sleep_quality == 'poor':
            st.info("📌 **Health**: Better sleep quality is correlated with better memory retention.")

# --- FOOTER ---
st.divider()
st.caption("Developed By Trymore Mhlanga with Streamlit & TensorFlow | Data Source: Exam_Score_Prediction.csv")