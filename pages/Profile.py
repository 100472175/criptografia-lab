import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from database_importer import delete_user

def logged_in_profile():
    st.set_page_config(
        page_title="Log In",
        layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
        initial_sidebar_state="collapsed",  # Can be "auto", "expanded", "collapsed"
        page_icon="📚"
    )

    st.markdown("<h1 style='text-align: center;'>Profile</h1>", unsafe_allow_html=True)








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