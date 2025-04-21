import streamlit as st

if st.button("Log in"):
    st.login("google")
if st.experimental_user.is_logged_in:
    if st.button("Log out"):
        st.logout()
    st.write(f"Hello, {st.experimental_user.name}!")