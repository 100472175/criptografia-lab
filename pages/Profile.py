import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from database_importer import delete_user
import sqlite3 as sqllite
from datetime import datetime
import re
from time import sleep


def logged_in_profile():
    st.set_page_config(
        page_title="Log In",
        layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
        initial_sidebar_state="collapsed",  # Can be "auto", "expanded", "collapsed"
        page_icon="📚"
    )

    st.markdown("<h1 style='text-align: center;'>Profile</h1>", unsafe_allow_html=True)
    st.header("Here you can see your profile and make changes to it")
    st.write(f"You are logged as {username}")
    con = sqllite.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM USER WHERE username = ?", (username,))
    user = cur.fetchall()
    con.close()
    if user == []:
        st.error("Wrong username or password")
    else:
        user = user[0]
        id_valid = False
        with st.form("update_profile"):
            username_col, password_col, rol_col, identifier_col, birthdate_col = st.columns(5)
            with username_col:
                new_username = st.text_input("Username", value=user[0], key="username", disabled=True)
            with password_col:
                new_password = st.text_input("Password", value=user[1], key="password", type="password")
            with rol_col:
                st.text_input("Role", value=user[2], key="role", disabled=True)
            with birthdate_col:
                format = '%Y-%m-%d'
                date = datetime.strptime(user[3], format)
                new_date = st.date_input("Birthdate", key="birthdate", value=date)
            with identifier_col:
                new_id = st.text_input("DNI/NIF", value=user[4], key="identifier")
            if st.form_submit_button("Update profile"):
                st.write(new_username, new_password, new_date, new_id, username)
                pattern = re.compile("^[0-9]{8}[A-Z]$")
                id_valid = pattern.match(new_id)
                if id_valid:
                    con = sqllite.connect("database.db")
                    cur = con.cursor()
                    cur.execute("UPDATE USER SET  password = ?, birthdate = ?, id = ? WHERE username = ?",
                                (new_password, new_date, new_id, username))
                    con.commit()
                    con.close()
                    st.success("The details have been changed successfully")
                else:
                    st.error("The identifier is not valid, please enter a valid one")



            # Llamar a la funcion de cambio de cada una individualmente


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