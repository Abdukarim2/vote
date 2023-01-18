from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
)


async def btn_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(
        KeyboardButton("So\'rovnoma"),
        KeyboardButton("Savol")
    )
    return kb


async def btn_sub_menu(sub):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    word = {
        'pool': [
            "Yangi so\'rovnoma yaratish",
            "Mavjud So\'rovnomalarni ko\'rish"
        ],
        'post': [
            "Yangi savol yaratish",
            "Mavjud savollarni ko\'rish"
        ]
    }
    data = word.get(sub)
    for i in data:
        kb.insert(
            KeyboardButton(f"{i}")
        )
    kb.add(
        KeyboardButton("Orqaga")
    )
    return kb


async def btn_back(additional: list = None):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    if additional:
        for text in additional:
            kb.insert(KeyboardButton(text))
    kb.add(
        KeyboardButton('Orqaga')
    )
    return kb


async def btn_cancel(additional: list = None):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    if additional:
        for text in additional:
            kb.insert(KeyboardButton(text))
    kb.add(
        KeyboardButton('Bekor qilish')
    )
    return kb


async def btn_inline(data, row, callback=None, index: list = None):
    kb = InlineKeyboardMarkup(row_width=row)
    if index and callback:
        if len(index) == 3:
            for i in data:
                kb.row(
                    InlineKeyboardButton(text=f"{data.index(i) + 1} {i[index[0]]} {i[index[2]]}",
                                         callback_data=f"{callback}{i[index[1]]}")
                )
        elif len(index) == 2:
            for i in data:
                kb.row(
                    InlineKeyboardButton(text=f"{data.index(i) + 1} {i[index[0]]}", callback_data=f"{callback}{i[index[1]]}")
                )
    else:
        for i in data:
            kb.row(
                InlineKeyboardButton(text=f"{data.index(i)+1} {i}", callback_data="None")
            )

    return kb


async def btn_inline_url(data, url):
    kb = InlineKeyboardMarkup(row_width=1)
    for i, z in zip(data, url):
        kb.add(
            InlineKeyboardButton(text=i, url=z)
        )
    return kb


async def btn_answer(data, callback):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton(text=data, callback_data=callback)
    )
    return kb
