import streamlit as st
import pandas as pd
import joblib
from youtubesearchpython import VideosSearch
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity

def run_home() :
    df= pd.read_csv('data/new_data.csv', index_col=0)
    df = df.drop_duplicates(['title'], keep = 'first')

    # st.dataframe(df)
    X = pd.read_csv('data/X.csv', index_col=0)
    y = pd.read_csv('data/y.csv', index_col=0)
    kn = joblib.load('data/kn.pkl')
    search = st.text_input('제목 검색')
    search_result = df.loc[df['title'].str.lower().str.contains(search, na=False)]
    search_list = search_result['title'].values


    if len(search_list) != 0 :
        selected = st.selectbox('검색 결과 리스트', search_list)
        st.markdown("---")
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #9EE681;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">{}</p>'.format(selected), unsafe_allow_html=True)
    
        
        # Youtube 동영상 검색후 영상 url 가져오기
        videosSearch = VideosSearch('Netflix {}'.format(selected), 
                                    limit = 2)
        video_url = videosSearch.result()['result'][0]['link']

        # 동영상 출력
        col_video1, _ = st.columns(2)
        with col_video1 :
            st.video(video_url)
        
        col1, col2 = st.columns([5,3])
        # 정보들 출력

        with col1 :
            st.subheader('나이 제한')
            st.write(df.loc[df['title'] == selected,'age_certification'].values[0])
            
            st.subheader('장르')
            genre_list = df.loc[df['title'] == selected,
                            'genres'].values[0]
            genre_list = genre_list.replace('[','').replace(']','').replace('\'','')
            st.text(genre_list)

            st.subheader('제작국가')
            country_list = df.loc[df['title'] == selected,
                                'production_countries'].values[0]
            country_list = country_list.replace('[','').replace(']','').replace('\'','')
            st.write(country_list)

            st.subheader('줄거리')
            st.write(df.loc[df['title'] == selected,'description'].values[0])
        with col2 :
            st.subheader('출시년도')
            st.text('{}년'.format(df.loc[df['title'] == selected,'release_year'].values[0]))

            st.subheader('러닝 타임')
            st.text('{}분'.format(df.loc[df['title'] == selected,'runtime'].values[0]))

            

            st.subheader('IMDB 점수')
            st.text(df.loc[df['title'] == selected,'imdb_score'].values[0])
            st.subheader('TMDB 인기도')
            st.text(df.loc[df['title'] == selected,'tmdb_popularity'].values[0])
            st.subheader('TMDB 점수')
            st.text(df.loc[df['title'] == selected,'tmdb_score'].values[0])

        st.markdown('---')

        # 추천시스템
        distances, indices = kn.kneighbors(np.array(X.loc[selected]).reshape(1,144))
        nearest_title = [y.loc[i][0] for i in indices.flatten()][1:]
        sim_rates = []
        # summary = []

        for nt in nearest_title :
            # summary.append(df.loc[df['title'] == nt]['description'].values[0])
            sim = cosine_similarity(np.array(X.loc[selected]).reshape(1,144),
                                    np.array(X.loc[nt]).reshape(1,144)).flatten()
            sim_rates.append(sim[0])
        
        recommended_movie = pd.DataFrame({
                                'Title' : nearest_title,                                 
                                'Similarity' : sim_rates} )
        recommended_movie.sort_values('Similarity', ascending =False)

        # st.dataframe(recommended_movie)
        recommend_list = recommended_movie['Title'].values
        recommend_choice = st.selectbox('추천 리스트', recommend_list)
        if st.button('선택한 프로그램 정보') :
            
            st.markdown(""" <style> .font {
            font-size:35px ; font-family: 'Cooper Black'; color: #9EE681;} 
            </style> """, unsafe_allow_html=True)
            st.markdown('<p class="font">{}</p>'.format(recommend_choice), unsafe_allow_html=True)

            # Youtube 동영상 검색후 영상 url 가져오기
            rec_videosSearch = VideosSearch('Netflix {}'.format(recommend_choice), 
                                        limit = 2)
            rec_video_url = rec_videosSearch.result()['result'][0]['link']

            # 동영상 출력
            col_video2, _ = st.columns(2)
            with col_video2 :
                st.video(rec_video_url)
        
            

            
            
            col3, col4 = st.columns([5,3])

            with col3 :
                st.subheader('유사도')
                similarity = recommended_movie.loc[recommended_movie['Title'] == recommend_choice,
                                                'Similarity'].values[0] * 100
                st.text('{}%'.format(round(similarity,2)))

                st.subheader('나이 제한')
                st.write(df.loc[df['title'] == recommend_choice,'age_certification'].values[0])
                    
                st.subheader('장르')
                genre_list = df.loc[df['title'] == recommend_choice,
                                'genres'].values[0]
                genre_list = genre_list.replace('[','').replace(']','').replace('\'','')
                st.text(genre_list)

                st.subheader('제작국가')
                country_list = df.loc[df['title'] == recommend_choice,
                                        'production_countries'].values[0]
                country_list = country_list.replace('[','').replace(']','').replace('\'','')
                st.write(country_list)

                st.subheader('줄거리')
                st.write(df.loc[df['title'] == recommend_choice,'description'].values[0])
            with col4 :
                st.subheader('출시년도')
                st.text('{}년'.format(df.loc[df['title'] == recommend_choice,'release_year'].values[0]))

                st.subheader('러닝 타임')
                st.text('{}분'.format(df.loc[df['title'] == recommend_choice,'runtime'].values[0]))

                    

                st.subheader('IMDB 점수')
                st.text(df.loc[df['title'] == recommend_choice,'imdb_score'].values[0])
                st.subheader('TMDB 인기도')
                st.text(df.loc[df['title'] == recommend_choice,'tmdb_popularity'].values[0])
                st.subheader('TMDB 점수')
                st.text(df.loc[df['title'] == recommend_choice,'tmdb_score'].values[0])






        


