from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_full_text_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    back_btn = KeyboardButton(text='◀️ Back')
    cancel_btn = KeyboardButton(text='❌ Cancel')
    keyboard.add(back_btn)
    keyboard.add(cancel_btn)

    return keyboard
