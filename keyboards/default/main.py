from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    add_btn = KeyboardButton(text='✍️ Add shortcut')
    all_btn = KeyboardButton(text='↙️ Show all shortcuts')
    keyboard.add(add_btn)
    keyboard.add(all_btn)

    return keyboard
