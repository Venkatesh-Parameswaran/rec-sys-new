import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Importing the model
pipe = pickle.load(open('pipe.pkl', 'rb'))
df = pd.read_csv('new_laptop.csv')

# Set the background image URL
background_image_url = "https://i.pinimg.com/564x/3f/1f/32/3f1f323e66f9b1fea2eeba591bc72d93.jpg"

# Add some styling to the page
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{background_image_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-color: rgba(255, 255, 255, 0.7); /* Semi-transparent background for Streamlit elements */
        color: #333333; /* Darker gray font color */
        font-size: 18px; /* Font size */
        font-family: Arial, sans-serif; /* Font family */
    }}
    .stTextInput, .stSelectbox, .stTextArea {{
        color: #333333 !important; /* Darker gray font color for input elements */
    }}
    .stButton>button {{
        color: #333333 !important; /* Darker gray font color for buttons */
    }}
    .stDataFrame td, .stDataFrame th {{
        color: #333333 !important; /* Darker gray font color for dataframes */
    }}
    .stMarkdown {{
        color: #333333; /* Darker gray font color for markdown */
    }}
    .stMarkdown a {{
        color: #0044cc; /* Darker blue font color for links */
    }}
    .stAlert > div > div > div > div, .stException > div > div > div > div {{
        color: #333333 !important; /* Darker gray font color for alerts and exceptions */
    }}
    .title-main {{
        font-size: 79px;
        color: #FFD700;
        font-family: 'Georgia', serif;
        text-shadow: 2px 2px #000000;
    }}
    .title-sub {{
        font-size: 39px;
        color: #FF4500;
        font-family: 'Arial', sans-serif;
    }}
    .welcome-message {{
        font-size: 30px;
        color: #333333;
        text-align: center;
        font-family: 'Verdana', sans-serif;
        margin-bottom: 20px;
    }}
    .footer {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #000000;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        color: white;
    }}
    .selectbox-label {{
        font-size: 25px;
        color: #333333;
        font-family: 'Arial', sans-serif;
    }}
    .stSubheader {{
        font-size: 25px;
        color: #0044cc;
        font-family: 'Arial', sans-serif;
    }}
    .expander-content {{
        background-color: rgba(0, 0, 0, 0.7);
        color: #FFD700;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Title and Subtitle
st.markdown('<div style="text-align:center"><h1 class="title-main">LapValue Predictor</h1><h2 class="title-sub">Find Your Laptop’s Worth Instantly!</h2></div>', unsafe_allow_html=True)

# Welcome Message
st.markdown(
    '''
    <div class="welcome-message">
        <h2 style="font-size: 32px;">Welcome to LapValue Predictor!</h2>
        <p>LapValue Predictor helps you estimate the value of your laptop based on its specifications. Just input the details, and get an instant price prediction!</p>
    </div>
    ''', 
    unsafe_allow_html=True
)

# Hero Image
hero_img_url = "https://path_to_your_hero_image/laptop_hero.jpg"
st.markdown(
    f'<img src="{hero_img_url}" style="width:100%;" class="hero-image">',
    unsafe_allow_html=True
)

# Short Guide
st.markdown(
    '''
    <div class="stSubheader">
        <h2>How It Works:</h2>
        <p>1. Select the brand, type, and specifications of your laptop.</p>
        <p>2. Click on "Predict Price" to get an estimated value of your laptop.</p>
    </div>
    ''',
    unsafe_allow_html=True
)

# Laptop Specifications Input
company = st.selectbox('Brand', df['Company'].unique())
type = st.selectbox('Type', df['TypeName'].unique())
ram = st.selectbox('Ram (in GB)', [2, 4, 6, 8, 12, 16, 24, 32, 64])
weight = st.number_input('Weight of the Laptop')
touchscreen = st.selectbox('Touchscreen', ['No', 'Yes'])
ips = st.selectbox('IPS', ['No', 'Yes'])
screen_size = st.number_input('Screen Size')
resolution = st.selectbox('Screen Resolution', ['1920x1080', '1366x768', '1600x900', '3840x2160', '3200x1800', '2880x1800', '2560x1600', '2560x1440', '2304x1440'])
cpu = st.selectbox('CPU', df['Cpu Brand'].unique())
hdd = st.selectbox('HDD(in GB)', [0, 128, 256, 512, 1024, 2048])
ssd = st.selectbox('SSD(in GB)', [0, 8, 128, 256, 512, 1024])
gpu = st.selectbox('GPU', df['Gpu brand'].unique())
os = st.selectbox('OS', df['os'].unique())

# Prediction Button
if st.button('Predict Price'):
    ppi = None
    if touchscreen == 'Yes':
        touchscreen = 1
    else:
        touchscreen = 0
    if ips == 'Yes':
        ips = 1
    else:
        ips = 0
    X_res = int(resolution.split('x')[0])
    Y_res = int(resolution.split('x')[1])
    ppi = ((X_res ** 2) + (Y_res ** 2)) ** 0.5 / screen_size
    query = np.array([company, type, ram, weight, touchscreen, ips, ppi, cpu, hdd, ssd, gpu, os])
    query = query.reshape(1, 12)
    predicted_price = np.exp(pipe.predict(query)[0])
    st.markdown(f'<h2 style="color: #333333;">The predicted price of this configuration is ${int(predicted_price)}</h2>', unsafe_allow_html=True)

# Thank You Message
st.markdown("""
<h2 class="stSubheader">Thank You!</h2>
<p class="stMarkdown">Thank you for using LapValue Predictor. We appreciate your interest and hope you found this application helpful.</p>
""", unsafe_allow_html=True)

# About Section
def init_session_state():
    session_state = st.session_state
    if 'sidebar_open' not in session_state:
        session_state.sidebar_open = False

if st.button("About LapValue Predictor"):
    st.session_state.sidebar_open = not st.session_state.sidebar_open

init_session_state()

if st.session_state.sidebar_open:
    st.sidebar.title("About")
    st.sidebar.info("""
        **LapValue Predictor** is a powerful tool designed to estimate the market value of laptops based on their specifications. It leverages machine learning algorithms to provide accurate price predictions.

        ### Key Features:
        - **Accurate Predictions**: Utilizing data analytics techniques and the XGBoost algorithm.
        - **User-Friendly Interface**: Simple and intuitive for seamless user experience.
        - **Interactive Web Application**: Built using Streamlit for interactive and responsive design.

        ### How It Works:
        1. **Enter Laptop Specifications**: Provide details like brand, type, RAM, etc.
        2. **Predict Price**: Click the button to get an estimated market value.
        
        ### Developer:
        Developed by Venkatesh, the LapValue Predictor showcases the power of data analytics and machine learning in practical applications. Have feedback or questions? Feel free to reach out!
    """)

# Footer
st.markdown("""
<div class="footer">
    <p>© 2024 LapValue Predictor. All rights reserved. | Developed by Venkatesh</p>
</div>
""", unsafe_allow_html=True)
