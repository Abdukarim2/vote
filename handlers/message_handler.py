from aiogram import types
from configs.config import CHANEL
from loader import dp
from buttons.button import (
    btn_menu, btn_sub_menu, btn_back, btn_inline_url
)
from utils.db import (
    get_all
)
from .helper import maker
from states.state import Pool, Question


@dp.message_handler()
async def messages(message: types.Message):
    text = message.text
    back = await btn_back()
    # pool submenu
    if text.lower() == 'so\'rovnoma':
        sub_menu = await btn_sub_menu('pool')
        await message.reply(f"Kerakli menu ni tanlang!", reply_markup=sub_menu)
    # create pool
    elif text.lower() == 'yangi so\'rovnoma yaratish':
        await Pool.name.set()
        await message.answer("So'rovnoma yaratish uchun nom kiritin ko'pi bilan 40ta belgi bo'lishi kerak.\n"
                             "Bu nom kanalda ko'rinmaydi bu nom adminlar uchun ishlatiladi.\n"
                             "Bu nom takrorlanmas bo'lishiga etibor berin.", reply_markup=back)
    elif text.lower() == 'mavjud so\'rovnomalarni ko\'rish':
        data = await get_all('pool', ['name', 'message_id'])
        if data:
            texts = []
            urls = []
            for i in data:
                texts.append(i[0])
                urls.append(f"https://t.me/{CHANEL[1:]}/{i[1]}")
            markup = await btn_inline_url(data=texts, url=urls)
            await maker(message.chat.id, "Barcha so'rovnomalar", markup)
        else:
            await message.answer("So'rovnoma mavjud emas")

    # question submenu
    elif text.lower() == 'savol':
        sub_menu = await btn_sub_menu('post')
        await message.reply(f"Kerakli menu ni tanlang!", reply_markup=sub_menu)
    elif text.lower() == 'yangi savol yaratish':
        await Question.name.set()
        await message.answer("Savol yaratish uchun nom kiritin ko'pi bilan 40ta belgi bo'lishi kerak.\n"
                             "Bu nom kanalda ko'rinmaydi bu nom adminlar uchun ishlatiladi.\n"
                             "Bu nom takrorlanmas bo'lishiga etibor berin.", reply_markup=back)
    elif text.lower() == "mavjud savollarni ko\'rish":
        data = await get_all('question', ['name', 'message_id'])
        if data:
            texts = []
            urls = []
            for i in data:
                texts.append(i[0])
                urls.append(f"https://t.me/{CHANEL[1:]}/{i[1]}")
            markup = await btn_inline_url(data=texts, url=urls)
            await maker(message.chat.id, "Barcha savollar!", markup)
        else:
            await message.answer("Savol mavjud emas")
    else:
        menu = await btn_menu()
        await message.answer(f"Kerakli menu ni tanlang!", reply_markup=menu)
