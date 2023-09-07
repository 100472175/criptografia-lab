from cryptography.fernet import Fernet
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import sqlite3 as sql


# username = "Paco"
username = st.session_state["username"]
col_1, col_2 = st.columns(2)
with col_1:
    st.title("The Library")
with col_2:
    st.write(f"You are logged as {username}")
st.subheader("Welcome to the library, here you can see the books available and make reservations on them")
col_books, col_reservation = st.columns(2)
with col_books:
    with st.form("Book_reservation"):
        st.header("Books")
        st.write("Here you can see the books available in the library")
        # mirar como hacer para que no muestre los que esten reservados
        con = sql.connect("database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM AVAILABLE_BOOKS WHERE AVAILABLE = '0'")
        books = cur.fetchall()
        # st.write(books)
        con.close()
        book_selection = st.selectbox("Select a book you want to make the reservation on:", books, format_func=lambda book: book[1])
        submitted = st.form_submit_button("Select your book")
        if submitted:
            st.write(f"Your book is {book_selection['title']}, it is a {book_selection['genre']} book and it has {book_selection['length']} pages")


with col_reservation:
    st.header(f"{'Current'} Reservations")
    # Here, the reservations the user has already made are shown (max 3)
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM AVAILABLE_BOOKS WHERE AVAILABLE = ?", (username,))
    books_reserved = cur.fetchall()
    con.close()
    for book in books_reserved:
        st.markdown("- " + book[1])



    #st.write("Your current reservations are:",books,format_func=lambda book: book["title"] if book["reserved"] == username else book)

