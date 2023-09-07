import sqlite3 as sql

con = sql.connect("database.db")
cur = con.cursor()
cur.execute("DROP TABLE USER")
cur.execute("DROP TABLE AVAILABLE_BOOKS")
cur.execute("""
     CREATE TABLE USER (
     username VARCHAR(100) NOT NULL PRIMARY KEY,
     password VARCHAR(100),
     role VARCHAR(10),
     birthdate DATE,
     id CHAR(9) UNIQUE NOT NULL
     );
     """)

cur.execute("""
    CREATE TABLE AVAILABLE_BOOKS(
    BOOK_ID INT NOT NULL PRIMARY KEY,
    BOOK_NAME VARCHAR(100) NOT NULL,
    AUTHOR_NAME VARCHAR(100) NOT NULL,
    PUBLICATION_YEAR INT NOT NULL,
    PAGE_COUNT INT NOT NULL,
    RESERVED VARCHAR(100)
    );
""")

res = cur.execute("SELECT * FROM USER")
print(res.fetchall())
