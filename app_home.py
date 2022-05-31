import streamlit as st
import pandas as pd
import joblib
def run_home() :
    df= pd.read_csv('data/new_data.csv', index_col=0)
    st.dataframe(df)
    X = pd.read_csv('data/X.csv', index_col=0)
    y = pd.read_csv('data/y.csv', index_col=0)
    kn = joblib.load('data/kn.pkl')
    search = st.text_input('제목 검색')
    search_result = df.loc[df['title'].str.lower().str.contains(search)]
    search_list = search_result['title'].values

    X.isna()
    if len(search_list) != 0 :
        selected = st.selectbox('검색 결과 리스트', search_list)