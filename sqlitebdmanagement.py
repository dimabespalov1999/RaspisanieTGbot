import sqlite3
from config import path_db

def connectdb(func):
    def output(*args):
        try:
            connect = sqlite3.connect(path_db)
            cursor = connect.cursor()
            func(*args, cursor)
            connect.commit()
        except Exception as e:
            print(e)
    return output