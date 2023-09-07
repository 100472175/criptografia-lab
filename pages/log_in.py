import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from database_importer import add_users
import sqlite3 as sqllite

st.set_page_config(
    page_title="Log In",
    layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
    initial_sidebar_state="collapsed",  # Can be "auto", "expanded", "collapsed"
    page_icon="📚"
)

col_1, col_2 = st.columns(2)
with col_1:
    with st.form("log_in_form"):
        st.markdown("<h1 style='text-align: center;'>Log In</h1>", unsafe_allow_html=True)
        st.header("Please state your username and password in order to access your account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        col_3, _, col_4 = st.columns(3)
        with col_3:
            submitted = st.form_submit_button("Log In")
            st.session_state["username"] = username
            if submitted:
                con = sqllite.connect("database.db")
                cur = con.cursor()
                cur.execute("SELECT * FROM USER WHERE username = ? AND password = ?", (username, password))
                user = cur.fetchall()
                con.close()
                if user == []:
                    st.error("Wrong username or password")
                else:
                    # Redirigir a la pagina principal
                    switch_page("Library")
        with col_4:
            f_password = st.form_submit_button("Forgot the password")


with col_2:
    with st.form("register_form"):
        st.markdown("<h1 style='text-align: center;'>Register Now</h1>", unsafe_allow_html=True)
        st.header("In case you don't have an account, please fill this forum to create one.")
        username = st.text_input("State your Username", key="username_r")
        password = st.text_input("State your Password", key="password_r", type="password")
        birthdate = st.date_input("Birthdate")
        identifier = st.text_input("DNI/NIF")
        submitted = st.form_submit_button("Register")
        if submitted:
            # autentificar
            try:
                add_users(username, password, birthdate, identifier)
                st.session_state["username"] = username
                switch_page("Library")
            except sqllite.IntegrityError:
                st.error("Username already exists, please choose another one")

            # Redirigir a la pagina principal


