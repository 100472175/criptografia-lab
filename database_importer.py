import re
import sqlite3 as sqllite
from crypto_settings import CryptoSettings


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
    return execute_sql_command("SELECT * FROM AVAILABLE_BOOKS ORDER BY (BOOK_ID)", None)


def get_reserved_books(username= '0'):
    if username is None:
        username = '0'
    return execute_sql_command("SELECT * FROM AVAILABLE_BOOKS WHERE RESERVED = ?", (username,))


def reserve_book(username, book_id):
    execute_sql_command("UPDATE AVAILABLE_BOOKS SET RESERVED = ? WHERE BOOK_ID = ?", (username, book_id))


def remove_book(name: str, year: str):
    if execute_sql_command("DELETE FROM AVAILABLE_BOOKS WHERE BOOK_NAME = ? AND PUBLICATION_YEAR = ?", (name, year)) == []:
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
        (empty_id, book_name, author, year, pages, '0', ))


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
    password, salt = CryptoSettings().encode(password)

    # Add user to database
    rol = "normal"
    con = sqllite.connect("database.db")
    sql = 'INSERT INTO USER (username,password,role,birthdate,id,salt) values (?, ?, ?, ?, ?, ?)'
    data = [user, password, rol, birthdate, user_id, salt]
    with con:
        con.execute(sql, data)
    con.commit()


def delete_user(user):
    execute_sql_command("DELETE FROM USER WHERE username = ?", (user,))


def change_username(user, old_username):
    execute_sql_command("UPDATE USER SET username = ? WHERE username = ?", (user, old_username))


def change_password(user, password):
    execute_sql_command("UPDATE USER SET password = ? WHERE username = ?", (password, user))


"""
import pick
options = ["add_books", "add_users"]
option, index = pick.pick(options, "Title", indicator='=>', default_index=0)
exec(option + "()")
"""
