import sqlite3 as sq

conn = sq.connect("EnglishDataBase.db")
c = conn.cursor()


def update_remembering_status(theID, remembering_status):
    with conn:
        c.execute(
            "UPDATE english SET remembering = :a WHERE id = :b",
            {"a": remembering_status, "b": theID},
        )


def get_word_by_ID(Id):
    c.execute("SELECT word,meaning FROM english WHERE id = ?", (Id,))
    for item in c.fetchall():
        yield item[0] + "\n" + item[1]


def get_word_by_remembering_status(remembering_status):
    c.execute("SELECT * FROM english WHERE remembering = ?", (remembering_status,))
    return c.fetchall()


def insert_new_word(word, meaning, remembering=1):
    with conn:
        c.execute("INSERT INTO english VALUES (?, ?, ?)", (word, meaning, remembering))


def delete_word(theword):
    with conn:
        c.execute("DELETE FROM english WHERE word =?", (theword,))


def print_database():
    for row in c.execute("SELECT * FROM english"):
        print("ID:", row[0])
        print("Word:", row[1])
        print("Meaning:", row[2])
        print("Remembering:", row[3])
        print("Count:", row[4])


def table_info():
    c.execute("PRAGMA TABLE_INFO(english)")
    return c.fetchall()


def add_new_column(column_name, column_type):
    with conn:
        c.execute("ALTER TABLE english ADD COLUMN " + column_name + column_type)


def random_words_by_remembering_status(remembering_status, limit):
    c.execute(
        "SELECT id,word FROM english WHERE remembering = ? ORDER BY count ASC,random() LIMIT "
        + str(limit),
        (remembering_status,),
    )
    random_words_by_remembering_status.ids = []
    for i, item in enumerate(c.fetchall(), 1):
        random_words_by_remembering_status.ids.append(item[0])
        print(i, ". ", item[1], sep="")
        with conn:
            c.execute("UPDATE english SET count = count + 1 WHERE id = ?", (item[0],))