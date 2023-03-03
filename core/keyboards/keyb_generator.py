
from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton




def make_keyb(items: list[str])-> ReplyKeyboardMarkup:

    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard = True)

def makegroups(items: tuple[str])-> ReplyKeyboardMarkup:
    rows=[]
    data = map(lambda x: list(x), items)
    buttons = map(lambda x: KeyboardButton(text = str(x[0])), data)
    buttons = list(buttons)
    for i in range(0, len(buttons), 4):
        rows.append(buttons[i:i+4])
    print(rows)
    return ReplyKeyboardMarkup(keyboard = rows, resize_keyboard = True)


