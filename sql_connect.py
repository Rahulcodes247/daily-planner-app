import streamlit as st
conn = st.connection("sql")


n = st.slider("Pick a number")

if st.button("Add the number!"):
    with conn.session as session:
        session.execute("INSERT INTO numbers (val) VALUES (:n);", {"n": n})
        session.commit()