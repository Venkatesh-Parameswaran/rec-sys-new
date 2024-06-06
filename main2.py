import streamlit as st
import pandas as pd
import pickle
import requests
import numpy as np

# Load the movies data and similarity matrix
movies = pd.read_csv('data_not_final.csv')
similarity = pickle.load(open('reduced_final_similarity_3.5k_new.pkl', 'rb'))

# Function to fetch movie posters from OMDB API
def fetch_poster(movie_id):
    api_key = "a9a9a557"  # Replace with your actual OMDB API key
    url = f'https://www.omdbapi.com/?i={movie_id}&apikey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        poster_url = data.get('Poster')
        return poster_url
    else:
        return None

# Recommendation function
def recommend_movies(movie_name, similarity_matrix, movie_data, top_n=10):
    movie_name = movie_name.lower()
    if movie_name not in movie_data['title'].str.lower().values:
        return "Movie not found in the database."
    movie_index = movie_data[movie_data['title'].str.lower() == movie_name].index[0]
    similarity_scores = similarity_matrix[movie_index]
    similar_movie_indices = np.argsort(similarity_scores)[::-1][1:top_n + 1]
    recommended_movies = [movie_data.iloc[idx]['title'] for idx in similar_movie_indices]
    return recommended_movies

# Streamlit web application
st.title('MovieMate: Your Personal Movie Recommender 🎬')

# Introduction and description
st.markdown("""
    <div style="text-align: center;">
        <h2 style="font-family: 'Arial Black', sans-serif; color: #FF5733; font-size: 40px;">
            Welcome to MovieMate! <span style="font-size: 30px;">(Click for Tailored Recommendations!)</span>
        </h2>
        <p style="font-family: Arial, sans-serif; color: #FFA07A; font-size: 20px;">
            Developed MovieMate, a movie recommendation system that provides personalized recommendations across a dataset of 50,000 movies.
            Orchestrated the development and deployment of a movie recommendation system, leveraging TF-IDF, spaCy, NLTK, and clustering machine learning algorithms like DB scan for customized recommendations.
            Boosted user interaction and retention rates post-implementation of MovieMate using NLP algorithms for personalized recommendations.
        </p>
    </div>
""", unsafe_allow_html=True)

# Movie selection
selected_movie_name = st.selectbox(
    'What movie are you interested in?',
    movies['title'].values
)

# Check if the "Recommend" button is clicked
if st.button('Recommend'):
    recommendations = recommend_movies(selected_movie_name, similarity, movies)
    if isinstance(recommendations, str):
        st.error(recommendations)  # Display an error message if the movie is not found
    else:
        num_recs = len(recommendations)  # All recommendations
        for i in range(0, num_recs, 2):
            col1, col2 = st.columns(2)
            for j in range(2):
                if i + j < num_recs:
                    recommended_movie = recommendations[i + j]
                    movie_data = movies[movies['title'] == recommended_movie].iloc[0]
                    movie_poster_url = fetch_poster(movie_data['imdb_id'])

                    with col1 if j == 0 else col2:
                        st.image(movie_poster_url, width=340)
                        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
                        st.markdown("<div style='width: 20px;'></div>", unsafe_allow_html=True)

                        expander = st.expander(f' More Info  -   *********{recommended_movie}*********')
                        with expander:
                            st.subheader('Overview')
                            st.write(movie_data['overview'])
                            st.subheader('Lead Actors')
                            st.write(movie_data['actor'])
                            st.subheader('Director')
                            st.write(movie_data['director'])
                            st.subheader('Genre')
                            st.write(movie_data['genre_names'])

st.markdown("""
    <style>
        .stApp {
            background-image: url("https://github.com/Venkatesh-Parameswaran/rec-sys-new/blob/main/mm%20bk1.png");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }

        .prediction-output {
            font-family: 'Arial', sans-serif;
            color: #00FF00; /* Light Green color */
            font-size: 30px;
            text-align: center;
            background: rgba(0, 0, 0, 0.7);
            padding: 20px;
            border-radius: 15px;
            margin-top: 20px;
        }

        .highlight {
            font-size: 40px;
            font-weight: bold;
            color: #FFD700; /* Gold color */
        }
    </style>
""", unsafe_allow_html=True)
