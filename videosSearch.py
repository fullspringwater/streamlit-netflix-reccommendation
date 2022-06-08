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