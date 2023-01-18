import asyncio
from aiogram import executor, types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
from loader import dp, bot
from configs.config import ADMINS
from utils.db import init
from editor import update_loop
import handlers


class AuthMiddleware(BaseMiddleware):
    # Filters
    async def on_process_message(self, message: types.Message, data: dict):
        user = message.chat
        data["middleware_data"] = user.id
        if user.id in ADMINS:
            return True
        else:
            await message.answer("Siz admin emassiz!")
            raise CancelHandler()
    # Handlers


async def start_up(_):
    await init()
    event_loop = asyncio.get_event_loop()
    event_loop.create_task(update_loop())
    print("start up ...")


async def shut_down(_):
    try:
        await bot.send_message(1144957860, "Shut down")
    except Exception as e:
        pass
    print("shut down")


if __name__ == "__main__":
    dp.middleware.setup(AuthMiddleware())
    executor.start_polling(dp, on_startup=start_up, on_shutdown=shut_down)
