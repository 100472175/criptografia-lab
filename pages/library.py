import base64
from pathlib import Path

from cryptography.fernet import Fernet
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import sqlite3 as sql
import os


def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded_img = base64.b64encode(img_bytes).decode()
    return encoded_img

def draw_not_logged():
    st.subheader("You are not logged in, please log in or register")
    if st.button("Log In"):
        switch_page("Log In")


def draw_normal():
    col_1,_,_,_,col_2 = st.columns(5)
    with col_1:
        st.title("The Library")
    with col_2:
        st.write(f"You are logged as {username}")
        link = "\Profile"
        img_path = os.getcwd() + "\images\\ajustes.png"
        image_base64 = img_to_bytes(img_path)
        html = f"<a href='{link}'><img width='40' height='40' src='data:image/png;base64,{image_base64}'></a>"
        st.markdown(html, unsafe_allow_html=True)
    st.subheader("Welcome to the library, here you can see the books available and make reservations on them")
    col_books, col_reservation = st.columns(2)
    with col_books:
        with st.form("Book_reservation"):
            non_reservable = False
            st.header("Books")
            st.write("Here you can see the books available in the library")
            # mirar como hacer para que no muestre los que esten reservados
            con = sql.connect("database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM AVAILABLE_BOOKS WHERE RESERVED = '0'")
            books = cur.fetchall()

            cur.execute("SELECT COUNT(*) FROM AVAILABLE_BOOKS WHERE RESERVED = ?", (username,))
            number_books = cur.fetchall()
            con.close()
            st.write(f"You have {number_books[0][0]} reservations")

            if len(books) == 0 or number_books[0][0] >= 3:
                non_reservable = True
                st.warning("You can't make more reservations")
            else:
                non_reservable = False

            book_selection = st.selectbox("Select a book you want to make the reservation on:", books,
                                          format_func=lambda book: book[1])
            submitted = st.form_submit_button("Select your book", disabled=non_reservable)
            if submitted:
                st.write(
                    f"Your book is {book_selection[1]}, it is from {book_selection[2]} book and it has {book_selection[4]} pages")
                con = sql.connect("database.db")
                cur = con.cursor()
                cur.execute("UPDATE AVAILABLE_BOOKS SET RESERVED = ? WHERE BOOK_ID = ?", (username, book_selection[0]))
                con.commit()
                con.close()
                st.success("Your reservation has been made")


    with col_reservation:
        st.header(f"{'Current'} Reservations")
        # Here, the reservations the user has already made are shown (max 3)
        con = sql.connect("database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM AVAILABLE_BOOKS WHERE RESERVED = ?", (username,))
        books_reserved = cur.fetchall()
        con.close()
        for book in books_reserved:
            st.markdown("- " + book[1])

        # st.write("Your current reservations are:",books,format_func=lambda book: book["title"] if book["reserved"] == username else book)



def draw_admin():
    st.subheader(f"You are logged as administrator, {username}")
    tab_normal, tab_admin = st.tabs(["Normal", "Administrator"])
    with tab_normal:
        draw_normal()
    with tab_admin:
        st.subheader("Administrator Panel")
        st.write("Here you can see the administrator panel")

try:
    username = st.session_state["username"]

    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT role FROM USER WHERE username = ?", (username,))
    role = cur.fetchall()
    con.close()
    if role:
        role = role[0][0]
    if username == "":
        draw_not_logged()
    elif role == "admin":
        draw_admin()
    else:
        draw_normal()
except KeyError:
    draw_not_logged()


