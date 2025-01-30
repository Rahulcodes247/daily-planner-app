import openai
import streamlit as st
import json
import os
import datetime
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Hardcode GCP credentials (usually a JSON file, but here it is a dictionary for simplicity)
gcp_credentials = {
  "type": "service_account",
  "project_id": "daily-planner-app-449118",
  "private_key_id": "20017fe39375b6d02c1222a6244af220492c27c5",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCx01zg5R+uN0xG\nYX9w/OtNrzkg0EZpTdbw5XH/fX9UVQHG/w4y1JdnGO9WwUc1tiqM1I928n8KHVgB\neesQhpR4qYBYXpQK6JwkoDOSS4gAb1dNWaZnoGUZU4l8ycu/bzpGMNhu5MOvjUkN\nWK4usyfnqpU5WfVkR/yoRHXcKOr26iTPpbmWJFekJQaxRmMJKu3Hto80gJChGz5t\n/OXNLo8RsMoBJi41WadA9olGSmzL3ULDKrl68KGEVH3aUw/AjTrDBL1Ux4UvdBPV\nqcGHLTC9oxin8C3/r3tkwgnWAmRVSgez5RbnOMekpcd+AfNB1wa/YrbguQo7Mj21\nIBPX+d0vAgMBAAECggEAFJGSqi7GedPKnk9zusF+hCdS79E3e8G1rXqUs400F7CX\neomQ/l8pvhKbyIilsHhINq71gzgsaqKXReBwyKIQdV6BynbyH8rlGLVxEahr7ET0\nr61BerYKS6Imgoki6Js4fdrzhewvGFS60PDjgOJXKMxJ427c3AMZnesBSPxwpSuh\nVH/yQcQE/5o2mRIPT5EcT1Mah3x4bIrFfDeDwoXsFS2tzn2Fv1zcCkqcDnkEhVdy\nIyF2tgH9RAc4qW3s+H+uOpFnrMJ5ufheBsnGoza3Y+72hPPTIbTW4Ffw47jVTqSW\nzQDg8Jy9rPpij7q6zrCqyFcF+chnGv2hqMrHWTCLYQKBgQD0KMXdN8rTrqPbdtHi\nFuG4N7WYW6cUn2aFdnzeJKLmJhkdVu4bb3NQ1GOQDjv+MhjbawDu0SXUjtn0eMU7\nh1FTSE7tASW0JOsb2uG+9Eyvu1IP2T0XsnrnW3HKDRLmsxQO8DU7d9TaXsH1DjoT\nHvcyFjTcFrPOje45skIyOEd1zwKBgQC6cw+FC/12zRcwa2I819zpBeaYGZJIFWNE\nK7FnWModj7oWZVC8I0XG/oKD7hQsXSZOXkW5umaTjD/E2LHVBQ2LyHaNgWdGdtoW\nHWcxBqGrdDa2LEisG6odbUxbjlGTxW/1TL1rB3RUazATRdgrMdXvz/i0niOqGCAl\nXMz1GAJaoQKBgC+7ONNCcPhpD8d7txRH/OCSo4GhiUxSzSwSOd8DsoTjtc0yjWH3\nq8eFfeFPpxLOoGVkyc3mPUsMkjdk1MoKbi+l1ygmLUTGYuATLkayY7uHF0fZ5EOZ\ntMU970TcwXEwWR+CfiWeC5KVK73Ihjnut8ym4raUCZq7zHKjEqXWssGpAoGBAIm7\nh8J0KghB1xiIqyhhGir1lfPUKBCh5BOu5z1+BMizrPbwXySsNdabmpSVIkfng+2u\njHl4LmBe4Zirryq6sdgJ/THpXv5ZvB9MFzfLO1Cp5+TJb+HcCd31KMwVpUOxPVSL\nHP5col3eVMRX+yllhjHCg2oBzDzR16ViGXIRC2QhAoGBAM+Np7isy5g//V1lSwZY\nBN9CDcUXFmTO7KTukUVbUy37D0VA9Sh2CE/dkNDv/B5io8qe+g/XWm1n+rQ9LbgY\nS2/IO7LTbfZr9fHz0i4nencu72/YwsfnuqTvWN4aE/8YzUGdzkbDWWVsEcj7M6Pd\nq7zCZiZHsvLcl0veAfop5bN5\n-----END PRIVATE KEY-----\n",
  "client_email": "daily-planner-app@daily-planner-app-449118.iam.gserviceaccount.com",
  "client_id": "113298100176630980379",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/daily-planner-app%40daily-planner-app-449118.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}


# Create credentials from the hardcoded JSON
credentials = service_account.Credentials.from_service_account_info(gcp_credentials)

# Now you can use the credentials for GCP services like Google Sheets, Google Cloud Storage, etc.

# Fetch the API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

if not openai.api_key:
    raise ValueError("OpenAI API key is missing. Check Streamlit Secrets.")


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
