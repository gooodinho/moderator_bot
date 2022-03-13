from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


shortcut_info_callback = CallbackData('sc', 'action', 'id')


def get_sc_info_keyboard(sc_id: int):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✏️ Edit",
                                 callback_data=shortcut_info_callback.new(action='edit', id=sc_id)),
            InlineKeyboardButton(text="🗑 Delete",
                                 callback_data=shortcut_info_callback.new(action='delete', id=sc_id))
        ],
        [
            InlineKeyboardButton(text="◀️ Back", callback_data=shortcut_info_callback.new(action='back', id=sc_id))
        ]
    ])

    return markup
