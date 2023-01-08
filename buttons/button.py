from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
)
from utils.db import get_all_pool, get_pool


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


def exist_pool(call_data):
    kb = InlineKeyboardMarkup(row_width=1)
    data = get_all_pool()
    for i in data:
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
        text = last_data[-1][0]
    for i in data:
        index = data.index(i)
        kb.add(
            InlineKeyboardButton(text=f"{index+1} {i[3]} {i[4]}", callback_data=f"pool_{i[5]}")
        )
    return {
        "kb": kb,
        "text": text
    }
