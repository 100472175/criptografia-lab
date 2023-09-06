import streamlit as st
from cryptography.fernet import Fernet

st.set_page_config(
    page_title="Páginda de administración de bibliotecas Madrid",
	layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
	initial_sidebar_state="collapsed",  # Can be "auto", "expanded", "collapsed"
	page_icon="media/logo.png",  # String, anything supported by st.image, or None.
)


st.title("Encryption and Decryption")
st.header("Encrypt and Decrypt your text")
st.write("Enter your text below and click on Encrypt to encrypt your text. Click on Decrypt to decrypt your text.")