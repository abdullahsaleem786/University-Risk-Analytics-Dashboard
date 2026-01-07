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
