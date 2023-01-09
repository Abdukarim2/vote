from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
)
from utils.db import get_all_pool, get_pool, get_all_post


def menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        KeyboardButton("So\'rovnoma"),
        KeyboardButton("Po\'st")
    )
    return kb


def sub_menu(sub):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    word = {
        'poll': [
            "Mavjud so\'rovnomani yuborish",
            "Yangi so\'rovnoma yaratish",
            "So\'rovnomani o\'chirish"
        ],
        'post': [
            "Mavjud po\'stni yuborish",
            "Yangi po\'st yaratish",
            "Po\'stni o\'chirish"
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


def back():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.insert(
        KeyboardButton("Orqaga")
    )
    return kb


def save_send_back():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(
        KeyboardButton("Saqlash"),
        KeyboardButton("Jo'natish"),
        KeyboardButton("Bekor qilish")
    )
    return kb


def exist_pool(call_data, send=None):
    kb = InlineKeyboardMarkup(row_width=1)
    data = get_all_pool()
    data_btn = []
    if not send:
        for i in data:
            if i[2] is None:
                data_btn.append(i)
    elif send:
        for i in data:
            data_btn.append(i)
    for i in data_btn:
        kb.add(
            InlineKeyboardButton(text=f"{i[0]}", callback_data=f"{call_data}{i[1]}")
        )
    return kb


def pool(pool_id):
    kb = InlineKeyboardMarkup(row_width=1)
    data = get_pool(pool_id)
    if data:
        text = data[0][1]
    else:
        last_data = get_all_pool()
        text = last_data[-1][3]
    for i in data:
        index = data.index(i)
        kb.add(
            InlineKeyboardButton(text=f"{index+1} {i[3]} {i[4]}", callback_data=f"pool_{i[5]}")
        )
    return {
        "kb": kb,
        "text": text
    }


def post_btn(data, post_id, url: str = None):
    kb = InlineKeyboardMarkup(row_width=1)
    if url:
        kb.add(
            InlineKeyboardButton(text=f"{data}", url=url)
        )
    else:
        kb.add(
            InlineKeyboardButton(text=f"{data}", callback_data=f"get_post_answer_{post_id}")
        )
    return kb


def get_all_post_btn(call_data, send):
    kb = InlineKeyboardMarkup(row_width=1)
    data = get_all_post()
    data_btn = []
    if not send:
        for i in data:
            if i[6] is None:
                data_btn.append(i)
    elif send:
        for i in data:
            data_btn.append(i)
    for i in data_btn:
        kb.add(
            InlineKeyboardButton(text=f"{i[1]}", callback_data=f"{call_data}{i[0]}")
        )
    return kb

