import base64
from pathlib import Path
import streamlit as st
from st_clickable_images import clickable_images
from streamlit_extras.switch_page_button import switch_page
import sqlite3 as sql
from cryptography.fernet import Fernet
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
        images = []
        file = os.path.join(os.getcwd(), "images/ajustes.png")
        with open(file, "rb") as image:
            encoded = base64.b64encode(image.read()).decode()
            images.append(f"data:image/jpeg;base64,{encoded}")
        clicked = clickable_images(
            images,
            div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
            img_style={"margin": "5px", "height": "40px"},
        )
        if clicked > -1:
            switch_page("Profile")

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

################################################
################ ADMINISTRATOR #################
################################################

def draw_admin():
    st.subheader(f"You are logged as administrator, {username}")
    tab_normal, tab_admin = st.tabs(["Normal", "Administrator"])
    with tab_normal:
        draw_normal()
    with tab_admin:
        st.subheader("Administrator Panel")
        st.write("Here you can see the administrator panel")


        tab_books, tab_privileges = st.tabs(["Books", "Privileges"])
        with tab_books:
            st.subheader("Books")
            st.write("Here you can see the books available in the library, add some, modify them or delete them")

        with tab_privileges:
            col_make_admin, col_remove_admin = st.columns(2)
            with col_make_admin:
                with st.form("make_admin"):
                    st.header("Make someone admin")
                    st.write("Here you can make someone admin, knowing their unique username")
                    username_to_admin = st.text_input("Username")
                    submitted = st.form_submit_button("Make admin")
                    if submitted:
                        con = sql.connect("database.db")
                        cur = con.cursor()
                        if cur.execute('SELECT * FROM USER WHERE username = ?', (username_to_admin,)).fetchall() != []:
                            cur.execute("UPDATE USER SET role = 'admin' WHERE username = ?", (username_to_admin,))
                            con.commit()
                            con.close()
                            st.success(f"{username_to_admin} is now admin")
                        else:
                            st.warning(f"This user {username_to_admin} doesn't exist")
            with col_remove_admin:
                with st.form("remove_admin"):
                    con = sql.connect("database.db")
                    cur = con.cursor()
                    number_admins = cur.execute("SELECT COUNT(*) FROM USER WHERE role = 'admin'").fetchall()
                    if number_admins[0][0] > 1:
                        multiple_admins = True
                    else:
                        multiple_admins = False
                        st.warning("You can't remove the last admin")
                    con.close()
                    st.header("Delete someone's admin")
                    st.write("Here you can remove someone admin, knowing their unique username")
                    username_to_remove_admin = st.text_input("Username")
                    submitted = st.form_submit_button("Remove admin", disabled=not(multiple_admins))
                    if submitted:
                        con = sql.connect("database.db")
                        cur = con.cursor()
                        if cur.execute('SELECT * FROM USER WHERE username = ?', (username_to_remove_admin,)).fetchall() != []:
                            cur.execute("UPDATE USER SET role = 'normal' WHERE username = ?", (username_to_remove_admin,))
                            con.commit()
                            con.close()
                            st.success(f"{username_to_remove_admin} is now normal user")


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


