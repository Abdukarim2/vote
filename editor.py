import asyncio
from loader import bot
from configs.config import CHANEL
from utils.db import get_all, get_all_by
from buttons.button import btn_inline


async def update_pool():
    pools = await get_all('pool', ['message_id', 'id'])
    for i in pools:
        pool_fields = await get_all_by('pool_field', ['*'], 'bind', i[1], "ORDER BY -voted")
        markup = await btn_inline(pool_fields, row=1, callback="vote_pool_", index=[1, 0, 2])
        if markup:
            try:
                await bot.edit_message_reply_markup(chat_id=CHANEL, message_id=i[0], reply_markup=markup)
            except Exception as e:
                pass
        else:
            pass


async def update_loop():
    while True:
        await asyncio.sleep(10)
        await update_pool()

