from aiogram.filters import Filter
from aiogram.types import Message


class Groups(Filter):
    def __init__(self, my_text: list[str]) -> None:
        self.my_text = my_text

    async def __call__(self, message: Message) -> bool:
        if message.text in self.my_text:
            return True
        else:
            return False
