from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

async def set_commansd(bot: Bot):
    commands = [
        BotCommand(
            command = 'start',
            description = 'Начало работы'
        ),
        BotCommand(
            command = 'reg',
            description = 'Регистрация'
        ),
        BotCommand(
            command = 'profile',
            description = 'Профиль'
        ),
        BotCommand(
            command = 'updprof',
            description = 'Обновить профиль'
        ),
        BotCommand(
            command='getrasp',
            description='Просмотреть расписание'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())