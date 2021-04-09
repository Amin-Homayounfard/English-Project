import sqlite3 as sq
import subprocess
from os import remove

conn = sq.connect("EnglishDataBase.db")
c = conn.cursor()

from functions import *


while True:
    remembering_status = int(input("0: Ask not known words\n1: Ask new words\n"))

    random_words_by_remembering_status(remembering_status, 10)
    if remembering_status == 1:
        not_remembering_words = list(
            map(
                int,
                input("Not known words [IDs]: ").split(),
            )
        )
        if len(not_remembering_words) != 0:
            string = ""
            for id in not_remembering_words:
                update_remembering_status(
                    random_words_by_remembering_status.ids[id - 1], 0
                )
                for word in get_word_by_ID(
                    random_words_by_remembering_status.ids[id - 1]
                ):
                    string += word + "\n"
            with open("not_remembering_words.txt", "w") as nr:
                nr.write(string)
            subprocess.Popen("not_remembering_words.txt", shell=True)
    elif remembering_status == 0:
        remembering_words = list(
            map(
                int,
                input("Known words [IDs]: ").split(),
            )
        )
        for id in remembering_words:
            update_remembering_status(random_words_by_remembering_status.ids[id - 1], 1)
        not_remembering_words = list(
            set([i for i in range(1, len(random_words_by_remembering_status.ids) + 1)])
            - set(remembering_words)
        )
        if len(not_remembering_words) != 0:
            string = ""
            for id in not_remembering_words:
                for word in get_word_by_ID(
                    random_words_by_remembering_status.ids[id - 1]
                ):
                    string += word + "\n"
            with open("not_remembering_words.txt", "w") as nr:
                nr.write(string)
            subprocess.Popen("not_remembering_words.txt", shell=True)
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
