from loader import dp


@dp.errors_handler(exception=Exception)
async def error(message, exception):
    print(exception)
