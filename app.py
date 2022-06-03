import streamlit as st
from streamlit_option_menu import option_menu

from app_home import run_home

def main() :
    st.set_page_config(layout="wide")
    st.title('Netflix 검색 및 추천')
    run_home() 
    print(st.__version__)

if __name__=='__main__' :
    main()