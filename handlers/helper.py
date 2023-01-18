from loader import bot


async def maker(chat, text, markup, file=None, file_type=None):
    text_code = text.replace(r'\n', '\n')
    if file_type and file:
        if file_type == "photo":
            posted = await bot.send_photo(chat_id=chat, photo=file, caption=text_code, reply_markup=markup)
        elif file_type == "video":
            posted = await bot.send_video(chat_id=chat, video=file, caption=text_code, reply_markup=markup)
        elif file_type == "document":
            posted = await bot.send_document(chat_id=chat, document=file, caption=text_code, reply_markup=markup)
        else:
            posted = None
    else:
        posted = await bot.send_message(chat_id=chat, text=text_code, reply_markup=markup)

    return posted
