import aiosqlite
import asyncio

async def connectdb():
    async with aiosqlite.connect("/home/bec/eclipse-workspace/Raspis_bot/bot.db") as cursor:
        return cursor
async def cursorexecute(sql, params):
    async with aiosqlite.connect("/home/bec/eclipse-workspace/Raspis_bot/bot.db") as cursor:
        await cursor.execute(sql, params)
        await cursor.commit()
        data = await cursor.execute_fetchall(sql)
        return data
async def insertdata(sql):
    async with aiosqlite.connect("/home/bec/eclipse-workspace/Raspis_bot/bot.db") as cursor:
        try:
            await cursor.execute(sql)
            await cursor.commit()
            return True
        except:
            return False



async def finduser(userid):
    async with aiosqlite.connect("/home/bec/eclipse-workspace/Raspis_bot/bot.db") as cursor:
        data = await cursor.execute_fetchall(f"""SELECT id FROM User_tg WHERE user_id = '{userid}'""")
        await cursor.commit()
        if len(data) == 1:
            return True
        else:
            return False

async def getusers():
    async with aiosqlite.connect("/home/bec/eclipse-workspace/Raspis_bot/bot.db") as cursor:
        data = await cursor.execute_fetchall(f"""SELECT user_id FROM User_tg""")
        await cursor.commit()
        return data

async def getgroupusr(userid):
    async with aiosqlite.connect("/home/bec/eclipse-workspace/Raspis_bot/bot.db") as cursor:
        data = await cursor.execute_fetchall(f"""SELECT group_id FROM User_tg WHERE user_id = '{userid}'""")
        await cursor.commit()
        data = list(data[0])
        return data


async def getrasp(userid,first_day, last_day): #2023-01-24T00:00:00/2023-01-32T00:00:00
    group = await getgroupusr(userid)
    async with aiosqlite.connect("/home/bec/eclipse-workspace/Raspis_bot/bot.db") as cursor:
        data = await cursor.execute_fetchall(f"""
        SELECT * FROM Raspis 
        WHERE 
        group_id = '{group[0]}' 
        AND start_date > '{first_day}' 
        AND start_date < '{last_day}' 
        ORDER BY start_date """)
        return data







        # data = await cursor.execute_fetchall(sql)
        # return data
# group = "299"
# user_id = '232323453'
# sql = """INSERT INTO User_tg(user_id) VALUES (?)"""
#
# params = (user_id,)
# asyncio.run(cursorexecute(sql,params))
