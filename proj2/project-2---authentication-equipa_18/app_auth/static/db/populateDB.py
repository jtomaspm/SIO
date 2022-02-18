import sqlite3
from os import walk

DB_STRING = "shop.db"

def setup_database():
    sql_commands = open('shop.sql')
    result = ""
    with sqlite3.connect(DB_STRING) as con:
        for com in sql_commands:
            for ch in com:
                result += ch
                if ch == ';':
                    con.execute(result)
                    result = ""


def load_imgs_to_dg():
    filenames = next(walk('../img'), (None, None, []))[2]  # [] if no file
    print(filenames[0][0])
    with sqlite3.connect(DB_STRING) as con:
        for filename in filenames:
            i = filename[0]
            con.execute("UPDATE Game SET img_path = \"static/img/" + str(filename) + "\" WHERE id_game = " + i + ";")
