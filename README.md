<h1 align="center"> 🙌 streamlit-netflix-recommendation-app</h1>

## 📃 Description

✅ 넷플릭스 영상 제목, 장르, 타입을 선택, 검색하여 그에 해당하는 프로그램에 대한 정보를 볼 수 있습니다.

✅ 해당 프로그램과 비슷한 영상을 추천해 보여줍니다. 

✅ 추천 시스템은 K-NN 알고리즘을 이용해 가장 유사한 5개의 타이틀을 추출했습니다.

## 📘 Dataset Source

 👉 출처 : https://www.kaggle.com/datasets/victorsoeiro/netflix-tv-shows-and-movies?select=titles.csv

 - **ID** :  타이틀 ID
 - **title** : 제목
 - **show type** : TV  또는 영화
 - **description** : 간략한 설명
 - **release year** : 출시 연도
 - **age certification** : 연령 인증
 - **runtime** : 에피소드(SHOW) 또는 영화의 길이
 - **genres** : 장르 목록입니다.
 - **production countries** : 타이틀을 제작한 국가 목록
 - **seasons** : SHOW인 경우 시즌 수
 - **IMDB ID** : IMDB의 타이틀
 - **IMDB Score** :  IMDB 점수.
 - **IMDB Votes** : IMDB 투표수
 - **TMDB Popularity** :  TMDB 인기도
 - **TMDB Score** :  TMDB 점수
##
## 🛠 Environment

✅ Language : Python 3.7

##
## 🔨 Installation

```
pip install streamlit
```

```
pip install youtube-search-python
```

```
pip install joblib
```

```
pip install plotly==5.8.0
```

```
pip install scikit-learn
```
## 💼  VideosSearch

```python
from youtubesearchpython import VideosSearch
import streamlit as st
# Youtube 동영상 검색후 영상 출력
def videosSearch(search):
    videosSearch = VideosSearch('Netflix {}'.format(search), 
                                    limit = 3)
    j = 5
    for i in range(len(videosSearch.result()['result'])) :
        if search.lower() in videosSearch.result()['result'][i]['title'].lower() :
            j = i
            break                                
    if j != 5 :
        video_url = videosSearch.result()['result'][j]['link']
        st.video(video_url)
    else : 
        st.info('관련 영상을 찾을 수 없습니다.')
```
## 💼 Recommendation System

✅ KNN을 이용해 가장 거리가 가장 가까운 (유사도가 가장 높은) 5개를 뽑아 추천하도록 했습니다.
![knn](https://user-images.githubusercontent.com/105832330/172280125-12d3f63b-3eea-48b3-ae72-bc94da8070c4.png)





## 💿 Usage

### 실행하기
![netflix_app_begin](https://user-images.githubusercontent.com/105832330/172292297-fabb8eb7-6486-4965-b65d-2dabba0c9783.gif)


### 테스트
![netflix_app_test](https://user-images.githubusercontent.com/105832330/172278582-f52e660b-2491-492b-a061-2fd570e59677.gif)

### Url
http://ec2-3-39-230-35.ap-northeast-2.compute.amazonaws.com:8503/
