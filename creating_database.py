import sqlite3 as sq

conn = sq.connect("EnglishDataBase.db")
c = conn.cursor()

c.execute(
    """CREATE TABLE english (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            word TEXT NOT NULL,
            meaning TEXT NOT NULL,
            remembering INTEGER NOT NULL,
            count INTEGER NOT NULL)"""
)

w = open("words.txt")
m = open("meanings.txt")

for word, meaning in zip([x.strip() for x in w], [y.strip() for y in m]):
    c.execute(
        "INSERT INTO english (word, meaning, remembering, count) VALUES (?, ?, ?, ?)",
        (word, meaning, 1, 0),
    )
    conn.commit()