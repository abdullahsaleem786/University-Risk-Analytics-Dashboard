import pandas as pd
import streamlit as st
import plotly.express as px
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
#Scatter plot
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






