import sqlite3 as sqllite
import re


def add_books():
    con = sqllite.connect("database.db")
    cur = con.cursor()
    sql = 'INSERT INTO AVAILABLE_BOOKS (BOOK_ID, BOOK_NAME, AUTHOR_NAME, PUBLICATION_YEAR, PAGE_COUNT, RESERVED) values(?, ?, ?, ?, ?, ?)'
    data = [
        [1, "The Great Gatsby", "F. Scott Fitzgerald", 1925, 180, "pedro"],
        [2, "To Kill a Mockingbird", "Harper Lee", 1960, 281, "anabel"],
        [3, "1984", "George Orwell", 1949, 328, "0"],
        [4, "Pride and Prejudice", "Jane Austen", 1813, 432, "0"],
        [5, "The Hobbit", "J.R.R. Tolkien", 1937, 310, "0"],
        [6, "The Catcher in the Rye", "J.D. Salinger", 1951, 277, "0"],
        [7, "The Lord of the Rings", "J.R.R. Tolkien", 1954, 1178, "0"],
        [8, "Harry Potter and the Sorcerer's Stone", "J.K. Rowling", 1997, 309, "0"],
        [9, "The Da Vinci Code", "Dan Brown", 2003, 454, "0"],
        [10, "Moby-Dick", "Herman Melville", 1851, 635, "0"],
        [11, "The Great Gatsby", "F. Scott Fitzgerald", 1925, 180, "0"],
        [12, "To Kill a Mockingbird", "Harper Lee", 1960, 281, "0"],
        [13, "1984", "George Orwell", 1949, 328, "0"],
        [14, "Pride and Prejudice", "Jane Austen", 1813, 432, "0"],
        [15, "The Hobbit", "J.R.R. Tolkien", 1937, 310, "0"],
        [16, "The Catcher in the Rye", "J.D. Salinger", 1951, 277, "0"],
        [17, "The Lord of the Rings", "J.R.R. Tolkien", 1954, 1178, "0"],
        [18, "Harry Potter and the Sorcerer's Stone", "J.K. Rowling", 1997, 309, "0"],
        [19, "The Da Vinci Code", "Dan Brown", 2003, 454, "0"],
        [20, "Moby-Dick", "Herman Melville", 1851, 635, "0"],
        [21, "The Great Gatsby", "F. Scott Fitzgerald", 1925, 180, "0"],
        [22, "To Kill a Mockingbird", "Harper Lee", 1960, 281, "0"],
        [23, "1984", "George Orwell", 1949, 328, "0"],
        [24, "Pride and Prejudice", "Jane Austen", 1813, 432, "0"],
        [25, "The Hobbit", "J.R.R. Tolkien", 1937, 310, "0"],
        [26, "The Catcher in the Rye", "J.D. Salinger", 1951, 277, "0"],
        [27, "The Lord of the Rings", "J.R.R. Tolkien", 1954, 1178, "0"],
        [28, "Harry Potter and the Sorcerer's Stone", "J.K. Rowling", 1997, 309, "0"],
        [29, "The Da Vinci Code", "Dan Brown", 2003, 454, "0"],
        [30, "Moby-Dick", "Herman Melville", 1851, 635, "0"],
        [31, "The Great Gatsby", "F. Scott Fitzgerald", 1925, 180, "0"],
        [32, "To Kill a Mockingbird", "Harper Lee", 1960, 281, "0"],
        [33, "1984", "George Orwell", 1949, 328, "0"],
        [34, "Pride and Prejudice", "Jane Austen", 1813, 432, "0"],
        [35, "The Hobbit", "J.R.R. Tolkien", 1937, 310, "0"],
        [36, "The Catcher in the Rye", "J.D. Salinger", 1951, 277, "0"],
        [37, "The Lord of the Rings", "J.R.R. Tolkien", 1954, 1178, "0"],
        [38, "Harry Potter and the Sorcerer's Stone", "J.K. Rowling", 1997, 309, "0"],
        [39, "The Da Vinci Code", "Dan Brown", 2003, 454, "0"],
        [40, "Moby-Dick", "Herman Melville", 1851, 635, "0"]
    ]
    with con:
        con.executemany(sql, data)
    con.commit()
    print(data)

def add_users(user, password, birthdate, id):
    # Check the password is valid, it contains at lesat a special character:
    spacial_character = ['$', '#', '@', '!', '*']
    if not any(c in spacial_character for c in password):
        raise ValueError("Password does not contain a spacial character: " + str(spacial_character))
    if len(password) < 10:
        raise ValueError("Password is does not have the minimum length")
    # Check the id is valid
    id = id.upper()
    pattern = re.compile("^[0-9]{8}[A-Z]$|^[A-Z][0-9]{7}[A-Z]")
    if not pattern.match(id):
        raise ValueError("The id does not math the spanish DNI/NIE format")

    rol = "normal"
    con = sqllite.connect("database.db")
    sql = 'INSERT INTO USER (username,password,role,birthdate,id) values (?, ?, ?, ?, ?)'
    data = [user, password, rol, birthdate, id]
    with con:
        con.execute(sql, data)
    con.commit()

def delete_user(user):
    con = sqllite.connect("database.db")
    cur = con.cursor()
    cur.execute("DELETE FROM USER WHERE username = ?", (user,))
    cur.fetchall()
    con.commit()
    con.close()

def change_username(user,old_username):
    con = sqllite.connect("database.db")
    cur = con.cursor()
    cur.execute("UPDATE USER SET username = ? WHERE username = ?", (user,old_username))
    cur.fetchall()
    con.commit()
    con.close()

def change_password(user,password):
    con = sqllite.connect("database.db")
    cur = con.cursor()
    cur.execute("UPDATE USER SET password = ? WHERE username = ?", (password,user))
    cur.fetchall()
    con.commit()
    con.close()
"""
import pick
options = ["add_books", "add_users"]
option, index = pick.pick(options, "Title", indicator='=>', default_index=0)
exec(option + "()")
"""