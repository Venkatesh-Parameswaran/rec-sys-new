import streamlit as st
import pandas as pd
import pickle
import requests
import numpy as np

# Load movie data and similarity matrix
movies = pd.read_csv('data_not_final.csv')
similarity = pickle.load(open('reduced_final_similarity_3.5k_new.pkl', 'rb'))

# Function to fetch movie posters from the OMDB API
def fetch_poster(movie_id):
    api_key = "a9a9a557"  # Replace with your actual OMDB API key
    url = f'https://www.omdbapi.com/?i={movie_id}&apikey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('Poster')
    else:
        print("Error: Failed to fetch data from the OMDB API.")
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

# Set background image using an online file
background_image_url = "https://raw.githubusercontent.com/Venkatesh-Parameswaran/rec-sys-new/main/background4.jpg"
hero_img_url = "https://raw.githubusercontent.com/Venkatesh-Parameswaran/rec-sys-new/main/bk%20img5.jpg"

page_bg_img = f'''
<style>
    .stApp {{
        background-image: url("{background_image_url}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .title {{
        text-align: center;
        margin-bottom: 0;
    }}
    .title-main {{
        font-size: 64px;
        color: #FFD700;
        font-family: 'Georgia', serif;
        text-shadow: 2px 2px #000000;
    }}
    .title-sub {{
        font-size: 32px;
        color: #FF4500;
        font-family: 'Arial', sans-serif;
    }}
    .author {{
        text-align: center;
        font-size: 20px;
        color: #FFFFFF;
        font-family: 'Verdana', sans-serif;
        margin-top: 0;
        margin-bottom: 20px;
    }}
    .stSubheader {{
        font-size: 24px;
        color: #FFD700;
        font-family: 'Arial', sans-serif;
    }}
    .stMarkdown {{
        color: #FFD700;
        font-family: 'Arial', sans-serif;
    }}
    .expander-content {{
        background-color: rgba(0, 0, 0, 0.7);
        color: #FFD700;
    }}
    .welcome-message {{
        font-size: 20px;
        color: #FFFFFF;
        text-align: center;
        font-family: 'Verdana', sans-serif;
        margin-bottom: 20px;
    }}
    .hero-image {{
        margin-top: -20px;
    }}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Streamlit web application title
st.markdown('<div class="title"><h1 class="title-main">MovieMate</h1><h2 class="title-sub">Your Personalized Recommender</h2></div>', unsafe_allow_html=True)

# Author name
st.markdown('<div class="author">By Venkatesh</div>', unsafe_allow_html=True)

# Welcome message
st.markdown('<div class="welcome-message">Welcome to MovieMate!

MovieMate offers you personalized movie recommendations tailored to your taste. Dive into a world of cinematic exploration and discover your next favorite film! Simply select a movie you love, hit the "Recommend" button, and let MovieMate suggest similar movies that you might enjoy. Explore, discover, and find your next cinematic adventure with MovieMate!</div>', unsafe_allow_html=True)

# Display hero image
st.markdown(
    f'<img src="{hero_img_url}" style="width:100%;" class="hero-image">', 
    unsafe_allow_html=True )

# Define your selectbox to choose the movie
selected_movie_name = st.selectbox('What movie are you interested in?', movies['title'].values)

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
                        # Display movie poster with a larger width
                        st.image(movie_poster_url, width=340)

                        # Add custom spacing using HTML
                        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

                        # Add space between two movie columns
                        st.markdown("<div style='width: 20px;'></div>", unsafe_allow_html=True)

                        # Create an expander button to show additional information
                        expander = st.expander(f'More Info - {recommended_movie}')
                        with expander:
                            st.markdown('<h2 class="stSubheader">Overview</h2>', unsafe_allow_html=True)
                            st.markdown(f'<div class="stMarkdown">{movie_data["overview"]}</div>', unsafe_allow_html=True)
                            st.markdown('<h2 class="stSubheader">Lead Actors</h2>', unsafe_allow_html=True)
                            st.markdown(f'<div class="stMarkdown">{movie_data["actor"]}</div>', unsafe_allow_html=True)
                            st.markdown('<h2 class="stSubheader">Director</h2>', unsafe_allow_html=True)
                            st.markdown(f'<div class="stMarkdown">{movie_data["director"]}</div>', unsafe_allow_html=True)
                            st.markdown('<h2 class="stSubheader">Genre</h2>', unsafe_allow_html=True)
                            st.markdown(f'<div class="stMarkdown">{movie_data["genre_names"]}</div>', unsafe_allow_html=True)

# Thank you message
st.markdown("""
<h2 class="stSubheader">Thank You!</h2>
<p class="stMarkdown">Thank you for using MovieMate. We appreciate your interest and hope you found this application helpful.</p>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #0a0d36;
    text-align: center;
    padding: 10px;
    font-size: 14px;
    color: white;
}
</style>
<div class="footer">
    <p>© 2024 MovieMate. All rights reserved. | Developed by Venkatesh</p>
</div>
""", unsafe_allow_html=True)
