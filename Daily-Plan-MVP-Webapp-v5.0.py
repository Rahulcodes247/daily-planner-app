import openai
import streamlit as st
import json
import os
import datetime
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Load secrets
GCP_CREDENTIALS = st.secrets["gcp"]["GCP_CREDENTIALS"]

# Convert string to dictionary
GCP_CREDENTIALS_dict = json.loads(GCP_CREDENTIALS)

# Authenticate
credentials = service_account.Credentials.from_service_account_info(GCP_CREDENTIALS_dict)
client = gspread.authorize(credentials)

st.write("✅ Successfully authenticated with Google Sheets API!")

# Load OpenAI API Key from secrets
OPENAI_API_KEY = st.secrets["openai"]["OPENAI_API_KEY"]

# Set the OpenAI API key for use in your application
OPENAI.API_KEY = OPENAI_API_KEY


# Authenticate with Google Sheets
client = gspread.authorize(credentials)

# Open the Google Sheet
spreadsheet = client.open("Your Google Sheet Name")
sheet = spreadsheet.sheet1  # Access first sheet

# Function to save feedback to Google Sheets
def save_feedback_to_gsheet(feedback):
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([timestamp, feedback])
        st.success("Feedback saved to Google Sheets!")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Function to generate daily plan
def generate_daily_plan(user_inputs):
    prompt = f"""
    The user has provided the following information:
    - Wake-up time: {user_inputs['wake_up_time']}
    - Sleep time: {user_inputs['sleep_time']}
    - Activities selected: {', '.join(user_inputs['activities'])}
    - Hours allocated for activities: {user_inputs['activity_hours']}
    - Preferred meal times: Breakfast at {user_inputs['breakfast_time']}, Lunch at {user_inputs['lunch_time']}, Dinner at {user_inputs['dinner_time']}
    - Constraints or preferences: {user_inputs.get('preferences', 'None')}

    Create a structured daily plan that includes time slots for each activity, ensuring constraints are met.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant specializing in personalized daily planners."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content'].strip()

# Streamlit UI
def main():
    st.title("Personalized Daily Planner Assistant")
    
    wake_up_time = st.time_input("Wake-up time:", value=datetime.time(6, 0))
    sleep_time = st.time_input("Sleep time:", value=datetime.time(22, 0))
    
    activities = [
        "Sleep", "Commute", "Eating", "Body Care", "Work", "Family Time", 
        "Fitness", "Meditation", "Reading", "Personal Development", "Writing", 
        "Social Media", "Cooking", "Caring for Kid", "Playing"
    ]
    selected_activities = st.multiselect("Select activities:", activities, default=[])

    activity_hours = {activity: st.number_input(f"Hours for {activity}:", min_value=0, max_value=24, value=1, step=1) for activity in selected_activities}

    breakfast_time = st.time_input("Breakfast time:", value=datetime.time(8, 0))
    lunch_time = st.time_input("Lunch time:", value=datetime.time(13, 0))
    dinner_time = st.time_input("Dinner time:", value=datetime.time(20, 0))

    preferences = st.text_area("Constraints or preferences:", "")

    if st.button("Generate Daily Plan"):
        user_inputs = {
            "wake_up_time": str(wake_up_time),
            "sleep_time": str(sleep_time),
            "activities": selected_activities,
            "activity_hours": activity_hours,
            "breakfast_time": str(breakfast_time),
            "lunch_time": str(lunch_time),
            "dinner_time": str(dinner_time),
            "preferences": preferences
        }
        with st.spinner("Generating your daily plan..."):
            daily_plan = generate_daily_plan(user_inputs)
        st.subheader("Your Daily Plan:")
        st.text(daily_plan)

        feedback = st.text_area("Provide feedback:", "")
        if st.button("Save Feedback"):
            save_feedback_to_gsheet(feedback)

if __name__ == "__main__":
    main()
