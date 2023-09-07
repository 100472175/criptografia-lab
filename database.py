import sqlite3 as sql

con = sql.connect("database.db")
cur = con.cursor()
#cur.execute("DROP TABLE USER")
cur.execute("""
     CREATE TABLE USER (
     username VARCHAR(100) NOT NULL PRIMARY KEY,
     password VARCHAR(100),
     role VARCHAR(100),
     age INTEGER
     );
     """)

cur.execute("""
    CREATE TABLE AVAILABLE_BOOKS(
    BOOK_ID INT NOT NULL PRIMARY KEY,
    BOOK_NAME VARCHAR(100) NOT NULL,
    AUTHOR_NAME VARCHAR(100) NOT NULL,
    PUBLICATION_YEAR INT NOT NULL,
    PAGE_COUNT INT NOT NULL,
    AVAILABLE VARCHAR(100)
    );
""")

res = cur.execute("SELECT * FROM USER")
print(res.fetchall())
