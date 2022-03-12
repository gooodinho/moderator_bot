from aiogram.dispatcher.filters.state import StatesGroup, State


class NewShortcut(StatesGroup):
    Short = State()
    FullText = State()
    Confirm = State()
