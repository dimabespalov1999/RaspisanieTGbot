from datetime import timedelta, datetime
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Text
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from core.handlers.basic import get_start, get_profile
from core.handlers import orderingfackursgroup, getrasp, calendar_handler
from aiogram3_calendar import simple_cal_callback
import asyncio
import config
import logging
from core.handlers.orderingfackursgroup import cmd_updprof, cmd_reg
from core.utils.commands import set_commansd
from aiogram.filters import Command

bot = Bot(token=config.token_bot, parse_mode='HTML')
dp = Dispatcher(storage=MemoryStorage())

async def start_bot(bot: Bot):
    await set_commansd(bot)
    await bot.send_message(config.admin_id, text="Бот с расписанием запущен")


async def stop_bot(bot: Bot):
    await bot.send_message(config.admin_id, text="Бот с расписанием остановлен")


async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    scheduller = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduller.add_job(getrasp.raspnxtdy, trigger='cron', hour=config.send_rasp_hour, minute=config.start_upd_min)
    scheduller.add_job(getrasp.checupdate, trigger='interval', hours=config.start_upd_hour, next_run_time = datetime.now() + timedelta(seconds = 10))
    scheduller.start()

    dp.message.register(get_start, Command(commands=['start']))

    dp.message.register(get_profile, Text(text=['Профиль'], ignore_case=True))
    dp.message.register(get_profile, Command(commands=['profile']))

    dp.message.register(cmd_updprof, Text(text=['Обновить профиль'], ignore_case=True))
    dp.message.register(getrasp.cmd_getrasp, Text(text=['Расписание на неделю'], ignore_case=True))

    dp.message.register(cmd_reg, Text(text=['Зарегистрироваться'], ignore_case=True))

    dp.message.register(calendar_handler.nav_cal_handler, Text(text=['Выбрать день'], ignore_case=True))
    dp.message.register(calendar_handler.nav_cal_handler, Command(commands=['chooseday']))
    dp.callback_query.register(calendar_handler.process_simple_calendar, simple_cal_callback.filter())


    dp.include_router(orderingfackursgroup.router)
    dp.include_router(getrasp.router)

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()



if __name__ == "__main__":
    asyncio.run(start())
