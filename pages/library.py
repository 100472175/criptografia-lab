from cryptography.fernet import Fernet
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import sqlite3 as sql

st.title("The Library")

books = [
    {"title": "The Great Gatsby", "genre": "Fiction","publication_year":1990, "length": 180, "reserved": "paco"},
    {"title": "To Kill a Mockingbird", "genre": "Fiction", "length": 281, "reserved": False},
    {"title": "1984", "genre": "Science Fiction", "length": 328, "reserved": False},
    {"title": "Pride and Prejudice", "genre": "Romance", "length": 432, "reserved": False},
    {"title": "The Hobbit", "genre": "Fantasy", "length": 310, "reserved": False},
    {"title": "The Catcher in the Rye", "genre": "Fiction", "length": 277, "reserved": False},
    {"title": "The Lord of the Rings", "genre": "Fantasy", "length": 1178, "reserved": False},
    {"title": "Harry Potter and the Sorcerer's Stone", "genre": "Fantasy", "length": 309, "reserved": False},
    {"title": "The Da Vinci Code", "genre": "Mystery", "length": 454, "reserved": False},
]



col_books, col_reservation = st.columns(2)
with col_books:
    with st.form("Book_reservation"):
        st.header("Books")
        st.write("Here you can see the books available in the library")
        # mirar como hacer para que no muestre los que esten reservados
        book_selection = st.selectbox("Select a book you want to make the reservation on:", books, format_func=lambda book: book["title"] if not book["reserved"] else book)
        submitted = st.form_submit_button("Select your book")
        if submitted:
            st.write(f"Your book is {book_selection['title']}, it is a {book_selection['genre']} book and it has {book_selection['length']} pages")


with col_reservation:
    st.header(f"{'Current'} Reservations")
    # Here, the reservations the user has already made are shown (max 3)

    #st.write("Your current reservations are:",books,format_func=lambda book: book["title"] if book["reserved"] == username else book)


con = sql.connect("database.db")
cur = con.cursor()
cur.execute("SELECT * FROM AVAILABLE_BOOKS WHERE AVAILABLE = '0'")
books = cur.fetchall()
# st.write(books)
con.close()
a = st.selectbox("Select a book you want to make the reservation on:", books, format_func=lambda book: book[1])
st.write(a)