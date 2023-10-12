import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from database_importer import *
from datetime import datetime
from crypto_settings import CryptoSettings
import re
from time import sleep

def password_is_secure(password):
    if len(password) < 10:
        st.error("Password is does not have the minimum length")
        return False

    spacial_character = ['$', '#', '@', '!', '*']
    if not any(char in spacial_character for char in password):
        st.error("Password does not contain a spacial character: " + str(spacial_character))
        return False
    else:
        return True


def logged_in_profile():

    st.markdown("<h1 style='text-align: center;'>Profile</h1>", unsafe_allow_html=True)
    st.header("Here you can see your profile and make changes to it")
    st.write(f"You are logged as {username}")

    user = execute_sql_command("SELECT * FROM USER WHERE username = ?", (username,))

    if user == []:
        st.error("Wrong username or password")
    else:
        user = user[0]
        id_valid = False
        with (st.form("update_profile")):
            username_col, password_col, rol_col, identifier_col, birthdate_col = st.columns(5)
            with username_col:
                new_username = st.text_input("Username", value=user[0], key="username_n", disabled=True)
            with password_col:
                new_password = st.text_input("Password",value="*********",key="password_n")
            with rol_col:
                st.text_input("Role", value=user[2], key="role", disabled=True)
            with identifier_col:
                new_id = st.text_input("DNI/NIF", value=decrypt_id(user[4]), key="identifier", disabled=True)
            with birthdate_col:
                format = '%Y-%m-%d'
                date = datetime.strptime(user[3], format)
                new_date = st.date_input("Birthdate", key="birthdate", value=date)
            st.markdown("If you want to change your password, you have to do the forgot password method")

            if st.form_submit_button("Update profile"):
                if password_is_secure(new_password):
                    cripto = CryptoSettings()
                    new_password, salt = cripto.encode(new_password)
                    change_password(user[0], new_password, user[4], salt)

                if date != user[3]:
                    execute_sql_command("UPDATE USER SET birthdate = ? WHERE username = ?",
                                (new_date, username))
                    st.success("The details have been changed successfully")


        if st.button("Log out",type= "secondary"):
            st.session_state["username"] = ""
            switch_page("Log In")

        if st.button("Delete Account", type="primary"):
            delete_user(username)
            st.session_state["username"] = ""
            switch_page("Log In")


def draw_not_logged():
    st.subheader("You are not logged in, please log in or register")
    if st.button("Log In"):
        switch_page("Log In")

try:
    username = st.session_state["username"]
    if username == "":
        draw_not_logged()
    else:
        logged_in_profile()
except KeyError:
    draw_not_logged()