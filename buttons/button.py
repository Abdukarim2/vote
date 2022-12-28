from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.db import get_governors


def btn_governors():
    kb = InlineKeyboardMarkup(row_width=1)
    for i in get_governors():
        index = get_governors().index(i)+1
        kb.insert(
            InlineKeyboardButton(text=f"{index}. {i[1]} {i[2]}", callback_data=f"governor_{i[0]}")
        )
    return kb
