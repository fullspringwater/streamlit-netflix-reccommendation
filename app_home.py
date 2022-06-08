import streamlit as st
import pandas as pd
import joblib
from youtubesearchpython import VideosSearch
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
import plotly.graph_objs as go

# Youtube 동영상 검색후 영상 출력
def videosSearch(search):
    videosSearch = VideosSearch('Netflix {}'.format(search), 
                                    limit = 3)
    j = 5
    for i in range(len(videosSearch.result()['result'])) :
        if search.lower() in videosSearch.result()['result'][i]['title'].lower() :
            print(videosSearch.result()['result'][i]['link'])
            j = i
            break                                
    if j != 5 :
        video_url = videosSearch.result()['result'][j]['link']
        st.video(video_url)
    else : 
        st.info('관련 영상을 찾을 수 없습니다.')


# 추천 시스템
def recommended_movie(title):
    X = pd.read_csv('data/X.csv', index_col=0)
    y = pd.read_csv('data/y.csv', index_col=0)
    kn = joblib.load('data/kn.pkl')

    _, indices = kn.kneighbors(np.array(X.loc[title]).reshape(1,144))
    nearest_title = [y.iloc[i][0] for i in indices.flatten()][1:]
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
    age_dict = {'TV-MA' : '17세 미만의 어린이 혹은 청소년한테 부적절한 프로그램', 
            'R' : '수위가 매우 높은 성인영화. 18세 미만 관람불가', 
            'PG' : '전체 관람가지만, 폭력성이 존재하므로 어린이의 경우 보호자의 지도가 요구', 
            'TV-14' : '14세 미만의 어린이 혹은 청소년이 시청하려면 보호자 지도가 권장되는 프로그램', 
            'G' : '전체 관람가', 
            'PG-13' : '전체 관람가지만, 부모의 주의가 요구되며 13세 미만에게는 보호자 동반이 권고된다', 
            'Unknown' : '관람 등급이 등록되지 않았습니다.', 
            'TV-PG' : '어린이가 시청하려면 보호자 지도가 권장되는 프로그램' ,
            'TV-Y' : '영유아를 위한 프로그램', 
            'TV-G' : '모든 연령이 시청할 수 있는 프로그램. 다만 어린이를 대상으로 하지는 않았다', 
            'TV-Y7' : '7세 이상의 어린이를 위한 프로그램', 
            'NC-17' : '17세 이하 어린이 관람 불가 프로그램'}
    with col1 :
        st.subheader('관람 등급')
        age_class = df.loc[df['title'] == title,'age_certification'].values[0]
        st.text(age_class)
        st.text(age_dict[age_class])
            
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

        st.subheader('설명')
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

# 차트 출력함수 
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
                    width=1000, height=500, template = "plotly_dark",
                    font = dict(family = "PT Sans", size = 20))                
    st.plotly_chart(fig)


def run_home() :
    df= pd.read_csv('data/new_data.csv', index_col=0)
    df = df.drop_duplicates(['title'], keep = 'first')
     
    genres = ['Anything','Reality','European','Music','Family','Animation',
        'Comedy','Romance','Action','Thriller','Horror','Scifi',
        'History','Western','Crime','Documentation','Drama',
        'Sport','Fantasy','War']
    
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

        avg_choice_chart(df, selected)
        st.markdown('---')

        # 추천프로그램 데이터 프레임 가져오기
        recommended_movies = recommended_movie(selected)
        recommend_list = recommended_movies['Title'].values
        recommend_choice = st.selectbox('추천 리스트', recommend_list)

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
            avg_choice_chart(df, recommend_choice)
    else :
        st.warning('검색결과가 없습니다. 다시 검색해주세요')





        


