from datetime import timedelta, datetime

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from core.handlers.basic import get_start, get_profile
from core.handlers import common, orderingfackursgroup, getrasp
import asyncio
import config
import logging
from core.utils.commands import set_commansd
from aiogram.filters import Command


bot = Bot(token=config.token_bot, parse_mode='HTML')


async def start_bot(bot: Bot):
    await set_commansd(bot)
    await bot.send_message(config.admin_id, text="Бот с расписанием запущен")


async def stop_bot(bot: Bot):
    await bot.send_message(config.admin_id, text="Бот с расписанием остановлен")


async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    dp = Dispatcher(storage=MemoryStorage())

    scheduller = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduller.add_job(getrasp.raspnxtdy, trigger='cron', hour=config.send_rasp_hour, minute=config.start_upd_min)
    scheduller.add_job(getrasp.checupdate, trigger='interval', hours=config.start_upd_hour, next_run_time = datetime.now() + timedelta(seconds = 10))
    scheduller.start()

    dp.message.register(get_start, Command(commands=['start']))
    dp.message.register(get_profile, Command(commands=['profile']))

    dp.include_router(common.router)
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
