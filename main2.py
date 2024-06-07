import streamlit as st
import pandas as pd
import pickle
import requests
import numpy as np
import os

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

page_bg_img = f'''
<style>
    .stApp {{
        background-image: url("{background_image_url}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)
else:
    st.error("Background image not found. Please check the path.")

# Example hero image URL (hosted online for reliability)
hero_img_url = "https://example.com/path_to_your_hero_image.jpg"

# Display hero image
st.image(hero_img_url, use_column_width=True)

# Streamlit web application
st.title('MovieMate: Tailored Movie Recommendations')

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
                            st.subheader('Overview')
                            st.write(movie_data['overview'])
                            st.subheader('Lead Actors')
                            st.write(movie_data['actor'])
                            st.subheader('Director')
                            st.write(movie_data['director'])
                            st.subheader('Genre')
                            st.write(movie_data['genre_names'])

# Thank you message
st.markdown("""
## Thank You!
Thank you for using MovieMate. We appreciate your interest and hope you found this application helpful.
""")

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
