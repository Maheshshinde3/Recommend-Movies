import streamlit as st 
import pickle
import joblib
import pandas as pd
import requests
import time
import os

# api_key = st.secrets["TMDB_API_KEY"]
api_key = os.environ.get('TMDB_API_KEY')
movies_list = pickle.load(open("allmovies.pkl","rb"))
distanc = joblib.load(open("distance.pkl","rb"))

def fetch_poster(movies_ids,session):
    try:
        
        response = session.get(f"https://api.themoviedb.org/3/movie/{movies_ids}?api_key={api_key}")
        print("response taken")
        data = response.json()
        print("data successfully got")
        return "https://image.tmdb.org/t/p/w500" + data["poster_path"]
    except:
        print("Sorry ! Data didn't got")
        return "images/ImageError.png"


def recommend(selected_movie):
    recommended_movies_posters =[]
    recommended_movies = []
    indexval = allmovies.loc[allmovies["title"] == selected_movie].index[0].item()
    distinctpoints = distanc[indexval]
    movies_list = sorted(list(enumerate(distinctpoints.tolist())),reverse = True ,key = lambda x:x[1])[1:6]
    session = requests.Session()
    for i in movies_list:
        movies_ids = allmovies.iloc[i[0]].movie_id
        recommended_movies.append(allmovies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movies_ids,session))
    return recommended_movies,recommended_movies_posters
        



allmovies = pd.DataFrame(movies_list)


st.title('Movie Recommendation')


selected_movie = st.selectbox(
    "Select the Movie You Liked:",
    # ("Email", "Home phone", "Mobile phone")
    allmovies["title"],
    index=None,
    placeholder="Select the Movie You Like",
)


if st.button("Recommend", type="primary"):
    recommended_movies,posters = recommend(selected_movie)
    movies_id = []
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommended_movies[0])
        st.image(posters[0])

    with col2:
        st.text(recommended_movies[1])
        st.image(posters[1])

    with col3:
        st.text(recommended_movies[2])
        st.image(posters[2])
        
    with col4:
        st.text(recommended_movies[3])
        st.image(posters[3])
    
    with col5:
        st.text(recommended_movies[4])
        st.image(posters[4])
   
     


