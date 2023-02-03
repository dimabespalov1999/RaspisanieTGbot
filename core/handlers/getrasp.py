import datetime
from raspis_bot import bot
from aiogram import Router

from aiogram.filters.command import Command
from aiogram.types import Message, ReplyKeyboardRemove
from core.utils.dbconnect import finduser, getrasp, getusers

router = Router()


async def makemsg(data):
    msg = []
    rasp = {}
    datelist = []
    listdata = list(map(lambda x: list(x), data))

    for i in listdata:
        date, time = i[2].split('T', 1)
        datelist.append(date)

    for k in datelist:
        rasp[k] = []

    for i in listdata:
        for k in rasp:
            if k in i[2]:
                rasp[k].append(i)

    for k in rasp:
        msgitem = []
        msgitem.append("""
<u><i><b>\U0001F538\U0001F538\U0001F538 ДАТА: {}\U0001F538\U0001F538\U0001F538</b></i></u>
""".format(k))
        for i in rasp[k]:
            txt = """
<i><b>Начало - Конец пары:</b></i> {} - {}
<i><b>Пара:</b></i> <u>{}</u>
<i><b>Преподователь:</b></i> {}
<i><b>Аудитория:</b></i> {}
""".format(i[1], i[3], i[6], i[7], i[8], )
            msgitem.append(txt)

        msg.append(' '.join(msgitem))
    return msg

async def sendraspmsg(user:str, first:str, last:str):
    data = await getrasp(user, first, last)
    msg = await makemsg(data)
    for i in range(0, len(msg), 2):
        txt = msg[i:i + 2]
        txt1 = ' '.join(txt)
        await bot.send_message(user,text=txt1,reply_markup=ReplyKeyboardRemove)


async def raspnxtdy():
    data = await getusers()
    users = []
    data = list(map(lambda x: list(x) , data))
    now = datetime.datetime.now().date()
    delta = now + datetime.timedelta(3)
    first = str(now) + 'T00:00:00'
    last = str(delta) + 'T00:00:00'
    msg = """
<u><i><b>\U0001F538\U0001F538\U0001F538\U0001F538\U0001F538\U0001F538\U0001F538\U0001F538\U0001F538

Расписание на завтра

\U0001F538\U0001F538\U0001F538\U0001F538\U0001F538\U0001F538\U0001F538\U0001F538\U0001F538</b></i></u>
"""

    for i in data:
        users.append(i[0])
    for user in users:
        await bot.send_message(user, text=msg)
        await sendraspmsg(user, first, last)
        print('отправил всем сообщение')


@router.message(Command(commands=['getrasp']))
async def cmd_getrasp(message: Message):
    user = await finduser(message.from_user.id)

    if user is True:
        now = datetime.datetime.now().date()
        delta = now + datetime.timedelta(10)
        first = str(now) + 'T00:00:00'
        last = str(delta) + 'T00:00:00'

        await sendraspmsg(message.from_user.id, first, last)

    else:
        await message.answer(text="Твой аккаунт не найден, пройди регистрацию нажав комманду /reg",
                             reply_markup=ReplyKeyboardRemove)
