import pick
import sqlite3 as sql

def add_books():
    con = sql.connect("database.db")
    cur = con.cursor()
    sql = 'INSERT INTO AVAILABLE_BOOKS (BOOK_ID, BOOK_NAME, AUTHOR_NAME, PUBLICATION_YEAR, PAGE_COUNT) values(?, ?, ?, ?, ?)'
    data = [
        [1, "The Great Gatsby", "F. Scott Fitzgerald", 1925, 180],
        [2, "To Kill a Mockingbird", "Harper Lee", 1960, 281],
        [3, "1984", "George Orwell", 1949, 328],
        [4, "Pride and Prejudice", "Jane Austen", 1813, 432],
        [5, "The Hobbit", "J.R.R. Tolkien", 1937, 310],
        [6, "The Catcher in the Rye", "J.D. Salinger", 1951, 277],
        [7, "The Lord of the Rings", "J.R.R. Tolkien", 1954, 1178],
        [8, "Harry Potter and the Sorcerer's Stone", "J.K. Rowling", 1997, 309],
        [9, "The Da Vinci Code", "Dan Brown", 2003, 454],
        [10, "Moby-Dick", "Herman Melville", 1851, 635],
        [11, "The Great Gatsby", "F. Scott Fitzgerald", 1925, 180],
        [12, "To Kill a Mockingbird", "Harper Lee", 1960, 281],
        [13, "1984", "George Orwell", 1949, 328],
        [14, "Pride and Prejudice", "Jane Austen", 1813, 432],
        [15, "The Hobbit", "J.R.R. Tolkien", 1937, 310],
        [16, "The Catcher in the Rye", "J.D. Salinger", 1951, 277],
        [17, "The Lord of the Rings", "J.R.R. Tolkien", 1954, 1178],
        [18, "Harry Potter and the Sorcerer's Stone", "J.K. Rowling", 1997, 309],
        [19, "The Da Vinci Code", "Dan Brown", 2003, 454],
        [20, "Moby-Dick", "Herman Melville", 1851, 635],
        [21, "The Great Gatsby", "F. Scott Fitzgerald", 1925, 180],
        [22, "To Kill a Mockingbird", "Harper Lee", 1960, 281],
        [23, "1984", "George Orwell", 1949, 328],
        [24, "Pride and Prejudice", "Jane Austen", 1813, 432],
        [25, "The Hobbit", "J.R.R. Tolkien", 1937, 310],
        [26, "The Catcher in the Rye", "J.D. Salinger", 1951, 277],
        [27, "The Lord of the Rings", "J.R.R. Tolkien", 1954, 1178],
        [28, "Harry Potter and the Sorcerer's Stone", "J.K. Rowling", 1997, 309],
        [29, "The Da Vinci Code", "Dan Brown", 2003, 454],
        [30, "Moby-Dick", "Herman Melville", 1851, 635],
        [31, "The Great Gatsby", "F. Scott Fitzgerald", 1925, 180],
        [32, "To Kill a Mockingbird", "Harper Lee", 1960, 281],
        [33, "1984", "George Orwell", 1949, 328],
        [34, "Pride and Prejudice", "Jane Austen", 1813, 432],
        [35, "The Hobbit", "J.R.R. Tolkien", 1937, 310],
        [36, "The Catcher in the Rye", "J.D. Salinger", 1951, 277],
        [37, "The Lord of the Rings", "J.R.R. Tolkien", 1954, 1178],
        [38, "Harry Potter and the Sorcerer's Stone", "J.K. Rowling", 1997, 309],
        [39, "The Da Vinci Code", "Dan Brown", 2003, 454],
        [40, "Moby-Dick", "Herman Melville", 1851, 635],
    ]
    with con:
        con.executemany(sql, data)
    con.commit()
    print(data)

def add_users():
    print("Nada")

options = ["add_books", "add_users"]
option, index = pick.pick(options, "Title", indicator='=>', default_index=0)
exec(option+"()")