import sqlite3 as sql

con = sql.connect("new_file.db")
cur = con.cursor()
cur.execute("DROP TABLE prueba")
cur.execute("CREATE TABLE prueba(name, edad)")

for i in range(100):
    cur.execute("INSERT INTO prueba VALUES(" +str(i)+", "+ str(i+2) + ")")
# cur.execute("COMMIT")
res = cur.execute("SELECT * FROM prueba")
print(res.fetchall())
