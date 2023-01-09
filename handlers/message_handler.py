from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from buttons.button import menu, sub_menu, back, exist_pool, pool, get_all_post_btn, post_btn
from utils.states import Poll, Post
from configs.config import CHANEL
from utils.db import set_mes_id, delete, set_vote, get_voted, get_pool_for_del, get_post, set_post_mes_id, get_post_for_del


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
        await message.answer("Barcha so'ro'vnomalar kanalga jo'natish uchun birortasini bosing", reply_markup=exist_pool(data, False))
    # delete pool
    elif text.lower() == "so\'rovnomani o\'chirish":
        data = "del_pool_"
        await message.answer("Barcha so'ro'vnomalar o\'chirish uchun birortasini bosing", reply_markup=exist_pool(data, True))
    # create poll
    elif text.lower() == "yangi so\'rovnoma yaratish":
        await Poll.name.set()
        await message.answer("So'rovnoma uchun nom kiritin ko'pi bilan 40ta belgi bo'lishi kerak.\n"
                             "Bu nom kanalda ko'rinmaydi bu nom adminlar uchun ishlatiladi.\n"
                             "Bu nom takrorlanmas bo'lishiga etibor berin.", reply_markup=back())
    # send exist post
    elif text.lower() == "mavjud po\'stni yuborish":
        await message.answer("Barcha po\'stlar kanalga jo'natish uchun birortasini bosing", reply_markup=get_all_post_btn("send_exist_post_", False))
    # delete post
    elif text.lower() == "po\'stni o\'chirish":
        await message.answer("Barcha po\'stlar kanalga o\'chirish uchun birortasini bosing",
                             reply_markup=get_all_post_btn("delete_post_", True))
    # create post
    elif text.lower() == "yangi po\'st yaratish":
        await Post.name.set()
        await message.answer("Po\'st yaratish uchun nom kiritin ko'pi bilan 40ta belgi bo'lishi kerak.\n"
                             "Bu nom kanalda ko'rinmaydi bu nom adminlar uchun ishlatiladi.\n"
                             "Bu nom takrorlanmas bo'lishiga etibor berin.", reply_markup=back())
    else:
        await message.answer(f"Kerakli menu ni tanlang!", reply_markup=menu())


@dp.callback_query_handler(lambda callback: callback.data.startswith('all_pool_'))
async def callback_exist_pool(callback: types.CallbackQuery):
    message = callback.message
    pool_id = callback.data[9:]
    pool_data = pool(pool_id)
    text_pool = str(pool_data.get("text"))
    text_code = text_pool.replace(r'\n', '\n')
    pool_button = pool_data.get("kb")
    mes = await bot.send_message(CHANEL, text_code, reply_markup=pool_button)
    set_id = set_mes_id(pool_id, mes.message_id)
    if set_id:
        data = "all_pool_"
        await bot.edit_message_reply_markup(callback.from_user.id, callback.message.message_id, reply_markup=exist_pool(data, False))
        await callback.message.answer("Yuborildi")
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
    check_chanel = await bot.get_chat_member(CHANEL, user.id)
    if check_chanel.status == "member" or check_chanel.status == "creator" or check_chanel.status == "administrator":
        exist_vote = get_voted(user.id, message.message_id)
        if not exist_vote:
            put_vote = set_vote(field_id, user.id, message.message_id)
            if put_vote == 201:
                await bot.answer_callback_query(callback.id, "Muvofaqiyatlik ovoz berdingiz!", show_alert=True)
            else:
                await bot.answer_callback_query(callback.id, "Nimadur hato ketdi ilitimos boshqatdan urinib ko'ring!", show_alert=True)
        else:
            await bot.answer_callback_query(callback.id, "Siz avval ovoz bergansiz", show_alert=True)
    else:
        await bot.answer_callback_query(callback.id, "Kanalga obuna bolmagansiz. Iltimos kanalga obuna b'ling", show_alert=True)


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
            if pool_detail[0]:
                await bot.delete_message(CHANEL, pool_detail[0])
        except Exception as e:
            print(e)
        data = "del_pool_"
        await bot.edit_message_reply_markup(callback.from_user.id, callback.message.message_id, reply_markup=exist_pool(data, True))
        await callback.message.answer("O\'chirildi")


@dp.callback_query_handler(lambda callback: callback.data.startswith('get_post_answer_'))
async def get_post_answer(callback: types.CallbackQuery):
    user = callback.from_user
    post_id = callback.data[16:]
    post = get_post(post_id)
    answer = post[4]
    check_chanel = await bot.get_chat_member(CHANEL, user.id)
    if check_chanel.status == "member" or check_chanel.status == "creator" or check_chanel.status == "administrator":
        await bot.answer_callback_query(callback.id, answer, show_alert=True)
    else:
        await bot.answer_callback_query(callback.id, "Kanalga obuna bolmagansiz. Iltimos kanalga obuna b'ling", show_alert=True)


@dp.callback_query_handler(lambda callback: callback.data.startswith('send_exist_post_'))
async def send_post(callback: types.CallbackQuery):
    post = callback.data[16:]
    db_data = get_post(post_id=post)
    markup = post_btn(data=db_data[5], post_id=post)
    post_text = str(db_data[3])
    post_text = post_text.replace(r'\n', '\n')
    if db_data[2]:
        posted = await bot.send_photo(CHANEL, db_data[2], post_text, reply_markup=markup)
        url = f"https://t.me/{CHANEL[1:]}/{posted.message_id}"
        markup_url = post_btn(data=db_data[5], post_id=post, url=url)
        await callback.message.answer_photo(db_data[2], post_text, reply_markup=markup_url)
        set_post_message_id = set_post_mes_id(post, posted.message_id)
        if set_post_message_id == 201:
            pass
        else:
            # send creator if error
            pass
    else:
        posted = await bot.send_message(CHANEL, post_text, reply_markup=markup)
        url = f"https://t.me/{CHANEL[1:]}/{posted.message_id}"
        markup_url = post_btn(data=db_data[5], post_id=post, url=url)
        await callback.message.answer(post_text, reply_markup=markup_url)
        set_post_message_id = set_post_mes_id(post, posted.message_id)
        if set_post_message_id == 201:
            pass
        else:
            # send creator if error
            pass
    await bot.edit_message_reply_markup(callback.from_user.id, callback.message.message_id, reply_markup=get_all_post_btn("send_exist_post_", False))
    await callback.message.answer("Jo\'natildi", reply_markup=menu())


@dp.callback_query_handler(lambda callback: callback.data.startswith('delete_post_'))
async def send_post(callback: types.CallbackQuery):
    post_id = callback.data[12:]
    post_detail = get_post_for_del(post_id)
    reset_post = delete('post', 'id', int(post_id))
    if not reset_post:
        await callback.message.answer("O\'chirilmadi boshqatdan urinib ko\'ring")
        # send creator if error
    else:
        try:
            if post_detail[0]:
                await bot.delete_message(CHANEL, post_detail[0])
        except Exception as e:
            print(e)
        data = "delete_post_"
        await bot.edit_message_reply_markup(callback.from_user.id, callback.message.message_id,
                                            reply_markup=exist_pool(data, True))
        await callback.message.answer("O\'chirildi")


"""
 await bot.edit_message_text(f"In publishing and graphic design, Lorem ipsum is a placeholder text commonly used to demonstrate the visual form of a document or a typeface without relying on meaningful content. Lorem ipsum may be used as a placeholder before final copy is available\n\n<a href='https://t.me/test_chanel_uzb/{mes.message_id}'>link</a>",
                                "@test_chanel_uzb", mes.message_id, disable_web_page_preview=True)
"""
