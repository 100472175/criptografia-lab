from cryptography.fernet import Fernet
import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.title("The Library")

books = [
    {"title": "The Great Gatsby", "genre": "Fiction","publication_year":1990 "length": 180},
    {"title": "To Kill a Mockingbird", "genre": "Fiction", "length": 281},
    {"title": "1984", "genre": "Science Fiction", "length": 328},
    {"title": "Pride and Prejudice", "genre": "Romance", "length": 432},
    {"title": "The Hobbit", "genre": "Fantasy", "length": 310},
    {"title": "The Catcher in the Rye", "genre": "Fiction", "length": 277},
    {"title": "The Lord of the Rings", "genre": "Fantasy", "length": 1178},
    {"title": "Harry Potter and the Sorcerer's Stone", "genre": "Fantasy", "length": 309},
    {"title": "The Da Vinci Code", "genre": "Mystery", "length": 454},
]



col_books, col_reservation = st.columns(2)
with col_books:
    with st.form("Book_reservation"):
        st.header("Books")
        st.write("Here you can see the books available in the library")
        book_selection = st.selectbox("Select a book you want to make the reservation on:", books, format_func=lambda book: book["title"])
        submitted = st.form_submit_button("Select your book")
        if submitted:
            st.write(f"Your book is {book_selection['title']}, it is a {book_selection['genre']} book and it has {book_selection['length']} pages")


with col_reservation:
    st.header(f"{'User'} Reservations")
    # Here, the reservations the user has already made are shown
    #