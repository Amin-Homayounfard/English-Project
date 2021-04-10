import sqlite3 as sq

conn = sq.connect("EnglishDataBase.db")
c = conn.cursor()

c.execute(
    """CREATE TABLE if NOT EXISTS english (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            word TEXT NOT NULL,
            meaning TEXT NOT NULL,
            remembering INTEGER NOT NULL,
            count INTEGER NOT NULL)"""
)

w = open("words.txt", "r+")
m = open("meanings.txt", "r+")

for word, meaning in zip([x.strip() for x in w], [y.strip() for y in m]):
    c.execute(
        "INSERT INTO english (word, meaning, remembering, count) VALUES (?, ?, ?, ?)",
        (word, meaning, 1, 0),
    )
    conn.commit()

w.truncate(0)
m.truncate(0)
w.close()
m.close()
