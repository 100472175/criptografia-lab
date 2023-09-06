import streamlit as st

st.set_page_config(
    page_title="Log In",
	layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
	initial_sidebar_state="collapsed",  # Can be "auto", "expanded", "collapsed"
)
col_1, col_2 = st.columns(2)
with col_1:
	with st.form("log_in_form"):
		st.markdown("<h1 style='text-align: center;'>Log In</h1>", unsafe_allow_html=True)
		st.header("Please state your, username and password in order to access your account")
		username = st.text_input("Username")
		password = st.text_input("Password")
		col_3,_,col_4= st.columns(3)
		with col_3:
			submitted = st.form_submit_button("Log In")
			if submitted:
				#autentificar
				pass
				#Redirigir a la pagina principal
		with col_4:
			f_password = st.form_submit_button("Forgot the password")
with col_2:
	with st.form("register_form"):
		st.markdown("<h1 style='text-align: center;'>Register Now</h1>", unsafe_allow_html=True)
		st.header("In case you don't have an account, please fill this forum to create one.")
		username_r = st.text_input("State your Username")
		password_r = st.text_input("State your Password")
		birthdate = st.date_input("Birthdate")
		identifier = st.text_input("DNI/NIF")
		submitted = st.form_submit_button("Register")
		if submitted:
			# autentificar
			pass
			# Redirigir a la pagina principal

