import streamlit as st
from app_home import run_home
from PIL import Image
def main() :
    logo = Image.open('data/logo.jpg')

    st.set_page_config(page_title="Netflix Recommendation",
        page_icon=logo,
        layout="wide")
    
    col1, col2 = st.columns([5,9])
    with col1 :
        st.title('Netflix 검색 및 추천')
    with col2 :
        st.image(logo, width=130 )
    
    run_home() 


if __name__=='__main__' :
    main()