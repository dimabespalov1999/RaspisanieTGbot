from datetime import datetime

from aiogram import Bot
from aiogram.types import Message, ReplyKeyboardRemove

from core.keyboards.keyb_generator import make_keyb
from core.utils.dbconnect import finduser, get_prof, log_event, upd_last, get_group_name
from core.utils.messages import profile_stud_msg, profile_prepod_msg, reg_msg, start_msg


async def get_start(message: Message, bot: Bot):
    userid = message.from_user.id
    user = await finduser(userid)
    if user is True:
        await bot.send_message(message.from_user.id, start_msg, reply_markup=ReplyKeyboardRemove)
    else:
        await bot.send_message(message.from_user.id, reg_msg.format(message.from_user.first_name), reply_markup= make_keyb(["/reg"]))
async def get_profile(message: Message, bot: Bot):
    user_id = message.from_user.id
    user = await finduser(user_id)
    if user is True:
        username = message.from_user.username
        name = f"{message.from_user.first_name} {message.from_user.last_name}"
        event = 'Запрос профиля'
        mess = message.text
        date = datetime.now()
        await log_event(user_id, username, name, event, mess, date)
        await upd_last(user_id, date)
        userdata = await get_prof(userid=user_id)

        if userdata[0][2] == 'student':
            groupdata = await  get_group_name([userdata[0][3]])
            status = 'Студент(ка)'
            last_date = userdata[0][8]
            reg_date = userdata[0][9]
            kurs = groupdata[0][1]
            facul = groupdata[0][2]
            group = groupdata[0][0]
            msg = profile_stud_msg.format(message.from_user.first_name, status, kurs, facul, group, last_date, reg_date)
            await bot.send_message(message.from_user.id, msg)
        else:
            status = 'Преподаватель'
            last_date = userdata[0][8]
            reg_date = userdata[0][9]
            groupdata = await  get_group_name([userdata[0][4], userdata[0][5], userdata[0][6], userdata[0][7]])
            msg = []
            msg.append(profile_prepod_msg.format(message.from_user.first_name, status, last_date, reg_date))
            k = 0
            for i in groupdata:

                k=k+1
                msg.append(f"\n<b>Преодаватель</b> {k} - {i[0]}")
            await bot.send_message(message.from_user.id, ' '.join(msg))
    else:
        await bot.send_message(message.from_user.id, reg_msg.format(message.from_user.first_name),reply_markup= make_keyb(["/reg"]))




