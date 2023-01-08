from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from buttons.button import menu, sub_menu, back, exist_pool, pool
from utils.states import Poll
from configs.config import CHANEL
from utils.db import set_mes_id, delete, set_vote, get_voted, get_pool_for_del


@dp.errors_handler(exception=Exception)
async def errors(exception):
    print(exception)


@dp.message_handler()
async def messages(message: types.Message, state: FSMContext, middleware_data):
    text = message.text
    if text.lower() == "so\'rovnoma":
        await message.answer("Kerakli menu ni tanlang", reply_markup=sub_menu('poll'))
    elif text.lower() == "po\'st":
        await message.answer("Kerakli menu ni tanlang", reply_markup=sub_menu('post'))
    # send exist poll
    elif text.lower() == "mavjud so\'rovnomani yuborish":
        data = "all_pool_"
        await message.answer("Barcha so'ro'vnomalar kanalga jo'natish uchun birortasini bosing", reply_markup=exist_pool(data))
    elif text.lower() == "so\'rovnomani o\'chirish":
        data = "del_pool_"
        await message.answer("Barcha so'ro'vnomalar o\'chirish uchun birortasini bosing", reply_markup=exist_pool(data))
    # create poll
    elif text.lower() == "yangi so\'rovnoma yaratish":
        await Poll.name.set()
        await message.answer("So'rovnoma uchun nom kiritin ko'pi bilan 40ta belgi bo'lishi kerak.\n"
                             "Bu nom kanalda ko'rinmaydi bu nom adminlar uchun ishlatiladi.\n"
                             "Bu nom takrorlanmas bo'lishiga etibor berin.", reply_markup=back())
    # send exist post
    elif text.lower() == "mavjud po\'stni yuborish":
        await message.answer("dwdd")
    # create post
    elif text.lower() == "yangi po\'st yaratish":
        await message.answer("Yangi post yaratish")
    else:
        await message.answer(f"Kerakli menu ni tanlang!", reply_markup=menu())


@dp.callback_query_handler(lambda callback: callback.data.startswith('all_pool_'))
async def callback_exist_pool(callback: types.CallbackQuery):
    message = callback.message
    pool_id = callback.data[9:]
    pool_data = pool(pool_id)
    text_pool = pool_data.get("text")
    pool_button = pool_data.get("kb")
    mes = await bot.send_message(CHANEL, text_pool, reply_markup=pool_button)
    set_id = set_mes_id(pool_id, mes.message_id)
    if set_id:
        await message.answer("Jo'natildi", reply_markup=menu())
    else:
        # send creator if error
        await mes.delete()
        delete('pool', 'id', pool_id)
        delete('field', 'bind', pool_id)
        await message.answer("Nimadur hato ketdi iltimos malumotlarni qayta kiritib chiqing!", reply_markup=menu())


@dp.callback_query_handler(lambda callback: callback.data.startswith('pool_'))
async def set_pool_vote(callback: types.CallbackQuery):
    field_id = int(callback.data[5:])
    user = callback.from_user
    message = callback.message
    exist_vote = get_voted(user.id, message.message_id)
    if not exist_vote:
        put_vote = set_vote(field_id, user.id, message.message_id)
        if put_vote == 201:
            await bot.answer_callback_query(callback.id, "Muvofaqiyatlik ovoz berdingiz!", show_alert=True)
        else:
            await bot.answer_callback_query(callback.id, "Nimadur hato ketdi ilitimos boshqatdan urinib ko'ring!", show_alert=True)
    else:
        await bot.answer_callback_query(callback.id, "Siz avval ovoz bergansiz", show_alert=True)


@dp.callback_query_handler(lambda callback: callback.data.startswith('del_pool_'))
async def del_pool(callback: types.CallbackQuery):
    user = callback.from_user
    pool_id = callback.data[9:]
    pool_detail = get_pool_for_del(pool_id)
    reset_pool = delete('pool', 'id', int(pool_id))
    reset_field = delete('field', 'bind', int(pool_id))
    reset_votes = delete('vote', 'user_id', int(user.id))
    if not reset_field and reset_pool and reset_votes:
        await callback.message.answer("O\'chirilmadi boshqatdan urinib ko\'ring")
        # send creator if error
    else:
        try:
            await bot.delete_message(CHANEL, pool_detail[0])
        except Exception as e:
            print(e)
        await callback.message.answer("O\'chirildi")

"""
@dp.message_handler()
async def messages(message: types.Message, middleware_data):
    # print(middleware_data)
    # mes = await message.answer("dwd")
    # await mes.edit_text(f"dwdd<a href='https://t.me/test_projects2_bot/{mes.message_id}'>link</a>")
    mes = await bot.send_message("@test_chanel_uzb",
                           f"{message.text}\n\n<a href='https://t.me/test_chanel_uzb/{message.message_id}'>link</a>")
    # await mes.edit_text(
    #     f"In publishing and graphic design, Lorem ipsum is a placeholder text commonly used to demonstrate the visual form of a document or a typeface without relying on meaningful content. Lorem ipsum may be used as a placeholder before final copy is available\n\n<a href='https://t.me/test_chanel_uzb/{mes.message_id}'>link</a>",
    #     disable_web_page_preview=True)
    await bot.edit_message_text(f"In publishing and graphic design, Lorem ipsum is a placeholder text commonly used to demonstrate the visual form of a document or a typeface without relying on meaningful content. Lorem ipsum may be used as a placeholder before final copy is available\n\n<a href='https://t.me/test_chanel_uzb/{mes.message_id}'>link</a>",
                                "@test_chanel_uzb", mes.message_id, disable_web_page_preview=True)


@dp.channel_post_handler()
async def msg(message: types.Message):
    print(message)
    mes = message
"""
