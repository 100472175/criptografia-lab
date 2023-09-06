import sqlite3 as sql

con = sql.connect ("new_file.db")
cur = con.cursor()
#cur.execute("DROP TABLE USER")
cur.execute("""
     CREATE TABLE USER (
     username TEXT NOT NULL PRIMARY KEY,
     password TEXT,
     age INTEGER
     );
     """)



res = cur.execute("SELECT * FROM USER")
print(res.fetchall())