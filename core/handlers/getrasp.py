import asyncio
import datetime
import logging
import aiogram.exceptions
import requests
import config
from add_update_db import startupdate
from core.keyboards.meny import menu
from core.utils.messages import head_rasp_msg, date_rasp_msg, raspis_msg_students, raspis_msg_prepods, non_lessons, \
    check_update_msg
from raspis_bot import bot
from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message
from core.utils.dbconnect import finduser, getrasp, getusers, log_event, upd_last, getdate

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
        msgitem.append(date_rasp_msg.format(k))
        for i in rasp[k]:
            if len(i) == 12:
                msgitem.append(raspis_msg_students.format(i[1], i[3], i[6], i[7], i[9]))
            else:
                msgitem.append(raspis_msg_prepods.format(i[1], i[3], i[13], i[6], i[7], i[9]))

        msg.append(' '.join(msgitem))
    return msg


async def sendraspmsg(user: str, first: str, last: str):
    data = await getrasp(user, first, last)
    if len(data) != 0:
        msg = await makemsg(data)
        for i in range(0, len(msg), 1):
            txt = msg[i:i + 1]
            txt1 = ' '.join(txt)
            try:
                await bot.send_message(user, text=txt1, reply_markup=await menu())
            except aiogram.exceptions.TelegramForbiddenError:
                logging.basicConfig(level=logging.WARNING,
                                    format="%(asctime)s - [%(levelname)s] - %(name)s "
                                           "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
    else:
        await bot.send_message(user, text=non_lessons, reply_markup=await menu())





async def raspnxtdy():
    data = await getusers()
    users = []
    data = list(map(lambda x: list(x), data))
    now = datetime.datetime.now().date()
    delta = now + datetime.timedelta(3)
    first = str(now) + 'T00:00:00'
    last = str(delta) + 'T00:00:00'

    for i in data:
        users.append(i[0])
    for user in users:
        try:
            await bot.send_message(user, text=head_rasp_msg)
            await sendraspmsg(user, first, last, )
        except aiogram.exceptions.TelegramBadRequest as e:
            logging.basicConfig(level=logging.WARNING,
                                format="%(asctime)s - [%(levelname)s] - %(name)s "
                                       "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
        except aiogram.exceptions.TelegramForbiddenError as e:
            logging.basicConfig(level=logging.WARNING,
                                format="%(asctime)s - [%(levelname)s] - %(name)s "
                                       "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
    print('отправил всем сообщение')

async def checupdate():
    update_day = await getdate()
    url_raspis = config.url_raspis
    response = requests.get(f"{url_raspis}").json()
    rasp_up_date = response['data']['info']['dateUploadingRasp']
    print(f"{rasp_up_date}     {update_day}")
    if update_day == rasp_up_date:
        print("Обновление не требуется")
    else:
        startupdate()
        await asyncio.sleep(90)
        data = await getusers()
        for user in data:
            try:
                await bot.send_message(user[0], text=check_update_msg.format(rasp_up_date))

            except aiogram.exceptions.TelegramBadRequest as e:
                print(f"Отправка не возможна: {e}")
            except aiogram.exceptions.TelegramForbiddenError as e:
                print(f"Отправка не возможна: {e} на id: {user[0]}")
        print("Рассылка оповещения об обновлении успешна")


@router.message(Command(commands=['getrasp']))
async def cmd_getrasp(message: Message):
    user = await finduser(message.from_user.id)
    if user is True:
        now = datetime.datetime.now().date()
        delta = now + datetime.timedelta(10)
        first = str(now) + 'T00:00:00'
        last = str(delta) + 'T00:00:00'
        await sendraspmsg(str(message.from_user.id), first, last, )

        user_id = message.from_user.id
        username = message.from_user.username
        name = f"{message.from_user.first_name} {message.from_user.last_name}"
        event = 'Запрос расписания'
        mess = message.text
        date = datetime.datetime.now()
        await log_event(user_id, username, name, event, mess, date)
        await upd_last(user_id, date)

    else:
        await message.answer(text="Твой аккаунт не найден, пройди регистрацию нажав комманду /reg",
                             reply_markup=await menu())
