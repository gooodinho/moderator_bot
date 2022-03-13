from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from asyncpg.protocol.protocol import Record

shortcut_callback = CallbackData('sc', 'page')


def get_sc_pagination_keyboard(shortcuts: List[Record], page: int, max_pages: int):
    prev_page = page - 1
    prev_page_text = "< "

    next_page = page + 1
    next_page_text = " >"

    first_page = 1
    first_page_text = "1 << "

    last_page = max_pages
    last_page_text = f" >> {max_pages}"

    markup = InlineKeyboardMarkup(row_width=5)

    for sc in shortcuts:
        sc_btn = InlineKeyboardButton(text=sc.get('short'), callback_data='*')
        markup.add(sc_btn)

    if prev_page - 1 > 0:
        markup.add(
            InlineKeyboardButton(
                text=first_page_text,
                callback_data=shortcut_callback.new(page=first_page)
            )
        )

    if prev_page > 0:
        prev_page_btn = InlineKeyboardButton(
                text=prev_page_text,
                callback_data=shortcut_callback.new(page=prev_page)
            )
        if prev_page - 1 > 0:
            markup.insert(prev_page_btn)
        else:
            markup.add(prev_page_btn)

    # if prev_page - 1 < 0:
    #     markup.add(
    #         InlineKeyboardButton(
    #             text=f"№ {page}",
    #             callback_data=shortcut_callback.new(page='current')
    #         )
    #     )

    # if prev_page - 1 > 0:
    #     markup.insert(
    #         InlineKeyboardButton(
    #             text=f"№ {page}",
    #             callback_data=shortcut_callback.new(page='current')
    #         )
    #     )

    current_page_btn = InlineKeyboardButton(text=f"№ {page}", callback_data=shortcut_callback.new(page='current'))

    if page == first_page:
        markup.add(current_page_btn)

    if page != first_page:
        markup.insert(current_page_btn)

    if next_page <= max_pages:
        markup.insert(
            InlineKeyboardButton(
                text=next_page_text,
                callback_data=shortcut_callback.new(page=next_page)
            )
        )
    if next_page + 1 <= max_pages:
        markup.insert(
            InlineKeyboardButton(
                text=last_page_text,
                callback_data=shortcut_callback.new(page=last_page)
            )
        )

    delete_btn = InlineKeyboardButton(
        text="❌",
        callback_data=shortcut_callback.new(page='delete')
    )

    markup.add(delete_btn)

    return markup
