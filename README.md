# 🎓 University Risk Analytics Dashboard

An end-to-end data analytics and decision-support system built with **Python, Streamlit, Plotly, and Machine Learning** to identify, analyze, and intervene in student academic risk.

---

## 🚀 Project Overview

This dashboard helps universities:
- Monitor student performance and attendance
- Identify high-risk students early
- Predict future academic risk using Machine Learning
- Recommend actionable interventions automatically

The system evolves step-by-step, simulating real-world analytics development over multiple days.

---

## 🧠 Key Features

### 📊 Data Analytics & Visualization
- Student performance summary (Pass/Fail, Scores, Attendance)
- Dynamic filtering by score thresholds
- Risk-level distribution and trend analysis
- Interactive charts (Scatter, Box, Histogram, Sunburst)

### ⚠️ Risk Scoring System
- Rule-based risk categorization (Low / Medium / High)
- Customizable score and attendance thresholds
- **Danger Score** to prioritize critical cases

### 🔮 Forecasting & Early Warning
- Projected score & attendance decline simulation
- Identification of students likely to become high-risk

### 🤖 Machine Learning
- Logistic Regression model to predict high-risk students
- Model evaluation with accuracy, confusion matrix, and metrics
- Comparison of predicted vs actual risk

### 🎯 Decision Automation (Final Stage)
- Automated intervention recommendations:
  - Academic counseling
  - Attendance warning
  - Immediate intervention
  - Monitoring or no action

---

## 🛠 Tech Stack

- **Python**
- **Pandas & NumPy**
- **Streamlit**
- **Plotly**
- **Scikit-learn**
- **Git & GitHub**

---

## 📈 Project Structure
University-Risk-Analytics-Dashboard/
│
├── app/
│ └── main.py
├── data/
│ └── sample.csv
├── README.md
└── requirements.txt


## ▶️ How to Run

```bash
pip install -r requirements.txt
streamlit run app/main.py```

🎯 Future Improvements

Database integration (PostgreSQL / SQLite)

User roles (Admin / Faculty)

Real-time data ingestion

Advanced ML models

