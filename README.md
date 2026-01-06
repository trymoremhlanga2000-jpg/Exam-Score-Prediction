# 🎓 ExamScore AI Predictor: Streamlit Application

An end-to-end deep learning web application that predicts student exam scores based on academic behavior, study habits, and environmental factors. Built with TensorFlow and deployed using Streamlit, this project demonstrates applied machine learning, model deployment, and interactive dashboard design.

---

## 🚀 Live Application
>[Trymore's Model Application](https://exam-score-prediction-trymoremlangaaa.streamlit.app/)
---

## 📌 Project Overview

The **ExamScore AI Predictor** leverages a trained neural network model to estimate a student's expected exam score (0–100) using structured input data such as study hours, attendance, sleep quality, internet access, and exam difficulty.

The application provides:
- Real-time predictions
- Visual performance indicators
- Personalized recommendations for improvement
- A professional, user-friendly dashboard interface

This project is designed for educational analytics, machine learning deployment and portfolio demonstration purposes.

---

## 🧠 Machine Learning Model

- **Model Type:** Deep Neural Network (TensorFlow / Keras)
- **Target Variable:** Exam Score (0–100)
- **Features Include:**
  - Age
  - Gender
  - Course Type
  - Study Hours
  - Attendance Percentage
  - Study Method
  - Internet Access
  - Sleep Hours & Sleep Quality
  - Facility Rating
  - Exam Difficulty

- **Preprocessing:**
  - Categorical encoding using LabelEncoder mappings
  - Feature scaling using a saved Scikit-learn scaler
- **Training Dataset:** 20,000+ student records

---

## 📊 Application Features

- 🎯 **Real-Time Prediction**  
  Instantly predicts exam scores based on user inputs.

- 📈 **Interactive Gauge Visualization**  
  Displays predicted scores using a Plotly gauge chart.

- 💡 **Smart Recommendations**  
  Actionable insights based on predicted performance and input patterns.

- 🖥️ **Professional Dashboard UI**  
  Custom CSS styling and responsive Streamlit layout.

- ⚡ **Optimized Performance**  
  Cached model and scaler loading for fast inference.

---

## 🛠️ Tech Stack

| Category | Tools |
|-------|------|
| Frontend | Streamlit |
| Machine Learning | TensorFlow (Keras) |
| Data Processing | NumPy, Pandas |
| Model Persistence | Joblib |
| Visualization | Plotly |
| Deployment | Streamlit Cloud |

---

## 📂 Project Structure

```text
exam-score-ai-predictor-streamlit/
│
├── app.py                  # Main Streamlit application
├── exam_model.h5           # Trained TensorFlow model
├── scaler.pkl              # Fitted feature scaler
├── requirements.txt        # Project dependencies
├── README.md               # Project documentation
└── assets/                 # (Optional) images/icons



BY TRYMORE MHLANGA