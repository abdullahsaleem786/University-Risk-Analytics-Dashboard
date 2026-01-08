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
fig2=px.histogram(df,x='Scores',nbins=10,title='Score Distribution')
st.plotly_chart(fig2)

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

def risk_category(score, threshold):
    if score < threshold:
        return "High Risk"
    elif score < threshold + 20:
        return "Medium Risk"
    else:
        return "Low Risk"

df["Risk Level"] = df["Scores"].apply(lambda x: risk_category(x, risk_threshold))
filtered_df = df[df["Scores"] >= score_threshold]



st.subheader("Risk Level Distribution")
risk_counts = filtered_df["Risk Level"].value_counts()

st.bar_chart(risk_counts)

st.subheader("Risk Summary")
st.write("High Risk Threshold:", risk_threshold)

high_risk_students = filtered_df[filtered_df["Risk Level"] == "High Risk"]
st.write(f"High Risk Students: {high_risk_students.shape[0]}")

#High risk students
st.subheader("High Risk Students")
high_risk_std=filtered_df[filtered_df['Risk Level']=='High Risk']
st.dataframe(high_risk_std)

#High Risk KPI
high_risk_counts=high_risk_std.shape[0]
st.write(f"High Risk Students: {high_risk_counts}")