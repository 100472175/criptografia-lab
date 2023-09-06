import streamlit as st

st.set_page_config(
    page_title="Log In",
	layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
	initial_sidebar_state="collapsed",  # Can be "auto", "expanded", "collapsed"
)

st.markdown("<h1 style='text-align: center;'>Log In</h1>", unsafe_allow_html=True)
st.header("Please state your, username and password in order to access your account")
col_1, col_2 = st.columns(2)
with col_1:
	st.write("If you don't have an account please register using the following link")
with col_2:
	st.button("Register Now!")
import streamlit as st
