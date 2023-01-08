from aiogram.dispatcher.filters.state import State, StatesGroup


class Poll(StatesGroup):
    name = State()
    text = State()
    field = State()
