from aiogram.dispatcher.filters.state import State, StatesGroup


class Poll(StatesGroup):
    name = State()
    text = State()
    field = State()


class Post(StatesGroup):
    name = State()
    photo_id = State()
    text_visible = State()
    text_hidden = State()
    button = State()
    action = State()
