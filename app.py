
import numpy as np
import pandas as pd
import pickle
import streamlit as st

def recommend(watch_list, topk = 10):
    scores = np.zeros(similarity.shape[0],)
    index_list = []
    for movie in watch_list:
        index = movie_df[movie_df['title'] == movie].index[0]
        index_list.append(index)
        scores += similarity[index]
    recommended_movies = sorted(list(enumerate(scores)), reverse=True, key=lambda x: x[1])
    recommended_movies = [movie for movie in  recommended_movies if movie[0] not in index_list]
    return recommended_movies

st.header('Movie Recommender System')
movie_df = pd.read_json('data/tmdb_popular.json')
similarity = pickle.load(open('data/similarity_matrix.pkl','rb'))

movie_list = movie_df['title'].values

watch_list = st.multiselect(
    "시청한 영화 목록을 입력해주세요",
    movie_list
)
st.subheader('시청 목록')

watch_num = len(watch_list)
for i in range(watch_num//4 + 1):
    cols = st.columns(4)
    for j, col in enumerate(cols):
        if i*4 + j < watch_num:
            with col:
                title = watch_list[i*4 + j]
                movie = movie_df[movie_df['title'] == title].iloc[0]
                st.markdown(f"###### {title}")
                st.markdown(f"""
                            {movie.release_date} | {movie.runtime}분  
                            {' '.join(movie.genres)}
                            """)
                
                st.metric('평균 평점', float(movie.vote_average),delta = None)
                poster_path = "https://image.tmdb.org/t/p/w200/" + movie.poster_path
                st.image(poster_path)
                with st.expander("상세 정보"):
                    casts = [movie.cast_5[i] + '(' + movie.character_5[i] + ')' for i in range(5)]
                    st.markdown(f"""
                                  **출연**   
                                  {casts[0]}  
                                  {casts[1]}  
                                  {casts[2]}  
                                  {casts[3]}  
                                  {casts[4]}  
                                  **제작**  
                                  {movie.director[0]} | {movie.production_company[0]}  
                                  **줄거리**  
                                  {movie.overview}
                    """)
                

st.subheader('영화 추천')

if st.button('추천'):
    k = 10
    recommended_movies = recommend(watch_list, k)

    for idx, movie_id in enumerate(recommended_movies[:k]):
        movie = movie_df.iloc[movie_id[0]]
        col1, col2 = st.columns([3,2])
        with col1:
            st.subheader(movie.title)
            st.markdown(f"{movie.release_date} | {movie.runtime}분")
            st.markdown(f""" 
            {' '.join(movie.genres)}
            """)
            
            st.metric('평균 평점', float(movie.vote_average),delta = None)
            casts = [movie.cast_5[i] + '(' + movie.character_5[i] + ')' for i in range(5)]
            with st.expander("상세 정보"):
                st.markdown(f"""
                              **출연**   
                              {casts[0]}  
                              {casts[1]}  
                              {casts[2]}  
                              {casts[3]}  
                              {casts[4]}  
                              **제작**  
                              {movie.director[0]} | {movie.production_company[0]}  
                              **줄거리**  
                              {movie.overview}
                """)
        poster_path = "https://image.tmdb.org/t/p/w500/" + movie.poster_path
        col2.image(poster_path)
        
    
