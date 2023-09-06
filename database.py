import sqlite3 as sql

con = sql.connect("database.db")
cur = con.cursor()
#cur.execute("DROP TABLE USER")
cur.execute("""
     CREATE TABLE USER (
     username TEXT NOT NULL PRIMARY KEY,
     password TEXT,
     age INTEGER
     );
     """)

cur.execute("""
    CREATE TABLE AVAILABLE_BOOKS(
    BOOK_ID INT NOT NULL,
    BOOK_NAME VARCHAR(100) NOT NULL,
    AUTHOR_NAME VARCHAR(100) NOT NULL,
    PUBLICATION_YEAR INT NOT NULL,
    PAGE_COUNT INT NOT NULL,
    PRIMARY KEY(BOOK_ID)
    );
""")

res = cur.execute("SELECT * FROM USER")
print(res.fetchall())

if __name__ == "__main__":
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
        [9, "The Da Vinci Code", "Dan Brown", 2003, 454]
    ]
    with con:
        con.executemany(sql, data)
    con.commit()