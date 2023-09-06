import sqlite3 as sql

con = sql.connect ("new_file.db")
cur = con.cursor()
#cur.execute("DROP TABLE prueba")
cur.execute("CREATE TABLE prueba(name, edad)")


for i in range(10):
    cur.execute("INSERT INTO prueba values (" + str(i) + ", " + str(i+1) + ")")


res = cur.execute("SELECT * FROM prueba")
print(res.fetchall())