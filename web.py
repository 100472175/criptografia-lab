import streamlit as st
from cryptography.fernet import Fernet
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title="Páginda de administración de bibliotecas Madrid",
	layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
	initial_sidebar_state="collapsed",  # Can be "auto", "expanded", "collapsed"
	page_icon="🧊",  # String, anything supported by st.image, or None.
)

with st.container():
	st.title("Encryption and Decryption")
	st.header("Encrypt and Decrypt your text")
	st.write("Enter your text below and click on Encrypt to encrypt your text. C"
			 "lick on Decrypt to decrypt your text.")
st.text("Hello World")
st.selectbox("Select a number", [1,2,3])
st.multiselect("Select a number", [1,2,3])
st.button("Click me")
st.checkbox("Check me out")
st.radio("Radio", [1,2,3])
st.slider("Slide me", min_value=0, max_value=10)
st.select_slider("Slide to select", options=[1,'2'])
st.text_input("Enter some text")
st.number_input("Enter a number")
st.text_area("Area for textual entry")
st.date_input("Date input")
st.time_input("Time entry")
col_1, col_2 = st.columns(2)
with col_1:
	st.text("This is column 1")
with col_2:
	st.text("This is column 2")

tab1, tab2 = st.tabs([":blue[Tab 1]", ":red[Tab 2]"])
with tab1:
	st.text("This is inside tab 1")
	st.write(f'''Hola, que tal?
		<a target="_self" href="http://localhost:8501">
			<button>
				Please login via Google
			</button>
		</a>
		''',
		unsafe_allow_html=True
	)

with tab2:
	st.text("This is inside tab 2")

if st.button("Switch to login page"):
	switch_page("Log In")