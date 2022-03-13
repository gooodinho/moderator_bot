from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


shortcut_edit_callback = CallbackData('sc', 'to_edit', 'id')


def get_sc_edit_keyboard(sc_id: int):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Edit Short",
                                 callback_data=shortcut_edit_callback.new(to_edit='short', id=sc_id))
        ],
        [
            InlineKeyboardButton(text="Edit Full Text",
                                 callback_data=shortcut_edit_callback.new(to_edit='full', id=sc_id))
        ],
        [
            InlineKeyboardButton(text="◀️ Back", callback_data=shortcut_edit_callback.new(to_edit='back', id=sc_id))
        ]
    ])

    return markup
