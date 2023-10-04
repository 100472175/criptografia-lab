import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from database_importer import *
import sqlite3 as sqllite # No se puede borrar debido al integrity error
import re
from crypto_settings import CryptoSettings
from cryptography.exceptions import InvalidKey
import base64
from time import sleep

st.set_page_config(
    page_title="Log In",
    layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
    initial_sidebar_state="collapsed",  # Can be "auto", "expanded", "collapsed"
    page_icon="📚"
)

def check_id(identifier):
    pattern = re.compile("^[0-9]{8}[A-Z]$|^[A-Z][0-9]{7}[A-Z]$")
    id_valid = pattern.match(identifier)
    if not id_valid:
        st.error("The identifier is not valid, please enter a valid one")
        return False
    return True

def check_password(password):
    if len(password) < 10:
        st.error("Password is does not have the minimum length")
        return False

    spacial_character = ['$', '#', '@', '!', '*']
    if not any(char in spacial_character for char in password):
        st.error("Password does not contain a spacial character: " + str(spacial_character))
        return False
    else:
        return True


f_password = False
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
            if submitted:
                user = execute_sql_command("SELECT * FROM USER WHERE username = ?", (username,))
                if user:
                    result = CryptoSettings()
                    try:
                        result = result.verify(password, user[0][1], user[0][5])
                        st.session_state["username"] = username
                        switch_page("Library")
                    except InvalidKey:
                        st.error("Password is not correct")
                else:
                    st.error("Account doesn't exist")

        with col_4:
            if st.form_submit_button("Forgot the password"):
                f_password = True

    with st.expander("Forgot password", expanded=f_password):
        with st.form("forgot_password"):
            username = st.text_input("Username")
            identifier = st.text_input("DNI/NIF")
            new_password = st.text_input("New Password", type="password")

            if st.form_submit_button("Change password"):
                exist = execute_sql_command("SELECT * FROM USER WHERE username = ? and id= ?", (username,identifier))
                if exist:
                    if check_id(identifier) and check_password(new_password):
                        cripto = CryptoSettings()
                        new_password, salt = cripto.encode(new_password)
                        dot = change_password(user, password, identifier, salt)
                        st.success("Password changed successfully")
                else:
                    st.error("Wrong username or id")

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
            try:
                add_users(username, password, birthdate, identifier)
                st.session_state["username"] = username
                switch_page("Library")
            except sqllite.IntegrityError:
                st.error("Username already exists, please choose another one")
                sleep(2)
                switch_page("Log In")
