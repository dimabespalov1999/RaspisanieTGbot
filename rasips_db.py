import sqlite3

conn = sqlite3.connect("bot.db")  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()


# cursor.execute("""
# CREATE TABLE Groups(
#         id INTEGER,
#         name TEXT UNIQUE,
#         kurs INTEGER,
#         facul TEXT,
#         group_id INTEGER NOT NULL UNIQUE,
#         PRIMARY KEY("id" AUTOINCREMENT));""")
# cursor.execute("""CREATE TABLE User_tg(
#         id INTEGER,
#         user_id BIGINT UNIQUE,
#         group_id INTEGER NOT NULL,
#         FOREIGN KEY (group_id) REFERENCES Groups(group_id),
#         PRIMARY KEY("id" AUTOINCREMENT));""")
cursor.execute("""CREATE TABLE Raspis(
        id INTEGER,
        start_time TEXT,
        start_date TEXT,
        stop_time TEXT,
        number_date INTEGER,
        day_week TEXT,
        discipline TEXT,
        prepod TEXT,
        audit TEXT,
        group_id INTEGER NOT NULL,
        update_day TEXT,
        PRIMARY KEY ("id"),
        FOREIGN KEY (group_id) REFERENCES Groups(group_id));""")
conn.commit()
