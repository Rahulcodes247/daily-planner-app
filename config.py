import streamlit as st


db_info = st.secrets["connections"]["sql"]
db_url = f"postgresql+psycopg2://{db_info['username']}:{db_info['password']}@{db_info['host']}:{db_info['port']}/{db_info['dbname']}"
