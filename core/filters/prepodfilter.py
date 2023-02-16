from aiogram.filters import Filter
from aiogram.types import Message
from core.utils.messages import prep_fil_nonid_msg, idbigger_three_msg


class Prepods(Filter):
    def __init__(self, my_text: list[int]) -> None:
        self.my_text = my_text
    async def __call__(self, message: Message) -> bool:
        msg = message.text.split(' ')
        if len(msg) < 4:
            for i in msg:
                i = int(i)
                if i in self.my_text:
                    return True
                else:
                    await message.answer(text=prep_fil_nonid_msg)
                    return False
        else:
            await message.answer(text=idbigger_three_msg)
            return False


