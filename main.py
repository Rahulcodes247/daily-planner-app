import streamlit as st
from streamlit_google_auth import Authenticate  # Adjust this import to your actual lib
print(f"session = {st.session_state}")

authenticator = st.session_state.get("authenticator")

if authenticator is None:
    authenticator = Authenticate(
        secret_credentials_path='google_credentials.json',
        cookie_name='my_cookie_name',
        cookie_key='this_is_secret',
        redirect_uri='http://localhost:8501',
    )
    st.session_state["authenticator"] = authenticator

user_data = authenticator.check_authentification()
print(f"{user_data = }")
st.write(user_data)
if user_data:
    st.session_state["connected"] = True
    st.session_state["user_info"] = user_data
    user_info = st.session_state['user_info']
    st.write(f"Hello, {user_info.get('name', 'User')}")
    st.write(f"Your email is {user_info.get('email', 'Not found')}")
    if st.button("Log out"):
        authenticator.logout()
        st.rerun()
else:
    authenticator.login()

# # After login success
if st.session_state['connected']:
    user_info = st.session_state['user_info']
    st.image(user_info.get('picture', ''))
    st.write(f"Hello, {user_info.get('name', 'User')}")
    st.write(f"Your email is {user_info.get('email', 'Not found')}")

    if st.button("Log out"):
        authenticator.logout()
        st.rerun()


