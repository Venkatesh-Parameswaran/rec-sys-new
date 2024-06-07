import streamlit as st
import pandas as pd
import pickle
import requests
import numpy as np
import zipfile
import os

# Path to your zip file (relative path)
zip_file_path = 'path_to_your_zip_file.zip'
extract_dir = 'unzipped_model'
current_directory = os.getcwd()
zip_file_path = os.path.join(current_directory, zip_file_path)
extract_dir = os.path.join(current_directory, extract_dir)
os.makedirs(extract_dir, exist_ok=True)
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)

# Load your model
model_filename = [f for f in extracted_files if f.endswith('.h5')][0]
model_path = os.path.join(extract_dir, model_filename)
model = tf.keras.models.load_model(model_path)

# Set background image using an online URL
background_image_url = "https://github.com/Venkatesh-Parameswaran/rec-sys-new/blob/main/background4.jpg"

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

# Example hero image URL
hero_img_url = "https://path_to_your_hero_image.jpg"

# Display hero image
st.image(hero_img_url, use_column_width=True)

# Load movie data
movies = pd.read_csv('data_not_final.csv')
similarity = pickle.load(open('reduced_final_similarity_3.5k_new.pkl', 'rb'))

def fetch_poster(movie_id):
    api_key = "a9a9a557"
    url = f'https://www.omdbapi.com/?i={movie_id}&apikey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('Poster')
    return None

def recommend_movies(movie_name, similarity_matrix, movie_data, top_n=10):
    movie_name = movie_name.lower()
    if movie_name not in movie_data['title'].str.lower().values:
        return "Movie not found in the database."
    movie_index = movie_data[movie_data['title'].str.lower() == movie_name].index[0]
    similarity_scores = similarity_matrix[movie_index]
    similar_movie_indices = np.argsort(similarity_scores)[::-1][1:top_n + 1]
    recommended_movies = [movie_data.iloc[idx]['title'] for idx in similar_movie_indices]
    return recommended_movies

st.title('MovieMate: Tailored Movie Recommendations')

selected_movie_name = st.selectbox('What movie are you interested in?', movies['title'].values)

if st.button('Recommend'):
    recommendations = recommend_movies(selected_movie_name, similarity, movies)
    if isinstance(recommendations, str):
        st.error(recommendations)
    else:
        num_recs = len(recommendations)
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

st.markdown("""
## Thank You!
Thank you for using MovieMate. We appreciate your interest and hope you found this application helpful.
""")

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
}
</style>
<div class="footer">
    <p>© 2024 MovieMate. All rights reserved. | Developed by Venkatesh</p>
</div>
""", unsafe_allow_html=True)
