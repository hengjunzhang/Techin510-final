import streamlit as st
from dotenv import load_dotenv
import os
from utils.recommendation_engine import generate_plan
from db import insert_user_input, create_connection
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd


load_dotenv()

st.set_page_config(page_title="FitFeed", page_icon="🏋️")


st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page:", ["Describe Your Body", "Fitness & Diet Plan", "Your Body's Journey", "Training Demo", "Training Music"])


if page == "Describe Your Body":
    st.title("FitFeed")
    st.subheader("Enter your body parameters")
    with st.form("body_params"):
        age = st.number_input("Age", min_value=18, max_value=100)
        weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0)
        height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0)
        body_fat_percentage = st.number_input("Body Fat Percentage", min_value=1.0, max_value=70.0)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        activity_level = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"])
        goal = st.selectbox("Fitness Goal", ["Lose Weight", "Maintain Weight", "Gain Muscle"])
        submit_button = st.form_submit_button("Generate Plan")

    if submit_button:
        db_file = "user_data.db"
        conn = create_connection(db_file)
        user_data = (age, weight, height, body_fat_percentage, gender, activity_level, goal, str(datetime.now()))
        insert_user_input(conn, user_data)
        conn.close()
        st.session_state['fitness_plan'] = generate_plan(age, weight, height, body_fat_percentage, gender, activity_level, goal)
        st.success("Plans generated successfully!")

elif page == "Fitness & Diet Plan":
    st.title("Your Fitness & Diet Plan")
    if 'fitness_plan' in st.session_state:
        st.write(st.session_state['fitness_plan'])
    else:
        st.write("No fitness plan has been generated yet.")

elif page == "Your Body's Journey":
    db_file = "user_data.db"
    conn = create_connection(db_file)

    df = pd.read_sql_query("SELECT timestamp, weight, body_fat_percentage FROM user_inputs ORDER BY timestamp ASC", conn)
    conn.close()

    st.subheader("Weight Change Over Time")
    plt.figure()
    plt.plot(df['timestamp'], df['weight'], marker='o', linestyle='-')
    plt.xlabel('Time')
    plt.ylabel('Weight (kg)')
    plt.title('Weight Change Over Time')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())  
    plt.gcf().autofmt_xdate() 
    st.pyplot(plt)


    plt.clf()


    st.subheader("Body Fat Percentage Change Over Time")
    plt.figure()
    plt.plot(df['timestamp'], df['body_fat_percentage'], marker='o', linestyle='-')
    plt.xlabel('Time')
    plt.ylabel('Body Fat Percentage')
    plt.title('Body Fat Percentage Change Over Time')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())  
    plt.gcf().autofmt_xdate() 

    st.pyplot(plt)

    plt.clf()

elif page == "Training Demo":
    st.title("Training Demos")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.image('gifs/1.gif', use_column_width=True)
    with col2:
        st.image('gifs/2.gif', use_column_width=True)
    with col3:
        st.image('gifs/3.gif', use_column_width=True)

    col4, col5, col6 = st.columns(3)
    with col4:
        st.image('gifs/4.gif', use_column_width=True)
    with col5:
        st.image('gifs/5.gif', use_column_width=True)
    with col6:
        st.image('gifs/6.gif', use_column_width=True)

elif page == "Training Music":
    st.title("Training Music")
    audio_files = ['music/1.wav', 'music/2.wav', 'music/3.wav']
    for audio_file in audio_files:
        st.audio(audio_file, format='audio/wav')

