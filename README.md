<h1 align="center">streamlit-netflix-recommendation-app</h1>

## 🔶 Description

✅ 넷플릭스 영상 제목, 장르, 타입을 선택, 검색하여 그에 해당하는 프로그램에 대한 정보를 볼 수 있습니다.

✅ 해당 프로그램과 비슷한 영상을 추천해 보여줍니다.

## 🔶 Dataset Source

https://www.kaggle.com/datasets/victorsoeiro/netflix-tv-shows-and-movies?select=titles.csv
 - ID:  타이틀 ID
 - title: 제목의 이름
 - show type: TV 쇼 또는 영화
 - description: 간략한 설명
 - release year: 출시 연도
 - age certification: 연령 인증
 - runtime: 에피소드(SHOW) 또는 영화의 길이
 - genres: 장르 목록입니다.
 - production countries: 타이틀을 제작한 국가 목록
 - seasons: SHOW인 경우 시즌 수
 - IMDB ID: IMDB의 타이틀
 - IMDB Score:  IMDB 점수.
 - IMDB Votes: IMDB 투표수
 - TMDB Popularity:  TMDB 인기도
 - TMDB Score:  TMDB 점수
 
##
## 🔶 Environment

✅ Python 3.7

##
## 🔶 Prerequisite

```
pip install streamlit
```

```
pip install youtube-search-python
```

```
pip install joblib
```

## 🔶 Recommendation System

✅ KNN을 이용해 가장 거리가 가장 가까운 (유사도가 가장 높은) 5개를 뽑아 추천하도록 했습니다.
![knn](https://user-images.githubusercontent.com/105832330/172280125-12d3f63b-3eea-48b3-ae72-bc94da8070c4.png)



## 🔶 Usage

### 실행하기
![netflix_app_begin](https://user-images.githubusercontent.com/105832330/172275238-ffbab2d0-c37a-4ca4-8ddf-ab2db13ece13.gif)

### 테스트
![netflix_app_test](https://user-images.githubusercontent.com/105832330/172278582-f52e660b-2491-492b-a061-2fd570e59677.gif)
