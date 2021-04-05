import sqlite3 as sq
import subprocess
from os import remove

conn = sq.connect("EnglishDataBase.db")
c = conn.cursor()


from functions import *


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
                ).split(),
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
