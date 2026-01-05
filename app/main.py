import pandas as pd
import streamlit as st
st.title("University Risk Analytics Dashboard")

#load Data
df=pd.read_csv('data/sample.csv')
st.subheader('Data Preview:')
st.dataframe(df)