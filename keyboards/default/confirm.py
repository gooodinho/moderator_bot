from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_confirm_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    yes_btn = KeyboardButton(text='✅ Yes')
    no_btn = KeyboardButton(text='🚫 No')
    cancel_btn = KeyboardButton(text='❌ Cancel')
    keyboard.insert(yes_btn)
    keyboard.insert(no_btn)
    keyboard.add(cancel_btn)

    return keyboard
