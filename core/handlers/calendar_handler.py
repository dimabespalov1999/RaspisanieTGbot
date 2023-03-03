from datetime import datetime
from aiogram.types import Message, CallbackQuery
from aiogram3_calendar import SimpleCalendar
from core.handlers import getrasp
from core.keyboards.keyb_generator import make_keyb
from core.utils.dbconnect import finduser, log_event
from core.utils.messages import reg_msg


async def nav_cal_handler(message: Message):
    user = await finduser(message.from_user.id)
    if user is True:
        await message.answer("Выберите нужную дату: ", reply_markup=await SimpleCalendar().start_calendar())
        await message.delete()
        event = 'Запрос расписания на дату'
        user_id = message.from_user.id
        username = message.from_user.username
        name = f"{message.from_user.first_name} {message.from_user.last_name}"
        mess = message.text
        date = datetime.now()
        await log_event(user_id, username, name, event, mess, date)
    else:
        await message.answer(text=reg_msg.format(message.from_user.first_name),
                             reply_markup=make_keyb(['Зарегистрироваться']))

async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        date = date.strftime("%Y-%m-%d")
        userid= callback_query.from_user.id
        await getrasp.sendraspmsg(userid, f"{date}T00:00:00", f"{date}T24:00:00")
        await callback_query.message.delete()