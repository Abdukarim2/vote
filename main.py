from aiogram import executor
from loader import dp
from handlers import message_handler, error_handler
from utils.db import init


async def start_up(_):
    print("start up")
    init()


async def shut_down(_):
    print("shut down")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False, on_startup=start_up, on_shutdown=shut_down)
