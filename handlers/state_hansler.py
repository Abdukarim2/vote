from aiogram import types
from aiogram.dispatcher import FSMContext
from configs.config import CHANEL
from loader import dp, bot
from buttons.button import (btn_back, btn_menu, btn_cancel, btn_inline, btn_inline_url, btn_answer)
from utils.db import (create, delete, get_all_by, set_message_id)
from states.state import Pool, Question
from handlers.helper import maker


@dp.message_handler(lambda message: message.text.lower() == "orqaga", state='*')
async def cancel_state(message: types.Message, state: FSMContext):
    menu = await btn_menu()
    await state.reset_data()
    await state.finish()
    await message.reply("Bekor qilindi!", reply_markup=menu)


@dp.message_handler(state=Pool.name)
async def pool_name(message: types.Message, state: FSMContext):
    text = message.text
    if len(text) > 40:
        await message.answer("Nom ko'pi bilan 40ta belgi bo'lishi kerak iltimos qaytadan kiritin.")
    else:
        async with state.proxy() as data:
            data['name'] = text
        await Pool.next()
        await message.answer("So\'rovnoma uchun rasm, video yoki fayl jo'nating agar "
                             "so\'rovnomada rasm, video yoki fayl bo\'lishini hohlamasangiz"
                             "so\'rovnoma matnini kiritishingiz mumkun ushbu matn"
                             "so\'rovnoma tepasida ko\'rinib turadi")


@dp.message_handler(content_types=types.ContentTypes.PHOTO, state=Pool.file_id)
async def pool_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1]
    async with state.proxy() as data:
        data['file_id'] = photo.file_id
        data['file_type'] = 'photo'
    await Pool.next()
    await message.answer("So\'rovnoma matnini kiritishingiz mumkun ushbu matn so\'rovnomada tepasida ko\'rinib turadi")


@dp.message_handler(content_types=types.ContentTypes.VIDEO, state=Pool.file_id)
async def pool_video(message: types.Message, state: FSMContext):
    video = message.video
    file_id = video.file_id
    async with state.proxy() as data:
        data['file_id'] = file_id
        data['file_type'] = 'video'
    await Pool.next()
    await message.answer("So\'rovnoma matnini kiritishingiz mumkun ushbu matn so\'rovnomada tepasida ko\'rinib turadi")


@dp.message_handler(content_types=types.ContentTypes.DOCUMENT, state=Pool.file_id)
async def pool_document(message: types.Message, state: FSMContext):
    document = message.document
    file_id = document.file_id
    async with state.proxy() as data:
        data['file_id'] = file_id
        data['file_type'] = 'document'
    await Pool.next()
    await message.answer("So\'rovnoma matnini kiritishingiz mumkun ushbu matn so\'rovnomada tepasida ko\'rinib turadi")


@dp.message_handler(state=Pool.file_id)
async def pool_fileid_override(message: types.Message, state: FSMContext):
    text = message.text
    async with state.proxy() as data:
        data['text'] = text
    await Pool.button.set()
    await message.answer("So'rovnomaga taklif qiluvchi tugma uchun matn kiritin ushbu"
                         "matn 40ta belgidan oshmasligi kerak.")


@dp.message_handler(state=Pool.text)
async def pool_text(message: types.Message, state: FSMContext):
    text = message.text
    async with state.proxy() as data:
        data['text'] = text
    await Pool.next()
    await message.answer("So'rovnomaga taklif qiluvchi tugma uchun matn kiritin ushbu"
                         "matn 40ta belgidan oshmasligi kerak.")


@dp.message_handler(state=Pool.button)
async def pool_button(message: types.Message, state: FSMContext):
    text = message.text
    back = await btn_back(['Ha', 'Yo\'q'])
    if len(text) > 40:
        await message.answer("Matn ko'pi bilan 40ta belgi bo'lishi kerak iltimos qaytadan kiritin.")
    else:
        async with state.proxy() as data:
            data['button'] = text
        await Pool.next()
        await message.answer("Ushbu so\'rovnomada ishtirok etish uchun kanalga obuna bo\'lishi kerakmi?",
                             reply_markup=back)


@dp.message_handler(state=Pool.check)
async def pool_check_user(message: types.Message, state: FSMContext):
    text = message.text.lower()
    if text in ['ha', 'yo\'q']:
        async with state.proxy() as data:
            if text == 'ha':
                data['check_user'] = True
            else:
                data['check_user'] = False
            new_pool_id = await create('pool', data.as_dict())
            if new_pool_id:
                data['bind'] = new_pool_id
                data['pool_field'] = []
                await Pool.next()
                cancel = await btn_cancel()
                await message.answer("So'rovnoma maydonlarini kiritishingiz mumkun.\n"
                                     "So'rovnoma maydonlarini birma bir kiritishingiz kerak.\n"
                                     f"Maydon kiritin...", reply_markup=cancel)
            else:
                data.clear()
                await state.finish()
                menu = await btn_menu()
                await message.reply("Nimadur hato ketdi iltimos boshqatdan kiritib chiqing!", reply_markup=menu)
    else:
        back = await btn_back(['Ha', 'Yo\'q'])
        await message.answer("Ushbu so\'rovnomada ishtirok etish uchun kanalga obuna bo\'lishi kerakmi?",
                             reply_markup=back)


@dp.message_handler(state=Pool.field)
async def pool_field(message: types.Message, state: FSMContext):
    text = message.text
    chat = message.chat
    async with state.proxy() as data:
        pool_id = data.as_dict().get('bind')
        if not text.lower() == 'bekor qilish':
            if text.lower() == 'jo\'natish' or text.lower() == 'ko\'rish':
                fields = data.as_dict().get('pool_field')
                if len(fields) >= 2:
                    as_dict = data.as_dict()
                    file = as_dict.get('file_id')
                    file_type = as_dict.get('file_type')
                    text_body = as_dict.get('text')
                    if text.lower() == 'jo\'natish':
                        for i in fields:
                            new_pool_field = await create('pool_field', i)
                            if new_pool_field:
                                continue
                            else:
                                await delete('pool_field', 'bind', pool_id)
                                await delete('pool', 'id', pool_id)
                                data.clear()
                                await state.finish()
                                menu = await btn_menu()
                                await message.answer("Nimadur hato ketdi iltimos boshqatdan kiritib chiqing!", reply_markup=menu)
                                break
                        else:
                            pool_fields = await get_all_by('pool_field', ['*'], 'bind', pool_id)
                            fields_list = [list(i) for i in pool_fields]
                            markup = await btn_inline(data=fields_list, row=1, callback="vote_pool_", index=[1, 0, 2])
                            posted = await maker(CHANEL, text=text_body, markup=markup, file=file, file_type=file_type)
                            button = as_dict.get('button')
                            url = f"https://t.me/{CHANEL[1:]}/{posted.message_id}"
                            markup_url = await btn_inline_url(data=[button], url=[url])
                            shared = await maker(chat=chat.id, text=text_body, markup=markup_url,
                                                 file=file, file_type=file_type)
                            data.clear()
                            menu = await btn_menu()
                            await state.finish()
                            message_id = await set_message_id('pool', posted.message_id, pool_id)
                            if message_id:
                                await message.answer("Jo\'natildi 👆ushbu postni reklama qila olasiz.",
                                                     reply_markup=menu)
                            else:
                                await message.answer("Nimadur hato ketdi iltimos boshqatdan kiritib chiqing!",
                                                     reply_markup=menu)
                                await delete('pool', 'id', pool_id)
                                await delete('pool_field', 'bind', pool_id)
                                await posted.delete()
                                await shared.delete()
                    elif text.lower() == 'ko\'rish':
                        fields_list = [i.get('name') for i in fields]
                        markup = await btn_inline(data=fields_list, row=1)
                        await maker(chat=chat.id, text=text_body, markup=markup, file=file, file_type=file_type)
                else:
                    await message.answer("Maydon kiritin...")
            else:
                data['pool_field'].append({'name': text,
                                           'voted': 0,
                                           'bind': pool_id})
                fields = data.as_dict().get('pool_field')
                if len(fields) == 2:
                    cancel = await btn_cancel(['Jo\'natish', 'Ko\'rish'])
                    await message.answer("1.Hamma maydonlarni kiritib bo'lgach "
                                         "<b>Jo'natish</b> tugmasini bossangiz ushbu"
                                         "so'rovnoma saqlab olinadi va kanalga jo'natiladi\n\n"
                                         "2.Agar so\'rovnoma qanday bo\'lishini oldindan ko\'rmoqchi bo'lsangiz "
                                         "<b>Ko\'rish</b> tugmasini bosing va yana "
                                         "maydon kiritishda davom etishingiz mumkun\n\n"
                                         "3.Agar bekor qilmoqchi bo'lsangiz <b>Bekor qilish</b> tugmasini bossangiz ushbu "
                                         "so'rovnoma o'chib ketadi va kanalga ham jo'natilmaydi\n\n",
                                         reply_markup=cancel)
                else:
                    await message.answer("Maydon kiritin...")
        else:
            await delete('pool', 'id', pool_id)
            await delete('pool_field', 'bind', pool_id)
            data.clear()
            menu = await btn_menu()
            await state.finish()
            await message.reply("Bekor qilindi!", reply_markup=menu)


@dp.message_handler(state=Question.name)
async def question_name(message: types.Message, state: FSMContext):
    text = message.text
    if len(text) > 40:
        await message.answer("Nom ko'pi bilan 40ta belgi bo'lishi kerak iltimos qaytadan kiritin.")
    else:
        async with state.proxy() as data:
            data['name'] = text
        await Question.next()
        await message.answer("Savol uchun rasm, video yoki fayl jo'nating agar "
                             "savolda rasm, video yoki fayl bo\'lishini hohlamasangiz"
                             "savol matnini kiritishingiz mumkun ushbu matn"
                             "savol tepasida ko\'rinib turadi.")


@dp.message_handler(content_types=types.ContentTypes.PHOTO, state=Question.file_id)
async def question_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1]
    async with state.proxy() as data:
        data['file_id'] = photo.file_id
        data['file_type'] = 'photo'
    await Question.next()
    await message.answer("Savolni kiritishingiz mumkun ushbu matn savol tepasida ko\'rinib turadi.")


@dp.message_handler(content_types=types.ContentTypes.VIDEO, state=Question.file_id)
async def question_video(message: types.Message, state: FSMContext):
    video = message.video
    file_id = video.file_id
    async with state.proxy() as data:
        data['file_id'] = file_id
        data['file_type'] = 'video'
    await Question.next()
    await message.answer("Savolni kiritishingiz mumkun ushbu matn savol tepasida ko\'rinib turadi.")


@dp.message_handler(content_types=types.ContentTypes.DOCUMENT, state=Question.file_id)
async def question_document(message: types.Message, state: FSMContext):
    document = message.document
    file_id = document.file_id
    async with state.proxy() as data:
        data['file_id'] = file_id
        data['file_type'] = 'document'
    await Question.next()
    await message.answer("Savolni kiritishingiz mumkun ushbu matn savol tepasida ko\'rinib turadi.")


@dp.message_handler(state=Question.file_id)
async def question_fileid_override(message: types.Message, state: FSMContext):
    text = message.text
    async with state.proxy() as data:
        data['text_visible'] = text
    await Question.text_hidden.set()
    await message.answer("Savol javobini kiritishingiz mumkun 100ta belgidan oshmasligi kerak.")


@dp.message_handler(state=Question.text_visible)
async def question_text_visible(message: types.Message, state: FSMContext):
    text = message.text
    async with state.proxy() as data:
        data['text_visible'] = text
    await Question.next()
    await message.answer("Savol javobini kiritishingiz mumkun 100ta belgidan oshmasligi kerak.")


@dp.message_handler(state=Question.text_hidden)
async def question_text_hidden(message: types.Message, state: FSMContext):
    text = message.text
    async with state.proxy() as data:
        data['text_hidden'] = text
    await Question.next()
    await message.answer("Savol javobini bilish tugmasi uchun matn kiritin ushbu matn 40ta belgidan oshmasligi kerak.")


@dp.message_handler(state=Question.button)
async def question_button(message: types.Message, state: FSMContext):
    text = message.text
    if len(text) > 40:
        await message.answer("Matn ko'pi bilan 40ta belgi bo'lishi kerak iltimos qaytadan kiritin.")
    else:
        async with state.proxy() as data:
            data['button'] = text
        await Question.next()
        back = await btn_back(['Ha', 'Yo\'q'])
        await message.answer("Savol javobini bilish uchun kanalga obuna bo\'lishi kerakmi?",
                             reply_markup=back)


@dp.message_handler(state=Question.check_user)
async def question_check_user(message: types.Message, state: FSMContext):
    text = message.text.lower()
    if text in ['ha', 'yo\'q']:
        async with state.proxy() as data:
            if text == 'ha':
                data['check_user'] = True
            else:
                data['check_user'] = False
        await Question.next()
        back = await btn_back(['Jo\'natish', 'Ko\'rish'])
        await message.answer("1.Agar <b>Jo'natish</b> tugmasini bossangiz ushbu "
                             "savol saqlab olinadi va kanalga jo'natiladi\n\n"
                             "2.Agar savol qanday bo\'lishini oldindan ko\'rmoqchi bo'lsangiz "
                             "<b>Ko\'rish</b> tugmasini bosing va yana\n\n"
                             "3.Agar bekor qilmoqchi bo"
                             "'lsangiz <b>Orqaga</b> tugmasini bossangiz ushbu "
                             "so'rovnoma o'chib ketadi va kanalga ham jo'natilmaydi\n\n", reply_markup=back)
    else:
        back = await btn_back(['Ha', 'Yo\'q'])
        await message.answer("Savol javobini bilish uchun kanalga obuna bo\'lishi kerakmi?",
                             reply_markup=back)


@dp.message_handler(state=Question.action)
async def question_check_user(message: types.Message, state: FSMContext):
    text = message.text
    async with state.proxy() as data:
        if text.lower() in ['jo\'natish', 'ko\'rish']:
            as_dict = data.as_dict()
            file = as_dict.get('file_id')
            file_type = as_dict.get('file_type')
            text_body = as_dict.get('text_visible')
            button = as_dict.get('button')
            if text.lower() == 'jo\'natish':
                await state.finish()
                data.clear()
                menu = await btn_menu()
                new_question = await create('question', as_dict)
                if new_question:
                    markup = await btn_answer(button, callback=f"question_answer_{new_question}")
                    posted = await maker(CHANEL, text_body, markup, file, file_type)
                    msg_id = posted.message_id
                    set_msg_id = await set_message_id('question', msg_id, new_question)
                    if set_msg_id:
                        markup_url = await btn_inline_url([button], url=[f"https://t.me/{CHANEL[1:]}/{msg_id}"])
                        await maker(message.chat.id, text_body, markup_url, file, file_type)
                        await message.answer("Jo\'natildi 👆ushbu postni reklama qila olasiz.",
                                             reply_markup=menu)
                    else:
                        await message.answer("Nimadur hato ketdi iltimos boshqatdan kiritib chiqing!",
                                             reply_markup=menu)
                        await posted.delete()
                        await delete('question', 'id', new_question)
                else:
                    await message.answer("Nimadur hato ketdi iltimos boshqatdan kiritib chiqing!",
                                         reply_markup=menu)
            else:
                await Question.next()
                markup = await btn_answer(button, callback='view_question')
                await maker(message.chat.id, text_body, markup, file, file_type)
        else:
            back = await btn_back(['Jo\'natish', 'Ko\'rish'])
            await message.answer("1.Agar <b>Jo'natish</b> tugmasini bossangiz ushbu "
                                 "savol saqlab olinadi va kanalga jo'natiladi\n\n"
                                 "2.Agar savol qanday bo\'lishini oldindan ko\'rmoqchi bo'lsangiz "
                                 "<b>Ko\'rish</b> tugmasini bosing va yana\n\n"
                                 "3.Agar bekor qilmoqchi bo"
                                 "'lsangiz <b>Orqaga</b> tugmasini bossangiz ushbu "
                                 "so'rovnoma o'chib ketadi va kanalga ham jo'natilmaydi\n\n", reply_markup=back)


@dp.callback_query_handler(lambda callback: callback.data == 'view_question', state=Question.view)
async def question_view(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        as_dict = data.as_dict()
        text_hidden = as_dict.get('text_hidden')
        await bot.answer_callback_query(callback.id, text_hidden, show_alert=True)


@dp.message_handler(state=Question.view)
async def question_view_back(message: types.Message, state: FSMContext):
    await Question.previous()
    await question_check_user(message, state)
