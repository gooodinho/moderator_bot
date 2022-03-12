from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_cancel_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    cancel_btn = KeyboardButton(text='❌ Cancel')
    keyboard.add(cancel_btn)

    return keyboard
