import pandas as pd
import streamlit as st
import plotly.express as px
#Day-11
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
import numpy as np

st.title("University Risk Analytics Dashboard")

#load Data
df=pd.read_csv('data/sample.csv')
st.subheader('Data Preview:')
st.dataframe(df)

#Summary Metrics & Pass/Fail Chart
st.subheader('Summary Metrics')

#Total Students
total_students=df.shape[0]

#Count Passed/Fail
passed=df[df['Pass/Fail']=='Pass'].shape[0]
failed=df[df['Pass/Fail']=='Fail'].shape[0]

st.write(f"Total Students: {total_students}")
st.write(f"Passed : {passed}")
st.write(f"Failed: {failed}")

#Bar Chart for Pass/Fail
st.subheader("Pass/Fail Distribution")
st.bar_chart(df['Pass/Fail'].value_counts())

#Day-3
#Filtering
# Example: filter by score
score_threshold = st.slider("Minimum Score", min_value=int(df['Scores'].min()), max_value=int(df['Scores'].max()), value=int(df['Scores'].min()))
filtered_df = df[df['Scores'] >= score_threshold]

st.subheader(f"Students with Score ≥ {score_threshold}")
st.dataframe(filtered_df)

#Histogram



#Day-4:We already have histogram and filtering.
#Pie chart for Pass/Fail
#Dynamic pie chart for Pass/Fail based on filtered data

st.subheader("Pass/Fail Distribution (Filtering)")
fig=px.pie(filtered_df,names='Pass/Fail',title='Pass/Fail Percentage')
st.plotly_chart(fig)

#Average Score Metric
st.subheader("Key Stats (Filtered)")
avg_score=filtered_df['Scores'].mean()
st.write(f"Average Score: {avg_score:.2f}")

#Day-5 Risk Category
risk_threshold = st.number_input(
    "High Risk Threshold",
    min_value=0,
    max_value=100,
    value=45,
    step=1
)
#Day-6
#Add Attendance Threshold
attendance_threshold=st.number_input(
    "Low Attendance Threshold %",
    min_value=0,
    max_value=100,
    value=65,
    step=1
)
#Day-5&6
# 2️⃣ Upgrade Risk Logic (replace function only)

def risk_category(score, attendance, score_th, att_th):
    if score < score_th or attendance < att_th:
        return "High Risk"
    elif score < score_th + 15 or attendance < att_th + 10:
        return "Medium Risk"
    else:
        return "Low Risk"


df["Risk Level"] = df.apply(
    lambda x: risk_category(x["Scores"], x["Attendance"], risk_threshold, attendance_threshold),
    axis=1
)

filtered_df = df[df["Scores"] >= score_threshold]
fig2 = px.histogram(
    filtered_df,
    x="Scores",
    color="Risk Level",
    nbins=10,
    title="Score Distribution by Risk Level (Filtered)"
)
st.plotly_chart(fig2)


st.subheader("Risk Level Distribution")
risk_counts = filtered_df["Risk Level"].value_counts()

st.bar_chart(risk_counts)

st.subheader("Risk Summary")
st.write("High Risk Threshold:", risk_threshold)

high_risk_students = filtered_df[filtered_df["Risk Level"] == "High Risk"]
st.write(f"High Risk Students: {high_risk_students.shape[0]}")

# 4️⃣ Add Top-5 At-Risk Students Table

# Place after your risk summary:

st.subheader("Top 5 At-Risk Students (Filtered)")

top_risk = filtered_df[filtered_df["Risk Level"] == "High Risk"] \
    .sort_values(by=["Scores", "Attendance"]) \
    .head(5)

st.dataframe(top_risk)
#Day-7 due to exams I delayed it and now I am back 19-01-2026. Monday and Fix some errors Today of Histogram. 
st.subheader("Export High Risk Students")

export_df = filtered_df[filtered_df["Risk Level"] == "High Risk"]

csv = export_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download High Risk Students CSV",
    data=csv,
    file_name="high_risk_students.csv",
    mime="text/csv"
)

st.subheader("🚨 Critical Risk Alerts")

critical_df = filtered_df[
    (filtered_df["Scores"] < risk_threshold - 10) |
    (filtered_df["Attendance"] < attendance_threshold - 10)
]

if critical_df.shape[0] == 0:
    st.success("No critical-risk students right now 🎉")
else:
    st.error(f"{critical_df.shape[0]} students need immediate intervention!")
    st.dataframe(critical_df)


#Day-8
# let's do some visulization
# Filtered Data Table
st.subheader(f"Students with Score ≥ {score_threshold}")
st.dataframe(filtered_df)

# --- Step 1: Scatter Plot ---
st.subheader("Scores vs Attendance (Risk Level)")
fig_scatter = px.scatter(
    filtered_df,
    x="Attendance",
    y="Scores",
    color="Risk Level",
    hover_data=["StudentID", "Name"],
    size="Scores",
    title="Scores vs Attendance Colored by Risk Level"
)
st.plotly_chart(fig_scatter)

# --- Step 2: Box Plot ---
st.subheader("Score Distribution by Risk Level")
fig_box = px.box(
    filtered_df,
    x="Risk Level",
    y="Scores",
    color="Risk Level",
    points="all",
    title="Score Distribution per Risk Level"
)
st.plotly_chart(fig_box)

# --- Day-9 Step 1: Attendance Distribution by Risk Level ---

st.subheader("Attendance Distribution by Risk Level")

fig_att = px.histogram(
    filtered_df,
    x="Attendance",
    color="Risk Level",
    nbins=10,
    title="Attendance Distribution by Risk Level"
)

st.plotly_chart(fig_att)

#Step 2: Pass/Fail → Risk Level Sunburst ---

st.subheader("Pass / Fail → Risk Level Breakdown")

fig_sunburst = px.sunburst(
    filtered_df,
    path=["Pass/Fail", "Risk Level", "Name"],
    values="Scores",
    title="Student Risk Hierarchy"
)

st.plotly_chart(fig_sunburst)
# Step 3.1: Danger Score Calculation ---

df["Danger Score"] = (
    (risk_threshold - df["Scores"]).clip(lower=0) +
    (attendance_threshold - df["Attendance"]).clip(lower=0)
)
# Recreate filtered_df so it includes Danger Score
filtered_df = df[df["Scores"] >= score_threshold]

# Step 3.2: Priority Intervention List ---

st.subheader("🚨 Priority Intervention List (Most Critical Students)")

priority_df = filtered_df.sort_values(
    by="Danger Score",
    ascending=False
).head(10)

st.dataframe(priority_df)

#Day-10
st.subheader("Score & Attendance Trends by Risk Level")

fig_trend = px.line(
    filtered_df.sort_values(by="Scores"),  # sort to make trend line smooth
    x="StudentID",
    y=["Scores", "Attendance"],
    color="Risk Level",
    markers=True,
    title="Student Scores & Attendance Trends"
)

st.plotly_chart(fig_trend)


st.subheader("Early-Warning Projection")

future_risk_df = filtered_df.copy()
future_risk_df["Projected Scores"] = future_risk_df["Scores"] * 0.95  # assume 5% drop
future_risk_df["Projected Attendance"] = future_risk_df["Attendance"] * 0.95

# Recalculate projected danger score
future_risk_df["Projected Danger Score"] = (
    (risk_threshold - future_risk_df["Projected Scores"]).clip(lower=0) +
    (attendance_threshold - future_risk_df["Projected Attendance"]).clip(lower=0)
)

# Filter for students who will cross high-risk threshold
future_high_risk = future_risk_df[future_risk_df["Projected Danger Score"] > 10]

st.write(f"{future_high_risk.shape[0]} students may become high risk soon:")
st.dataframe(future_high_risk.sort_values(by="Projected Danger Score", ascending=False).head(10))


st.subheader("Machine Learning: Predict High-Risk Students")
# After creating High_Risk_Flag
# 1️⃣ Create target variables / ML columns first
df["High_Risk_Flag"] = np.where(df["Risk Level"] == "High Risk", 1, 0)

# 2️⃣ Predict with ML model
X = df[["Scores", "Attendance"]]
y = df["High_Risk_Flag"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)

df["Predicted_High_Risk"] = model.predict(df[["Scores", "Attendance"]])

# 3️⃣ Filter AFTER all new columns are added
filtered_df = df[df["Scores"] >= score_threshold]

# Create target variable: 1 if High Risk, 0 otherwise
df["High_Risk_Flag"] = np.where(df["Risk Level"] == "High Risk", 1, 0)

# Features
X = df[["Scores", "Attendance"]]
y = df["High_Risk_Flag"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LogisticRegression()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

st.write(f"Model Accuracy: {accuracy*100:.2f}%")

# 🔹 Step 3: Predict Risk for Filtered Students
# Predict risk for current filtered_df
filtered_df["Predicted_High_Risk"] = model.predict(filtered_df[["Scores", "Attendance"]])

st.subheader("Predicted High-Risk Students (ML Model)")
predicted_high_risk = filtered_df[filtered_df["Predicted_High_Risk"] == 1]
st.dataframe(predicted_high_risk.sort_values(by=["Scores", "Attendance"]).head(10))

#Step#4
st.subheader("Predicted vs Actual High-Risk Students")

fig_pred = px.scatter(
    filtered_df,
    x="Attendance",
    y="Scores",
    color="Predicted_High_Risk",
    symbol="High_Risk_Flag",
    hover_data=["Name", "StudentID"],
    title="Predicted vs Actual High-Risk Students"
)

st.plotly_chart(fig_pred)









