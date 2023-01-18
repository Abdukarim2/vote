from aiogram import types
from loader import dp, bot
from configs.config import CHANEL
from utils.db import (get_one, get_voted, set_vote)


@dp.callback_query_handler(lambda callback: callback.data.startswith('vote_pool_'))
async def vote_pool(callback: types.CallbackQuery):
    user = callback.from_user
    message = callback.message
    pool_field_id = int(callback.data[10:])
    pool_id = await get_one('pool_field', ['bind'], 'id', pool_field_id)
    pool_id = pool_id[0]
    pool = await get_one('pool', ['check_user'], 'id', pool_id)
    check_chanel = await bot.get_chat_member(CHANEL, user.id)
    if pool[0] == 0 or check_chanel.status == "member" or check_chanel.status == "creator" or check_chanel.status == "administrator":
        exist_vote = await get_voted(user.id, message.message_id)
        if not exist_vote:
            put_vote = await set_vote(pool_field_id, user.id, message.message_id)
            if put_vote:
                await bot.answer_callback_query(callback.id, "Muvofaqiyatlik ovoz berdingiz!", show_alert=True)
            else:
                await bot.answer_callback_query(callback.id, "Nimadur hato ketdi ilitimos boshqatdan urinib ko'ring!",
                                                show_alert=True)
        else:
            await bot.answer_callback_query(callback.id, "Siz avval ovoz bergansiz", show_alert=True)
    else:
        await bot.answer_callback_query(callback.id, "Kanalga obuna bolmagansiz. Iltimos kanalga obuna b'ling",
                                        show_alert=True)


@dp.callback_query_handler(lambda callback: callback.data.startswith('question_answer_'))
async def question_answer(callback: types.CallbackQuery):
    user = callback.from_user
    question_id = callback.data[16:]
    question = await get_one('question', ['check_user', 'text_hidden'], 'id', question_id)
    check_chanel = await bot.get_chat_member(CHANEL, user.id)
    if question[0] == 0 or check_chanel.status == "member" or check_chanel.status == "creator" or check_chanel.status == "administrator":
        await bot.answer_callback_query(callback.id, f"{question[1]}", show_alert=True)
    else:
        await bot.answer_callback_query(callback.id, "Kanalga obuna bolmagansiz. Iltimos kanalga obuna b'ling",
                                        show_alert=True)
