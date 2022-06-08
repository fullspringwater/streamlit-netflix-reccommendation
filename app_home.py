import streamlit as st
import pandas as pd


from avg_vs_choice_chart import avg__vs_choice_chart
from movie_info import movie_info
from videosSearch import videosSearch
from recomemended_movies import recommended_movie

def run_home() :
    df= pd.read_csv('data/new_data.csv', index_col=0)
    df = df.drop_duplicates(['title'], keep = 'first')
     
    genres = ['Anything','Reality','European','Music','Family','Animation',
        'Comedy','Romance','Action','Thriller','Horror','Scifi',
        'History','Western','Crime','Documentation','Drama',
        'Sport','Fantasy','War']
    
    # Search
    col01, col02 = st.columns(2)
    with col01 :
        search = st.text_input('제목 검색')
        genre_choice = st.selectbox('장르 선택', genres)
    with col02 :
        type_choice = st.radio('타입 선택',
        ['Anything', 'Movie', 'Show'])
        print(type_choice)
    
    if genre_choice == 'Anything' and type_choice == 'Anything':
        search_result = df.loc[df['title'].str.lower().str.contains(search.lower(), na=False)]
        search_list = search_result['title'].values

    elif genre_choice == 'Anything' and type_choice != 'Anything':
        search_result = df.loc[df['title'].str.lower().str.contains(search.lower(), na=False) &
                            df['type'].str.contains(type_choice.upper())]
        search_list = search_result['title'].values

    elif genre_choice != 'Anything' and type_choice == 'Anything':
        search_result = df.loc[df['title'].str.lower().str.contains(search.lower(), na=False) &
                            df['genres'].str.contains(genre_choice.lower())]
        search_list = search_result['title'].values
    else :
        search_result = df.loc[df['title'].str.lower().str.contains(search.lower(), na=False) &
                            df['genres'].str.contains(genre_choice.lower())&
                            df['type'].str.contains(type_choice.upper())]
        search_list = search_result['title'].values


    # search_list 가 비어있지 않을때 
    if len(search_list) != 0:
        selected = st.selectbox('검색 결과 리스트', search_list)
        st.markdown("---")
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #9EE681;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">{}</p>'.format(selected), unsafe_allow_html=True)
    
        # 동영상 출력
        col_video1, _ = st.columns(2)
        with col_video1 :
            videosSearch(selected)
        
        col1, col2 = st.columns([5,3])
        # 정보들 출력
        movie_info(col1, col2, df, selected)

        avg__vs_choice_chart(df, selected)
        st.markdown('---')

        # 추천프로그램 데이터 프레임 가져오기
        recommended_movies = recommended_movie(selected)
        recommend_list = recommended_movies['Title'].values
        recommend_choice = st.selectbox('추천 리스트', recommend_list)

        # 버튼을 누를 때
        if st.button('선택한 프로그램 정보', key = 1) :
            
            # 추천 프로그램 정보 출력
            st.markdown(""" <style> .font {
            font-size:35px ; font-family: 'Cooper Black'; color: #9EE681;} 
            </style> """, unsafe_allow_html=True)
            st.markdown('<p class="font">{}</p>'.format(recommend_choice), unsafe_allow_html=True)


            # 동영상 출력
            col_video2, _ = st.columns(2)
            with col_video2 :
                videosSearch(recommend_choice)
                                    
            col3, col4 = st.columns([5,3])

            # 정보들 출력
            with col3 :
                st.subheader('유사도')
                similarity = recommended_movies.loc[recommended_movies['Title'] == recommend_choice,
                                                'Similarity'].values[0] * 100
                st.text('{}%'.format(round(similarity,2)))
            movie_info(col3, col4, df, recommend_choice)

            # 차트 출력
            avg__vs_choice_chart(df, recommend_choice)
    else :
        st.warning('검색결과가 없습니다. 다시 검색해주세요')





        


