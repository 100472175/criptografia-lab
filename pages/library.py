import base64
from pathlib import Path
import streamlit as st
from st_clickable_images import clickable_images
from streamlit_extras.switch_page_button import switch_page
import sqlite3 as sql  # Igual se puede borrar
from database_importer import *
from cryptography.fernet import Fernet
from time import sleep
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
    col_1, _, _, _, col_2 = st.columns(5)
    with col_1:
        st.title("The Library")
    with col_2:
        images = []
        file = os.path.join(os.getcwd(), "images/ajustes.png")
        with open(file, "rb") as image:
            encoded = base64.b64encode(image.read()).decode()
            images.append(f"data:image/jpeg;base64,{encoded}")
        clicked = clickable_images(
            images,
            div_style={"display": "flex", "justify-content": "left", "flex-wrap": "wrap"},
            img_style={"margin": "5px", "height": "40px"},
        )
        if clicked > -1:
            switch_page("Profile")
        st.write(f"You are logged as {username}")

    st.subheader("Welcome to the library, here you can see the books available and make reservations on them")
    col_books, col_reservation = st.columns(2)
    with col_books:
        with st.form("Book_reservation"):
            non_reservable = False
            st.header("Books")
            st.write("Here you can see the books available in the library")
            books = get_reserved_books(None)
            number_books = get_reserved_books(username)

            st.write(f"You have {len(number_books)} reservations")
            if len(books) == 0 or len(number_books) >= 3:
                non_reservable = True
                st.warning("You can't make more reservations")
            else:
                non_reservable = False

            book_selection = st.selectbox("Select a book you want to make the reservation on:", books,
                                          format_func=lambda book_individual: book_individual[1])
            submitted = st.form_submit_button("Select your book", disabled=non_reservable)
            if submitted:
                st.write(
                    f"Your book is {book_selection[1]}, it is from {book_selection[2]} book and "
                    f"it has {book_selection[4]} pages")
                reserve_book(username, book_selection[0])
                st.success("Your reservation has been made")
                sleep(0.5)
                switch_page("Library")

    with col_reservation:
        st.header(f"{'Current'} Reservations")
        # Here, the reservations the user has already made are shown (max 3)
        books_reserved = get_reserved_books(username)
        # books_reserved = execute_sql_command("SELECT * FROM AVAILABLE_BOOKS WHERE RESERVED = ?", (username,))
        c1, c2 = st.columns(2)
        for book in books_reserved:
            with c1:
                st.markdown("- " + book[1])
            with c2:
                if st.button("Cancel Reservation", key=str(book[0])):
                    execute_sql_command("UPDATE AVAILABLE_BOOKS SET RESERVED = ? WHERE BOOK_ID = ?", ("0", book[0]))
                    st.success("Your reservation has been successfully cancelled")
                    switch_page("Library")

################################################
############# ADMINISTRATOR ####################
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
            list_books, manage_books = st.columns(2)

            with list_books:
                st.write("Here you can see the books available in the library")
                books = get_all_books()
                st.write(books[-1][0])
                st.table(i for i in books)
            with manage_books:
                with st.form("Add a new book"):
                    st.header("Add a new book to the library")
                    book_name = st.text_input("Name")
                    author_name = st.text_input("Author")
                    pub_year = st.text_input("Publication year")
                    pages = st.text_input("Nº of pages")
                    submitted = st.form_submit_button("Add the book")

                    if submitted:
                        # Versión Edu:
                        try:
                            add_book(book_name, author_name, pub_year, pages)
                            st.success(f"{book_name} is now available in the library")
                            sleep(1)
                            switch_page("Library")
                        except ValueError as e:
                            st.warning(e)


                with st.form("Remove a book"):
                    st.header("Remove a book from the library")
                    book_name = st.text_input("Name")
                    publication_year = st.text_input("Publication year")
                    submitted = st.form_submit_button("Remove the book")
                    if submitted:
                        try:
                            remove_book(book_name, int(publication_year))
                            st.success(f"{book_name} has been removed from the library")
                            sleep(1)
                            switch_page("Library")
                        except ValueError as e:
                            st.warning(e)



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
                    number_admins = execute_sql_command("SELECT COUNT(*) FROM USER WHERE role = 'admin'", None)
                    if number_admins[0][0] > 1:
                        multiple_admins = True
                    else:
                        multiple_admins = False
                        st.warning("You can't remove the last admin")

                    st.header("Delete someone's admin")
                    st.write("Here you can remove someone admin, knowing their unique username")
                    username_to_remove_admin = st.text_input("Username")
                    submitted = st.form_submit_button("Remove admin", disabled=not multiple_admins)
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
    role = execute_sql_command("SELECT role FROM USER WHERE username = ?", (username,))
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

b = """
                        # Verify data is correct by checking if pub_year and pages are numbers
                        try:
                            pub_year = int(pub_year)
                            pages = int(pages)
                        except ValueError:
                            st.warning("Publication year and pages must be numbers")
                            sleep(1)
                            switch_page("Library")

                        # Check if the book is already in the library
                        if execute_sql_command("SELECT * FROM AVAILABLE_BOOKS WHERE BOOK_NAME = ? AND PUBLICATION_YEAR = ?", (book_name, pub_year)) != []:
                            st.warning("The book is already in the library")
                            sleep(1)
                            switch_page("Library")

                        execute_sql_command("INSERT INTO AVAILABLE_BOOKS (BOOK_ID, BOOK_NAME, AUTHOR_NAME, PUBLICATION_YEAR, PAGE_COUNT, RESERVED) values(?, ?, ?, ?, ?, ?)", (books[-1][0]+1, book_name, author_name, pub_year, pages, "0"))
                        st.success(f"{book_name} is now available in the library")
                        sleep(1)
                        switch_page("Library")"""