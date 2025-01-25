#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import openai
import streamlit as st
import json
import datetime
from datetime import time
import pandas as pd


# In[ ]:


#Anaconda Command Prompt codes
#streamlit run "Daily Plan MVP Webapp v4.3.py"
#jupyter nbconvert --to script "Daily Plan MVP Webapp v4.3.ipynb"
#cd C:\Users\rahul.kumar\Jupyter Notebook Codes\daily-planner-app
#pip install pandas xlsxwriter
#pip install openai==0.28.0


# In[ ]:


import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Access the API key
api_key = os.getenv('OPENAI_API_KEY')

# Use the API key in your application
print(f"My OpenAI API Key is: {api_key}")


# In[ ]:


def generate_daily_plan(user_inputs):
    """
    Generate a daily planner based on the user's input, including their wake-up time, selected activities, and constraints.
    """
    prompt = f"""
    The user has provided the following information:
    - Wake-up time: {user_inputs['wake_up_time']}
    - Sleep time: {user_inputs['sleep_time']}
    - Activities selected: {', '.join(user_inputs['activities'])}
    - Hours allocated for activities: {user_inputs['activity_hours']}
    - Preferred times for meals: Breakfast: {user_inputs['breakfast_time']}, Lunch: {user_inputs['lunch_time']}, Dinner: {user_inputs['dinner_time']}
    - Constraints or preferences: {user_inputs.get('preferences', 'None')}

    Create a structured daily plan that includes time slots for each activity, with special attention to any constraints or preferences, ensuring that the user's priorities are met.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant specializing in creating personalized daily planners."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content'].strip()


# In[ ]:


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
        "Sleep", "Commute", "Eating Food", "Body Care", "Office Work", "Family Time", 
        "Fitness", "Meditation", "Reading", "Personal Development", "Writing", 
        "Social Media", "Cooking", "Caring for Kid", "Playing", "Playing with Kid"
    ]
    
    if 'selected_activities' not in st.session_state:
        st.session_state.selected_activities = []

    selected_activities = st.multiselect("Select activities", activities, default=st.session_state.selected_activities, key="selected_activities")


    # Step 3: Ask for hours for each selected activity
    activity_hours = {}
    for activity in selected_activities:
        if f"hours_{activity}" not in st.session_state:
            st.session_state[f"hours_{activity}"] = 1  # Default hour is 1
        
        activity_hours[activity] = st.number_input(f"How many hours for {activity}?", 
                                                  min_value=0, max_value=24, 
                                                  value=st.session_state[f"hours_{activity}"], 
                                                  step=1, key=f"hours_{activity}")
 

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


        # JSON Export Button (always visible if a plan exists)
        st.subheader("Export Your Daily Plan")
        output_json = {
            "Daily Plan": st.session_state.daily_plan,
            "User Inputs": st.session_state.user_inputs
        }
        output_json_str = json.dumps(output_json, indent=4)
    
        st.download_button(
            label="Download Daily Plan as JSON File",
            data=output_json_str,
            file_name="Daily_Plan.json",
            mime="application/json",
            key="download_json_button"
        )      

if __name__ == "__main__":
    main()

