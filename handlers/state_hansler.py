from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from buttons.button import menu, save_send_back, pool
from utils.states import Poll
from utils.db import create, delete, set_mes_id
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
                                 "olinadi kanalga jo'natilmaydi buni keyinchalik jo'natishingiz mumkun.\n"
                                 "2.Kiritib bo'lgach <b>Jo'natish</b> tugmasini bossangiz ushbu so'rovnoma saqlab "
                                 "olinadi va kanalga jo'natiladi\n"
                                 "3.Agar bekor qilmoqchi bo'lsangiz <b>Bekor qilish</b> tugmasini bossangiz ushbu "
                                 "so'rovnoma o'chib ketadi va kanalga ham jo'natilmaydi\n ",
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
            text_pool = pool_data.get("text")
            pool_button = pool_data.get("kb")
            mes = await bot.send_message(CHANEL, text_pool, reply_markup=pool_button)
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
