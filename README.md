<h1 align="center">streamlit-netflix-recommendation-app</h1>

## Description
- 넷플릭스 영상 제목, 장르, 타입을 선택, 검색하여 그에 해당하는 프로그램에 대한 정보를 볼 수 있다.
- 해당 프로그램와 유사한 다른 영상들도 추천 해준다.

##
## Environment
- Python 3.7


##
## Prerequisite

```
pip install streamlit
```

```
pip install youtube-search-python
```

```
pip install joblib
```

## Recommendation System
knn을 이용해 가장 거리가 가장 가까운 (유사도가 가장 높은) 5개를 추출했다.
![knn](https://user-images.githubusercontent.com/105832330/172280125-12d3f63b-3eea-48b3-ae72-bc94da8070c4.png)



## Usage
![netflix_app_begin](https://user-images.githubusercontent.com/105832330/172275238-ffbab2d0-c37a-4ca4-8ddf-ab2db13ece13.gif)

![netflix_app_test](https://user-images.githubusercontent.com/105832330/172278582-f52e660b-2491-492b-a061-2fd570e59677.gif)
