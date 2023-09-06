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
