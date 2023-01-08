import asyncio
from loader import bot
from utils.db import get_all_pool
from configs.config import CHANEL
from buttons.button import pool


async def update_pool():
    data = get_all_pool()
    for i in data:
        markup = pool(i[1])
        if i[2]:
            if markup:
                try:
                    await bot.edit_message_reply_markup(chat_id=CHANEL, message_id=i[2], reply_markup=markup.get("kb"))
                except Exception as e:
                    print(e)
            else:
                pass
        else:
            pass


async def forever():
    while True:
        await asyncio.sleep(8)
        await update_pool()
