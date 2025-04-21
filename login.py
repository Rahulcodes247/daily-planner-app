import streamlit as st
# from streamlit_oauth import OAuth2Component
# import requests

# App setup
client_id = st.secrets["google"]["client_id"]
client_secret = st.secrets["google"]["client_secret"]
print(f"Client ID: {client_id}")
print(f"Client Secret: {client_secret}")

redirect_uri = "http://127.0.0.1:8501"
auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
token_url = "https://oauth2.googleapis.com/token"
userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
# st.page_link("pages/home.py", label="", icon="🏠")
st.page_link("authenticate/login_callback.py", label="CallBack", icon="🏠")
# st.title("Google Login")

if st.button("Login"):
    print("user clicked login")
    st.login("google")
    print("got logged in")
    st.write(st.experimental_user)

if st.experimental_user.is_logged_in:
    print(st.experimental_user.to_dict())
    st.write(st.experimental_user)
