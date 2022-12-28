from aiogram import types
from loader import dp, bot
from configs.config import ADMIN, CHANNEL
from buttons.button import btn_governors
from utils.db import set_vote, get_voted


@dp.message_handler()
async def msg1(message: types.Message):
    await message.answer("It's working...")


@dp.message_handler(commands=['send'])
async def msg2(message: types.Message):
    if message.chat.id == ADMIN:
        await bot.send_message(CHANNEL,
                               "Vodiy1.uz сўровномаси: Фарғона вилоятида қайси ҳоким яхши фаолият олиб боряпти? ",
                               reply_markup=btn_governors())
    else:
        await message.answer("Siz admin emassiz!")


@dp.callback_query_handler(lambda call: True)
async def vote(message: types.CallbackQuery):
    gov_id = int(message.data[9:])
    user_id = message.from_user.id
    mess_id = message.message.message_id
    voted = get_voted(user_id=user_id, mess_id=mess_id)
    if not voted:
        status = set_vote(gov_id=gov_id, user_id=user_id, message_id=mess_id)
        if status == 201:
            await bot.edit_message_reply_markup(
                chat_id=CHANNEL,
                message_id=message.message.message_id,
                reply_markup=btn_governors()
            )
            await bot.answer_callback_query(message.id, "Muvofaqiyatlik ovoz berdingiz!", show_alert=True)
        else:
            await bot.answer_callback_query(message.id, "Nimadur hato ketdi boshqatdan urinib ko'rin!", show_alert=True)
    else:
        await bot.answer_callback_query(message.id, "Siz avval ovoz bergansiz!", show_alert=True)
    # await bot.edit_message_text(text="Vodiy1.uz сўровномаси: Фарғона вилоятида қайси ҳоким яхши фаолият олиб боряпти? test",
    #                             chat_id=CHANNEL,
    #                             message_id=message.message.message_id,
    #                             reply_markup=btn_governors())

