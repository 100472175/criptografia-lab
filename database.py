import sqlite3 as sl
con = sl.connect('database.db')
with con:
    con.execute("""
     CREATE TABLE USER (
     username TEXT NOT NULL PRIMARY KEY,
     password TEXT
     
     );
     """)