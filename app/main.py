import pandas as pd
import streamlit as st
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


