import aiosqlite
from config import path_db

async def connectdb():
    async with aiosqlite.connect(path_db) as cursor:
        return cursor
async def cursorexecute(sql, params):
    async with aiosqlite.connect(path_db) as cursor:
        await cursor.execute(sql, params)
        await cursor.commit()
        data = await cursor.execute_fetchall(sql)
        return data

async def insertdata(sql):
    async with aiosqlite.connect(path_db) as cursor:
        try:
            await cursor.execute(sql)
            await cursor.commit()
            return True
        except Exception as e:
            print(e)
            return False

async def finduser(userid):
    async with aiosqlite.connect(path_db) as cursor:
        data = await cursor.execute_fetchall(f"""SELECT id FROM User_tg WHERE user_id = '{userid}'""")
        await cursor.commit()
        if len(data) == 1:
            return True
        else:
            return False

async def getusers():
    async with aiosqlite.connect(path_db) as cursor:
        data = await cursor.execute_fetchall(f"""SELECT user_id FROM User_tg""")
        await cursor.commit()
        return data

async def getgroupusr(userid):
    async with aiosqlite.connect(path_db) as cursor:
        prep_stud = await cursor.execute_fetchall(f"""SELECT status FROM User_tg WHERE user_id = '{userid}'""")
        if 'prepod' in prep_stud[0]:
            data = await cursor.execute_fetchall(f"""SELECT prepod_id0, prepod_id1, prepod_id2, prepod_id3
                                                     FROM User_tg WHERE user_id = '{userid}'""")
        else:
            data = await cursor.execute_fetchall(f"""SELECT group_id FROM User_tg WHERE user_id = '{userid}'""")
        await cursor.commit()
        data = list(data[0])
        return data

async def get_prof(userid):
    async with aiosqlite.connect(path_db) as cursor:
        data = await cursor.execute_fetchall(f"""SELECT * FROM User_tg WHERE user_id = '{userid}'""")
        await cursor.commit()
        # print(data)
        return data

async def get_group_name(id:list[int]):
    async with aiosqlite.connect(path_db) as cursor:
        if len(id) == 4:
            data = await cursor.execute_fetchall(
                f"""SELECT name FROM Prepods WHERE prepod_id = '{id[0]}' OR prepod_id = '{id[1]}' OR prepod_id =  '{id[2]}' OR prepod_id = '{id[3]}' """)
        else:
            data = await cursor.execute_fetchall(f"""SELECT name, kurs, facul FROM Groups WHERE group_id = '{id[0]}'""")
        await cursor.commit()

        return data


async def log_event(userid, username, name, event, msg, date):
    async with aiosqlite.connect(path_db) as cursor:
        await cursor.execute(f"""INSERT INTO Logs(user_id, username, name, event, msg, date) VALUES(?, ?, ?, ?, ?, ?)""",
                             (userid, username, name, event, msg, date))
        await cursor.commit()

async def upd_last(userid, date):
    async with aiosqlite.connect(path_db) as cursor:
        await cursor.execute(f"""UPDATE User_tg SET last_date = '{date}' WHERE user_id = '{userid}' """)
        await cursor.commit()

async def getdate():
    async with aiosqlite.connect(path_db) as cursor:
        data = await cursor.execute_fetchall(f"""SELECT update_day FROM Raspis""")
        await cursor.commit()
        data = data[0][0]
        return data


async def getrasp(userid,first_day, last_day): #2023-01-24T00:00:00/2023-01-32T00:00:00
    group = await getgroupusr(userid)
    async with aiosqlite.connect(path_db) as cursor:
        prep_stud = await cursor.execute_fetchall(f"""SELECT status FROM User_tg WHERE user_id = '{userid}'""")
        if 'prepod' in prep_stud[0]:
            data = await cursor.execute_fetchall(
                f"""WITH tab1 AS(
                    SELECT * FROM Raspis LEFT JOIN Groups ON Raspis.group_id = Groups.group_id),
                    tab2 AS(
                    SELECT * FROM tab1
                    WHERE 
                    prepod_id = '{group[0]}'
                    or  prepod_id = '{group[1]}'
                    or  prepod_id = '{group[2]}'
                    or  prepod_id = '{group[3]}')
                    SELECT * FROM tab2
                    WHERE
                    start_date > '{first_day}' 
                    AND start_date < '{last_day}' 
                    ORDER BY start_date;
                """)
        else:
            data = await cursor.execute_fetchall(f"""
                   SELECT * FROM Raspis 
                   WHERE 
                   group_id = '{group[0]}' 
                   AND start_date > '{first_day}' 
                   AND start_date < '{last_day}' 
                   ORDER BY start_date """)
        await cursor.commit()
        return data
