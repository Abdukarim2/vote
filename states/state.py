from aiogram.dispatcher.filters.state import State, StatesGroup


class Pool(StatesGroup):
    name = State()
    file_id = State()
    text = State()
    button = State()
    check = State()
    field = State()


class Question(StatesGroup):
    name = State()
    file_id = State()
    text_visible = State()
    text_hidden = State()
    button = State()
    check_user = State()
    action = State()
    view = State()
