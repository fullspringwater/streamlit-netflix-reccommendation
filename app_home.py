import streamlit as st
import pandas as pd
import joblib
from youtubesearchpython import VideosSearch
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
import plotly.graph_objects as po
import plotly.graph_objs as go
# Youtube 동영상 검색후 영상 url 가져오기
def videosSearch(search):
    videosSearch = VideosSearch('Netflix {}'.format(search), 
                                    limit = 2)
    video_url = videosSearch.result()['result'][0]['link']

    return video_url

# 추천 시스템
def recommended_movie(title):
    X = pd.read_csv('data/X.csv', index_col=0)
    y = pd.read_csv('data/y.csv', index_col=0)
    kn = joblib.load('data/kn.pkl')

    _, indices = kn.kneighbors(np.array(X.loc[title]).reshape(1,144))
    nearest_title = [y.loc[i][0] for i in indices.flatten()][1:]
    sim_rates = []

    for nt in nearest_title :
        sim = cosine_similarity(np.array(X.loc[title]).reshape(1,144),
                                    np.array(X.loc[nt]).reshape(1,144)).flatten()
        sim_rates.append(sim[0])
        
    recommended_movies = pd.DataFrame({
                            'Title' : nearest_title,                                 
                            'Similarity' : sim_rates} )
    recommended_movies.sort_values('Similarity', ascending =False)

    return recommended_movies

# 프로그램 정보 출력
def movie_info(col1, col2, df, title) :
    with col1 :
        st.subheader('나이 제한')
        st.write(df.loc[df['title'] == title,'age_certification'].values[0])
            
        st.subheader('장르')
        genre_list = df.loc[df['title'] == title,
                            'genres'].values[0]
        genre_list = genre_list.replace('[','').replace(']','').replace('\'','')
        st.text(genre_list)

        st.subheader('제작국가')
        country_list = df.loc[df['title'] == title,
                            'production_countries'].values[0]
        country_list = country_list.replace('[','').replace(']','').replace('\'','')
        st.write(country_list)

        st.subheader('줄거리')
        st.write(df.loc[df['title'] == title,'description'].values[0])

    with col2 :
        st.subheader('출시년도')
        st.text('{}년'.format(df.loc[df['title'] == title,'release_year'].values[0]))

        st.subheader('러닝 타임')
        st.text('{}분'.format(df.loc[df['title'] == title,'runtime'].values[0]))

        

        st.subheader('IMDB 점수')
        st.text(df.loc[df['title'] == title,'imdb_score'].values[0])
        st.subheader('TMDB 인기도')
        st.text(df.loc[df['title'] == title,'tmdb_popularity'].values[0])
        st.subheader('TMDB 점수')
        st.text(df.loc[df['title'] == title,'tmdb_score'].values[0])

def avg_choice_chart(df, title) :
    imdb_scores = [round(df['imdb_score'].mean(),1), df.loc[df['title'] == title, 'imdb_score'].values[0] ]
    tmdb_popularity = [round(df['tmdb_popularity'].mean(),1), df.loc[df['title'] == title, 'tmdb_popularity'].values[0] ]
    tmdb_scores = [round(df['tmdb_score'].mean(),1), df.loc[df['title'] == title, 'tmdb_score'].values[0] ]
    runtimes = [round(df['runtime'].mean()), df.loc[df['title'] == title, 'runtime'].values[0] ]

    df_score_runtime = pd.DataFrame({'movie' : ['average', 'choice'],
             'imdb_score' : imdb_scores,
              'tmdb_popularity' : tmdb_popularity,
              'tmdb_score' : tmdb_scores,
              'runtime' : runtimes} )
    
    fig = go.Figure(data=[go.Bar(
    name = 'imdb_score',
    x = df_score_runtime['movie'].values.tolist(),
    y = df_score_runtime['imdb_score'].values.tolist()
                        ),
                       go.Bar(
    name = 'tmdb_score',
    x = df_score_runtime['movie'].values.tolist(),
    y = df_score_runtime['tmdb_score'].values.tolist()
                       ),
                        go.Bar(
    name = 'tmdb_popularity',
    x = df_score_runtime['movie'].values.tolist(),
    y = df_score_runtime['tmdb_popularity'].values.tolist()
                        ),
                       go.Bar(
    name = 'runtime',
    x = df_score_runtime['movie'].values.tolist(),
    y = df_score_runtime['runtime'].values.tolist()

                        )]
                    )
    fig.update_layout(title='<b>전체평균 VS 선택한 타이틀</b>',
                    width=1000, height=500)                
    st.plotly_chart(fig)


def run_home() :
    df= pd.read_csv('data/new_data.csv', index_col=0)
    df = df.drop_duplicates(['title'], keep = 'first')

    search = st.text_input('제목 검색')
    search_result = df.loc[df['title'].str.lower().str.contains(search.lower(), na=False)]
    search_list = search_result['title'].values


    if len(search_list) != 0 :
        selected = st.selectbox('검색 결과 리스트', search_list)
        st.markdown("---")
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #9EE681;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">{}</p>'.format(selected), unsafe_allow_html=True)
    
        # 동영상 출력
        col_video1, _ = st.columns(2)
        with col_video1 :
            st.video(videosSearch(selected))
        
        col1, col2 = st.columns([5,3])
        # 정보들 출력
        movie_info(col1, col2, df, selected)

        avg_choice_chart(df, selected)
        st.markdown('---')

        # 추천프로그램 데이터 프레임 가져오기
        recommended_movies = recommended_movie(selected)
        recommend_list = recommended_movies['Title'].values
        recommend_choice = st.selectbox('추천 리스트', recommend_list)

        if st.button('선택한 프로그램 정보') :
            
            # 추천 프로그램 정보 출력
            st.markdown(""" <style> .font {
            font-size:35px ; font-family: 'Cooper Black'; color: #9EE681;} 
            </style> """, unsafe_allow_html=True)
            st.markdown('<p class="font">{}</p>'.format(recommend_choice), unsafe_allow_html=True)


            # 동영상 출력
            col_video2, _ = st.columns(2)
            with col_video2 :
                st.video(videosSearch(recommend_choice))
                                    
            col3, col4 = st.columns([5,3])

            # 정보들 출력
            with col3 :
                st.subheader('유사도')
                similarity = recommended_movies.loc[recommended_movies['Title'] == recommend_choice,
                                                'Similarity'].values[0] * 100
                st.text('{}%'.format(round(similarity,2)))
            movie_info(col3, col4, df, recommend_choice)

            # 차트 출력
            avg_choice_chart(df, recommend_choice)






        


