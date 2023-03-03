
from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton


async def menu():
    menu = [
        [KeyboardButton(text="Расписание на неделю"), KeyboardButton(text="Выбрать день")],
        [KeyboardButton(text='Профиль'), KeyboardButton(text="Обновить профиль")]
    ]
    return ReplyKeyboardMarkup(keyboard=menu, resize_keyboard=True)