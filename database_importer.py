import re
import sqlite3 as sqllite
from crypto_settings import *


def execute_sql_command(function, parameters):
    con = sqllite.connect("database.db")
    cur = con.cursor()
    if parameters:
        cur.execute(function, parameters)
    else:
        cur.execute(function)
    data = cur.fetchall()
    con.commit()
    con.close()
    return data


def get_all_books():
    books = execute_sql_command("SELECT * FROM AVAILABLE_BOOKS ORDER BY (BOOK_ID)", None)
    for i in range(len(books)):
        books[i] = list(books[i])
        if books[i][5] not in (b'0', '0', 0):
            books[i][5] = decrypt_id(books[i][5])
        else:
            books[i][5] = "Libre"
    return books


def get_reserved_books(dni):
    if dni is None:
        dni = '0'
    return execute_sql_command("SELECT * FROM AVAILABLE_BOOKS WHERE RESERVED = ?", (dni,))


def get_id_from_username(username):
    return execute_sql_command("SELECT id FROM USER WHERE username = ?", (username,))


def reserve_book(dni, book_id):
    execute_sql_command("UPDATE AVAILABLE_BOOKS SET RESERVED = ? WHERE BOOK_ID = ?", (dni, book_id))


def remove_book(name: str, year: str):
    if execute_sql_command("DELETE FROM AVAILABLE_BOOKS WHERE BOOK_NAME = ? AND PUBLICATION_YEAR = ?",
                           (name, year)) == []:
        raise ValueError("The book does not exist in the library")


def get_latest_book_id():
    return execute_sql_command("SELECT MIN(BOOK_ID) + 1 AS first_missing_element "
                               "FROM AVAILABLE_BOOKS "
                               "WHERE BOOK_ID + 1 NOT IN (SELECT BOOK_ID FROM AVAILABLE_BOOKS)",
                               None)


def add_book(book_name: str, author: str, year: str, pages: str):
    # Check the year and pages are numbers
    try:
        year = int(year)
        pages = int(pages)
    except ValueError:
        raise ValueError("Publication year and pages must be numbers")

    # Check if the book is already in the library
    if execute_sql_command("SELECT * FROM AVAILABLE_BOOKS WHERE BOOK_NAME = ? AND PUBLICATION_YEAR = ?",
                           (book_name, year)) != []:
        raise ValueError("The book is already in the library")

    # Add the book to the library
    empty_id = get_latest_book_id()[0][0]
    # books = get_all_books()
    # execute_sql_command(
    #     "INSERT INTO AVAILABLE_BOOKS (BOOK_ID, BOOK_NAME, AUTHOR_NAME, PUBLICATION_YEAR, PAGE_COUNT, RESERVED) values(?, ?, ?, ?, ?, ?)",
    #     (int(books[-1][0]) + 1, book_name, author, year, pages, '0', ))
    execute_sql_command(
        "INSERT INTO AVAILABLE_BOOKS (BOOK_ID, BOOK_NAME, AUTHOR_NAME, PUBLICATION_YEAR, PAGE_COUNT, RESERVED) values(?, ?, ?, ?, ?, ?)",
        (empty_id, book_name, author, year, pages, '0',))


def add_users(user, password, birthdate, user_id):
    # Check the password is valid, it contains at lesat a special character:
    spacial_character = ['$', '#', '@', '!', '*']
    if not any(c in spacial_character for c in password):
        raise ValueError("Password does not contain a spacial character: " + str(spacial_character))
    if len(password) < 10:
        raise ValueError("Password is does not have the minimum length")
    # Check the id is valid
    user_id = user_id.upper()
    pattern = re.compile("^[0-9]{8}[A-Z]$|^[A-Z][0-9]{7}[A-Z]$")
    if not pattern.match(user_id):
        raise ValueError("The id does not math the spanish DNI/NIE format")

    # Encrypt the user and password
    cifrador = CryptoSettings()
    password, salt = cifrador.encode(password)

    # Cypher DNI
    user_id, nonce = check_ChaCha_id(user_id)


    # Add user to database
    rol = "normal"
    con = sqllite.connect("database.db")
    sql = 'INSERT INTO USER (username,password,role,birthdate,id,salt,nonce) values (?, ?, ?, ?, ?, ?, ?)'
    data = [user, password, rol, birthdate, user_id, salt, nonce]
    with con:
        con.execute(sql, data)
    con.commit()


def update_salt(user, password, salt):
    execute_sql_command("UPDATE USER SET PASSWORD = ?, SALT = ? WHERE USERNAME = ?", (password, salt, user))


def delete_user(user):
    execute_sql_command("DELETE FROM USER WHERE username = ?", (user,))
    execute_sql_command("UPDATE AVAILABLE_BOOKS SET RESERVED = ? WHERE RESERVED = ?", (0, user))


def change_username(user, old_username):
    execute_sql_command("UPDATE USER SET username = ? WHERE username = ?", (user, old_username))


def change_password(user, password, id, salt):
    execute_sql_command("UPDATE USER SET password = ?, salt = ? WHERE username = ? AND id = ?",
                        (password, salt, user, id))
