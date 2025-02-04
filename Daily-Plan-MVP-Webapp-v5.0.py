import openai
import streamlit as st
import json
import os
import datetime
from datetime import time
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Define the required scopes
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Load GCP credentials from Streamlit secrets
GCP_CREDENTIALS = st.secrets["gcp"]["GCP_CREDENTIALS"]

# Convert string to dictionary for Google Cloud credentials
GCP_CREDENTIALS_dict = json.loads(GCP_CREDENTIALS)


# Authenticate with Google Cloud
credentials = service_account.Credentials.from_service_account_info(GCP_CREDENTIALS_dict, scopes=SCOPES)
client = gspread.authorize(credentials)

# Load OpenAI API Key from Streamlit secrets
OPENAI_API_KEY = st.secrets["openai"]["OPENAI_API_KEY"]

# Set the OpenAI API key for use in your application
openai.api_key = OPENAI_API_KEY # Assign directly as a string

# Open the Google Sheet
spreadsheet = client.open("daily-planner-app-mvp-feedback")
sheet = spreadsheet.sheet1  # Access first sheet

# Open Sheet 2 for logging usage
daily_logs_sheet = spreadsheet.worksheet("Sheet2")  # Ensure Sheet2 exists in your Google Sheet

# Function to log app usage (only timestamp)
def log_app_usage():
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        daily_logs_sheet.append_row([timestamp])
    except Exception as e:
        st.error(f"Trivia1: {e}")
        
# Function to save feedback to Google Sheets
def save_feedback_to_gsheet(feedback):
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([timestamp, feedback])
        st.success("Feedback saved to Google Sheets!")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Open Sheet 3 for logging usage
daily_logs_inputs = spreadsheet.worksheet("Sheet3")  # Assuming Sheet3 is present

# Function to log each use of the app
def log_app_inputs(user_inputs):
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_data = [
            timestamp,
            user_inputs["wake_up_time"],
            user_inputs["sleep_time"],
            ", ".join(user_inputs["activities"]),
            json.dumps(user_inputs["activity_hours"]),  # Store activity hours as JSON string
            user_inputs["breakfast_time"],
            user_inputs["lunch_time"],
            user_inputs["dinner_time"],
            user_inputs["preferences"]
        ]
        daily_logs_inputs.append_row(log_data)
    except Exception as e:
        st.error(f"Trivia2: {e}")
        
# Function to generate daily plan
def generate_daily_plan(user_inputs):
    prompt = f"""
    You are an AI assistant specializing in creating structured and efficient daily planners. Your goal is to optimize the user's time while respecting their constraints and preferences.

    **User Information:**
    - **Wake-up Time:** {user_inputs['wake_up_time']}
    - **Sleep Time:** {user_inputs['sleep_time']}
    - **Selected Activities:** {', '.join(user_inputs['activities'])}
    - **Allocated Time for Activities (in hours):** {user_inputs['activity_hours']}
    - **Preferred Meal Times:** Breakfast at {user_inputs['breakfast_time']}, Lunch at {user_inputs['lunch_time']}, Dinner at {user_inputs['dinner_time']}
    - **User Constraints/Preferences:** {user_inputs.get('preferences', 'None')}

    **Task:**
    - Create a **well-structured** and **realistic** daily schedule, ensuring activities fit within the available time.
    - Use **a table format** to clearly present the time slots and activities.
    - Ensure a **logical flow** between activities and maintain proper breaks.
    - Adjust activities to avoid scheduling conflicts and ensure a smooth daily routine.

    **Output Format:**
    - Use a **Markdown Table** format with the following columns:  
      | Time Slot  | Activity | Notes (if any) |
      |-----------|----------|----------------|
      | 6:00 AM - 7:00 AM | Wake-up & Morning Routine | Freshen up, meditation, light exercise |
      | 7:00 AM - 8:00 AM | Workout | Gym/Yoga/Outdoor walk |
      | 8:00 AM - 8:30 AM | Breakfast | Healthy meal |
      | 9:00 AM - 12:00 PM | Work Session 1 | Deep focus work |
      | ... (continue until bedtime) |

    **Output Rules:**
    - Return the planner in **Markdown Table format** (with `|` and `---` for columns).
    - Use **clear, concise language** for activities.
    - Ensure a balanced routine with breaks and transitions.
    - No unnecessary explanations—only return the structured daily planner table.

    Generate the daily planner now.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant specializing in creating efficient, realistic, and personalized daily planners for busy professionals. Your output should be clear, well structured, and actionable."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content'].strip()

# Streamlit UI
def main():
    st.title("Personalized Daily Planner Assistant")
    st.write("Plan your day efficiently with AI-driven assistance.")

     # Step 1: Ask wake-up and sleep time
    st.subheader("Daily Routine Setup")
    if 'wake_up_time' not in st.session_state:
        st.session_state.wake_up_time = time(6, 0)  # Default to 6:00 AM
    if 'sleep_time' not in st.session_state:
        st.session_state.sleep_time = time(22, 0)  # Default to 10:00 PM

    wake_up_time = st.time_input("What time do you wake up?", value=st.session_state.wake_up_time, key="wake_up_time")
    sleep_time = st.time_input("What time do you go to sleep?", value=st.session_state.sleep_time, key="sleep_time")
    
    # Step 2: Ask for key activities selection
    st.subheader("Select the key activities you want to include in your daily plan:")
    activities = [
    "Commute/Travel", 
    "Work/Office Tasks", 
    "Snacks", 
    "Fitness/Exercise", 
    "Personal Care", 
    "Family Time", 
    "Personal Development", 
    "Relaxation/Leisure", 
    "Social/Networking",
    "Passion Project"
    ]
    
    if 'selected_activities' not in st.session_state:
        st.session_state.selected_activities = []

    selected_activities = st.multiselect("Select activities", activities, default=st.session_state.selected_activities, key="selected_activities")

# Step 3: Ask for hours for each selected activity
    activity_hours = {}
    for activity in selected_activities:
        if f"hours_{activity}" not in st.session_state:
            st.session_state[f"hours_{activity}"] = 1  # Default hour is 1.0
        
        activity_hours[activity] = st.number_input(f"How many hours for {activity}?", 
                                                  min_value=0.0, max_value=24.0, 
                                                  value=st.session_state[f"hours_{activity}"], 
                                                  step=0.1, key=f"hours_{activity}")
 

    # Step 4: Ask preferred times for meals
    st.subheader("Preferred Meal Times")
    if 'breakfast_time' not in st.session_state:
        st.session_state.breakfast_time = datetime.time(8, 0)
    if 'lunch_time' not in st.session_state:
        st.session_state.lunch_time = datetime.time(13, 0)
    if 'dinner_time' not in st.session_state:
        st.session_state.dinner_time = datetime.time(20, 0)

    breakfast_time = st.time_input("Preferred time for breakfast?", value=st.session_state.breakfast_time, key="breakfast_time")
    lunch_time = st.time_input("Preferred time for lunch?", value=st.session_state.lunch_time, key="lunch_time")
    dinner_time = st.time_input("Preferred time for dinner?", value=st.session_state.dinner_time, key="dinner_time")


   # Step 5: Ask for any constraints or preferences
    if 'preferences' not in st.session_state:
        st.session_state.preferences = ""
        
    preferences = st.text_area("Any constraints or preferences? (e.g., workout in the morning, family time before dinner, etc.)", 
                              value=st.session_state.preferences, key="preferences")
    
   
    # Step 6: Compile all inputs and generate the daily plan
    if st.button("Generate Daily Plan", key="generate_button"):
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

        # Store the plan in session state
        st.session_state.daily_plan = daily_plan
        st.session_state.user_inputs = user_inputs

        # Log the usage in Sheet 2
        log_app_usage()

        # Log the usage in Sheet 3
        log_app_inputs(user_inputs)
    
    # Display the daily plan if it exists
    if "daily_plan" in st.session_state and st.session_state.daily_plan:
        st.subheader("Your Daily Planner:")
        st.text(st.session_state.daily_plan)
        
        # Feedback loop for revisions
        feedback = st.radio("Is this plan okay?", ("Yes", "No"), key="feedback_radio")
        if feedback == "No":
            changes = st.text_area("Specify the changes you want:", key="changes_text")
            if st.button("Regenerate Plan", key="regenerate_button"):
                st.session_state.user_inputs["Additional Changes"] = changes
                with st.spinner("Regenerating your daily planner..."):
                    updated_plan = generate_daily_plan(st.session_state.user_inputs)
                st.session_state.daily_plan = updated_plan

        feedback = st.text_area("Provide feedback:", "")
        if st.button("Save Feedback"):
            save_feedback_to_gsheet(feedback)

if __name__ == "__main__":
    main()
