from typing import Callable, Awaitable , Dict, Any
import aiosqlite
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from core.utils.dbconnect import Request
from config import path_db


class Dbsession(BaseMiddleware):
    def __init__(self, connector: aiosqlite.connect()):
        super().__init__()
        self.connector = connector

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    )-> Any:
        async with self.connector.connect as db:
            data['request'] = Request(db)
            return await handler(event, data)
