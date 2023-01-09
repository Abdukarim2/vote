from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from buttons.button import menu, save_send_back, pool, post_btn
from utils.states import Poll, Post
from utils.db import create, delete, set_mes_id, get_post, set_post_mes_id
from configs.config import CHANEL


@dp.message_handler(lambda message: message.text.lower() == "orqaga", state='*')
async def cancel_state(message: types.Message, state: FSMContext):
    await state.reset_data()
    await state.finish()
    await message.reply("Bekor qilindi!", reply_markup=menu())


@dp.message_handler(state=Poll.name)
async def pool_name(message: types.Message, state: FSMContext):
    text = message.text
    if len(text) > 40:
        await message.answer("Nom ko'pi bilan 40ta belgi bo'lishi kerak iltimos qaytadan kiritin.")
    else:
        async with state.proxy() as data:
            data['name'] = text
        await Poll.next()
        await message.answer("So'rovnoma matnini kiritin ushbu matn so'rovnoma tepasida ko'rinib turadi.")


@dp.message_handler(state=Poll.text)
async def pool_text(message: types.Message, state: FSMContext):
    text = message.text
    async with state.proxy() as data:
        data['text'] = text
        pool_id = create('pool', data.as_dict())
        if pool_id:
            data['bind'] = pool_id
            await Poll.next()
            await message.answer("So'rovnoma maydonlarini kiritishingiz mumkun.\n"
                                 "So'rovnoma maydonlarini birma bir kiritishingiz kerak.\n"
                                 f"Maydon kiritishingiz mumkun...\n\n"
                                 "1.Kiritib bo'lgach <b>Saqlash</b> tugmasini bossangiz ushbu so'rovnoma saqlab "
                                 "olinadi kanalga jo'natilmaydi buni keyinchalik jo'natishingiz mumkun.\n\n"
                                 "2.Kiritib bo'lgach <b>Jo'natish</b> tugmasini bossangiz ushbu so'rovnoma saqlab "
                                 "olinadi va kanalga jo'natiladi\n\n"
                                 "3.Agar bekor qilmoqchi bo'lsangiz <b>Bekor qilish</b> tugmasini bossangiz ushbu "
                                 "so'rovnoma o'chib ketadi va kanalga ham jo'natilmaydi\n\n",
                                 reply_markup=save_send_back()
                                 )
        else:
            await message.reply("Nimadur hato ketdi iltimos qaytadan urinib ko'ring", reply_markup=menu())


@dp.message_handler(state=Poll.field)
async def pool_field(message: types.Message, state: FSMContext):
    text = message.text
    async with state.proxy() as data:
        data['name'] = text
        data['voted'] = 0
        copy_data = data.as_dict()
        copy_data.pop('text')
        if text.lower() == "saqlash":
            data.clear()
            await state.finish()
            await message.answer("Saqlandi", reply_markup=menu())
        elif text.lower() == "jo\'natish":
            data.clear()
            await state.finish()
            pool_id = copy_data.get('bind')
            pool_data = pool(pool_id)
            text_pool = str(pool_data.get("text"))
            pool_button = pool_data.get("kb")
            text_code = text_pool.replace(r'\n', '\n')
            mes = await bot.send_message(CHANEL, text_code, reply_markup=pool_button)
            set_id = set_mes_id(pool_id, mes.message_id)
            if set_id:
                await message.answer("Jo'natildi", reply_markup=menu())
            else:
                # send creator if error
                await mes.delete()
                bind_id = copy_data.get("bind")
                delete('pool', 'id', bind_id)
                delete('field', 'bind', bind_id)
                await message.answer("Nimadur hato ketdi iltimos malumotlarni qayta kiritib chiqing!", reply_markup=menu())
        elif text.lower() == "bekor qilish":
            reset_pool = delete('pool', 'id', copy_data.get("bind"))
            reset_field = delete('field', 'bind', copy_data.get("bind"))
            if not reset_field and reset_pool:
                # send creator if error
                pass
            data.clear()
            await state.finish()
            await message.reply("Bekor qilindi!", reply_markup=menu())
        else:
            field = create("field", copy_data)
            if field:
                await message.answer(f"Yana maydon kiritishingiz mumkun...")
            else:
                await message.reply("Nimadur hato ketdi iltimos qaytadan urinib ko'ring", reply_markup=menu())


@dp.message_handler(state=Post.name)
async def post_name(message: types.Message, state: FSMContext):
    text = message.text
    if len(text) > 40:
        await message.answer("Nom ko'pi bilan 40ta belgi bo'lishi kerak iltimos qaytadan kiritin.")
    else:
        async with state.proxy() as data:
            data['name'] = text
        await Post.next()
        await message.answer("Po\'st uchun rasm yoki fayl jo'nating agar po\'stda rasm yoki fayl bo\'lishini hohlamasangiz "
                             "po\'st matnini bir qismini kiritishingiz mumkun qolgan qismini tugma bosilganda chiqishi uchun alohida kiritasiz.")


@dp.message_handler(content_types=types.ContentTypes.PHOTO, state=Post.photo_id) #[, types.ContentTypes.DOCUMENT]
async def post_image(message: types.Message, state: FSMContext):
    photo = message.photo
    file_id = photo[-1].file_id
    async with state.proxy() as data:
        data['photo_id'] = file_id
    await Post.next()
    await message.answer("Po\'st matnini bir qismini kiritishingiz mumkun qolgan qismini tugma bosilganda chiqishi uchun alohida kiritasiz.")


@dp.message_handler(content_types=types.ContentTypes.DOCUMENT, state=Post.photo_id)
async def post_document(message: types.Message, state: FSMContext):
    document = message.document
    file_id = document.file_id
    async with state.proxy() as data:
        data['photo_id'] = file_id
    await Post.next()
    await message.answer("Po\'st matnini bir qismini kiritishingiz mumkun qolgan qismini tugma bosilganda chiqishi uchun alohida kiritasiz.")


@dp.message_handler(state=Post.photo_id)
async def no_post_image(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text_visible'] = message.text
    await Post.text_hidden.set()
    await message.answer("Po\'st matnini qolgan qismini kiritishingiz mumkun qolgan qismi tugma bosilganda chiqadi.")


@dp.message_handler(state=Post.text_visible)
async def post_visible_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text_visible'] = message.text
    await Post.next()
    await message.answer("Po\'st matnini qolgan qismini kiritishingiz mumkun qolgan qismi tugma bosilganda chiqadi.")


@dp.message_handler(state=Post.text_hidden)
async def post_hidden_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text_hidden'] = message.text
    await Post.next()
    await message.answer("Po\'st tagidagi tugma uchun matn kiritin bu matn ko'pi bilan 40ta belgi bo'lishi kerak.")


@dp.message_handler(state=Post.button)
async def post_button_text(message: types.Message, state: FSMContext):
    text = message.text
    if len(text) > 40:
        await message.answer("Matn ko'pi bilan 40ta belgi bo'lishi kerak.")
    else:
        async with state.proxy() as data:
            data['button'] = text
        await Post.next()
        await message.answer("1.Po\'st ni saqlash uchun <b>Saqlash</b> tugmasini bossangiz ushbu po\'st saqlab "
                             "olinadi kanalga jo'natilmaydi buni keyinchalik jo'natishingiz mumkun.\n\n"
                             "2.Po\'stni kanalga jo\'natish uchun <b>Jo'natish</b> tugmasini bossangiz ushbu po\'st saqlab "
                             "olinadi va kanalga jo'natiladi\n\n"
                             "3.Agar bekor qilmoqchi bo'lsangiz <b>Bekor qilish</b> tugmasini bossangiz ushbu "
                             "po\'st o'chib ketadi va kanalga ham jo'natilmaydi\n\n",
                             reply_markup=save_send_back()
                             )


@dp.message_handler(state=Post.action)
async def post_action(message: types.Message, state: FSMContext):
    text = message.text
    async with state.proxy() as data:
        data_db = data.as_dict()
        if text.lower() == "saqlash":
            data.clear()
            await state.finish()
            post = create('post', data_db)
            if post:
                await message.answer("Saqlandi", reply_markup=menu())
            else:
                await message.answer("Nimadur hato ketdi iltimos malumotlarni qayta kiritib chiqing!",
                                     reply_markup=menu())
        elif text.lower() == "jo\'natish":
            data.clear()
            await state.finish()
            post = create('post', data_db)
            if post:
                db_data = get_post(post_id=post)
                markup = post_btn(data=db_data[5], post_id=post)
                post_text = str(db_data[3])
                post_text = post_text.replace(r'\n', '\n')
                if db_data[2]:
                    posted = await bot.send_photo(CHANEL, db_data[2], post_text, reply_markup=markup)
                    url = f"https://t.me/{CHANEL[1:]}/{posted.message_id}"
                    markup_url = post_btn(data=db_data[5], post_id=post, url=url)
                    await message.answer_photo(db_data[2], post_text, reply_markup=markup_url)
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
                    await message.answer(post_text, reply_markup=markup_url)
                    set_post_message_id = set_post_mes_id(post, posted.message_id)
                    if set_post_message_id == 201:
                        pass
                    else:
                        # send creator if error
                        pass
                await message.answer("Jo\'natildi", reply_markup=menu())
            else:
                await message.answer("Nimadur hato ketdi iltimos malumotlarni qayta kiritib chiqing!",
                                     reply_markup=menu())
        elif text.lower() == "bekor qilish":
            data.clear()
            await state.finish()
            await message.reply("Bekor qilindi!", reply_markup=menu())
        else:
            await message.answer("1.Po\'st ni saqlash uchun <b>Saqlash</b> tugmasini bossangiz ushbu po\'st saqlab "
                                 "olinadi kanalga jo'natilmaydi buni keyinchalik jo'natishingiz mumkun.\n\n"
                                 "2.Po\'stni kanalga jo\'natish uchun <b>Jo'natish</b> tugmasini bossangiz ushbu po\'st saqlab "
                                 "olinadi va kanalga jo'natiladi\n\n"
                                 "3.Agar bekor qilmoqchi bo'lsangiz <b>Bekor qilish</b> tugmasini bossangiz ushbu "
                                 "po\'st o'chib ketadi va kanalga ham jo'natilmaydi\n\n",
                                 reply_markup=save_send_back()
                                 )
