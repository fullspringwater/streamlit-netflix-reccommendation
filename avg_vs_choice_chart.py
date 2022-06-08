import plotly.graph_objs as go
import streamlit as st
import pandas as pd
# 차트 출력함수 
def avg__vs_choice_chart(df, title) :
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