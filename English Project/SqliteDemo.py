import sqlite3 as sq
import subprocess
from os import remove

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
    for item in c.fetchall():
        print("ID:", item[0])
        print("Word:", item[1])
        with conn:
            c.execute("UPDATE english SET count = count + 1 WHERE id = ?", (item[0],))


while True:
    remembering_status = int(
        input(
            "Enter 0 if you want to measure the recall of words"
            + " you did not know the meaning of before, and enter 1 if"
            + " you want to measure the recall of new words: "
        )
    )

    random_words_by_remembering_status(remembering_status, 10)
    if remembering_status == 1:
        not_remembering_words = list(
            map(
                int,
                input(
                    """Please enter the ID of words that you do not remember the meaning of with a space: """
                ).split(),
            )
        )
        if len(not_remembering_words) != 0:
            string = ""
            for id in not_remembering_words:
                update_remembering_status(id, 0)
                for word in get_word_by_ID(id):
                    string += word + "\n"
            with open("not_remembering_words.txt", "w") as nr:
                nr.write(string)
            subprocess.Popen("not_remembering_words.txt", shell=True)
    elif remembering_status == 0:
        remembering_words = list(
            map(
                int,
                input(
                    """Please enter the ID of the words you remember the meaning of with a space: """
                ),
            )
        )
        for id in remembering_words:
            update_remembering_status(id, 1)
    else:
        print("Invalid input!")
        break

    continue_status = input("continue? (y/n): ")
    if continue_status == "y":
        pass
    elif continue_status == "n":
        break
    else:
        print("Invalid input!")
        break


conn.close()
