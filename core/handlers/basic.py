from aiogram import Bot
from aiogram.types import Message, ReplyKeyboardRemove
from core.utils.dbconnect import finduser

async def get_start(message: Message, bot: Bot):
    userid = message.from_user.id
    user = await finduser(userid)
    if user is True:
        await  bot.send_message(message.from_user.id,f"<b>\U0001F538   /getrasp  -  Просмотреть расписание\
                                                          \U0001F538   /updprof  -  Изменить данные профиля\
                                                          \U0001F538   /profile  -  Ваш профиль</b>",
                                reply_markup=ReplyKeyboardRemove)
    else:
        await bot.send_message(message.from_user.id, f'<b>Привет {message.from_user.first_name}'
                                                 f'. Рад тебя видеть. Для регистрации выбери команду /reg из Меню.</b>')


