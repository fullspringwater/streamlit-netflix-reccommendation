import streamlit as st

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
