import logging

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from data import config
from filters import IsPrivate
from filters.is_admin import AdminFilter
from keyboards.default.cancel import get_cancel_keyboard
from keyboards.default.confirm import get_confirm_keyboard
from keyboards.default.full_text import get_full_text_keyboard
from keyboards.default.main import get_main_keyboard
from keyboards.inline.shortcut_edit import get_sc_edit_keyboard, shortcut_edit_callback
from keyboards.inline.shortcut_info import get_sc_info_keyboard, shortcut_info_callback
from keyboards.inline.shortcut_pagination import get_sc_pagination_keyboard, shortcut_callback, pagination_callback
from loader import dp, db
from aiogram import types

from states.new_shortcut import NewShortcut
from util import get_random_string
from util.misc.logging import logger


@dp.message_handler(Command('add_admin'), IsPrivate(), AdminFilter())
async def add_admin(message: types.Message):
    admin = await db.select_admin(telegram_id=message.from_user.id)
    admin_id = admin.get("id")
    ref_string = get_random_string(15)
    ref_link = f"https://t.me/{config.BOT_USERNAME}?start=" + ref_string
    result = await db.add_link(ref_string, admin_id)
    if result:
        await message.answer("Your link to add a new admin, it will only work for one user.\n"
                             f"\n{ref_link}")
        logger.info(f"Admin ({admin.get('user_name')}) has created new \'add admin\' link")
    else:
        admin_link = await db.get_admin_link(admin_id)
        await message.answer("You have already had active add link"
                             f"\n\nhttps://t.me/{config.BOT_USERNAME}?start={admin_link.get('code')}")


@dp.message_handler(IsPrivate(), AdminFilter(), text='✍️ Add shortcut')
async def add_shortcut(message: types.Message):
    await message.answer('Send short command:', reply_markup=get_cancel_keyboard())
    await NewShortcut.Short.set()


@dp.message_handler(IsPrivate(), AdminFilter(), state=NewShortcut.Short)
async def get_shortcut(message: types.Message, state: FSMContext):
    if message.text == "❌ Cancel":
        await state.finish()
        await message.answer("Action cancelled", reply_markup=get_main_keyboard())
    else:
        if ' ' in message.text:
            await message.answer('Shortcut must be without spaces')
        else:
            exists_shortcut = await db.select_shortcut(short=message.text)
            if exists_shortcut is not None:
                await message.answer('This shortcut already exists. Try another one')
            else:
                await state.update_data(short=message.text)
                await message.answer('Send the text to replace the shortcut:', reply_markup=get_full_text_keyboard())
                await NewShortcut.FullText.set()


@dp.message_handler(IsPrivate(), AdminFilter(), state=NewShortcut.FullText)
async def get_full_text(message: types.Message, state: FSMContext):
    if message.text == "❌ Cancel":
        await state.finish()
        await message.answer("Action cancelled", reply_markup=get_main_keyboard())
    elif message.text == "◀️ Back":
        await add_shortcut(message)
    else:
        full_text = message.parse_entities()
        if len(full_text) >= 4096:
            await message.answer('Full text is too long! Write something shorter')
            logger.warning("Trying to add shortcut with too long full text!")
        else:
            await state.update_data(full_text=full_text)
            await NewShortcut.Confirm.set()
            await message.answer('Confirm the action on the keyboard', reply_markup=get_confirm_keyboard())


@dp.message_handler(IsPrivate(), AdminFilter(), state=NewShortcut.Confirm)
async def confirm_add_shortcut(message: types.Message, state: FSMContext):
    if message.text == "✅ Yes":
        data = await state.get_data()
        short, full_text = data.get('short'), data.get('full_text')
        await db.add_shortcut(short, full_text)
        logger.info(f"Add new shortcut ({short})")
        await state.finish()
        await message.answer('The shortcut was successfully added 🎉', reply_markup=get_main_keyboard())

    elif message.text == "🚫 No":
        await message.answer('Send the text to replace the shortcut:', reply_markup=get_full_text_keyboard())
        await NewShortcut.FullText.set()

    elif message.text == "❌ Cancel":
        await state.finish()
        await message.answer("Action cancelled", reply_markup=get_main_keyboard())


@dp.message_handler(IsPrivate(), AdminFilter(), text='↙️ Show all shortcuts')
async def show_all_shortcuts(message: types.Message):
    max_pages = await db.count_shortcut_pages()
    shortcuts = await db.select_shortcuts_range(1)
    await message.answer("All shortcuts:", reply_markup=get_sc_pagination_keyboard(shortcuts, 1, max_pages))


@dp.callback_query_handler(pagination_callback.filter())
async def get_new_page(call: types.CallbackQuery, callback_data: dict):
    await call.answer(cache_time=4)
    page = callback_data.get('page')
    if page == "current":
        pass
    elif page == "delete":
        await call.message.delete()
    else:
        page = int(page)
        max_pages = await db.count_shortcut_pages()
        shortcuts = await db.select_shortcuts_range(page)
        await call.message.edit_reply_markup(reply_markup=get_sc_pagination_keyboard(shortcuts, page, max_pages))


@dp.callback_query_handler(shortcut_callback.filter())
async def show_shortcut_info(call: types.CallbackQuery, callback_data: dict):
    await call.answer(cache_time=4)
    sc_id = int(callback_data.get("id"))
    shortcut = await db.select_shortcut(id=sc_id)
    sc_info = f"""SHORTCUT INFO
\n📍Short: {shortcut.get('short')}
\n📍Full text: \n\n{shortcut.get('full_text')}
"""
    await call.message.delete()
    await call.message.answer(sc_info, reply_markup=get_sc_info_keyboard(sc_id))


@dp.callback_query_handler(shortcut_info_callback.filter(action='edit'))
async def edit_shortcut_start(call: types.CallbackQuery, callback_data: dict):
    sc_id = int(callback_data.get("id"))
    await call.message.edit_reply_markup(reply_markup=get_sc_edit_keyboard(sc_id))


@dp.callback_query_handler(shortcut_info_callback.filter(action='delete'))
async def delete_shortcut_start(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    sc_id = int(callback_data.get("id"))
    await call.message.delete()
    await state.set_state('delete_short_confirm')
    await state.update_data(sc_id=sc_id)
    await call.message.answer('Confirm the action on the keyboard', reply_markup=get_confirm_keyboard())


@dp.message_handler(IsPrivate(), state='delete_short_confirm')
async def delete_shortcut(message: types.Message, state: FSMContext):
    data = await state.get_data()
    sc_id = data.get("sc_id")
    shortcut = await db.select_shortcut(id=sc_id)
    short = shortcut.get('short')
    if message.text == "✅ Yes":
        await db.delete_shortcut(sc_id, short)
        logger.info(f'Shortcut ({short}) was deleted')
        await state.finish()
        await message.answer(f'The shortcut was successfully deleted 🦄',
                             reply_markup=get_main_keyboard())
    elif message.text == "🚫 No" or message.text == "❌ Cancel":
        sc_info = f"""SHORTCUT INFO
         \n📍Short: {short}
         \n📍Full text: \n\n{shortcut.get('full_text')}
         """
        await state.finish()
        await message.answer("Action canceled", reply_markup=get_main_keyboard())
        await message.answer(sc_info, reply_markup=get_sc_info_keyboard(sc_id))


@dp.callback_query_handler(shortcut_info_callback.filter(action='back'))
async def back_from_info(call: types.CallbackQuery):
    await call.message.delete()
    await show_all_shortcuts(call.message)


@dp.callback_query_handler(shortcut_edit_callback.filter())
async def edit_shortcut_choose(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    to_edit = callback_data.get('to_edit')
    sc_id = int(callback_data.get('id'))
    shortcut = await db.select_shortcut(id=sc_id)
    if to_edit == 'back':
        await call.message.edit_reply_markup(reply_markup=get_sc_info_keyboard(sc_id))
    elif to_edit == 'short':
        await state.set_state('edit_short')
        await state.update_data(sc_id=sc_id)
        await call.message.delete()
        await call.message.answer(f"Send new Short\n\nOld Short - {shortcut.get('short')}",
                                  reply_markup=get_cancel_keyboard())
    elif to_edit == 'full':
        await state.set_state('edit_full')
        await state.update_data(sc_id=sc_id)
        await call.message.delete()
        await call.message.answer(f"Send new Full text\n\nOld Full text\n{shortcut.get('full_text')}",
                                  reply_markup=get_cancel_keyboard())


@dp.message_handler(IsPrivate(), state='edit_short')
async def edit_short(message: types.Message, state: FSMContext):
    data = await state.get_data()
    sc_id = data.get("sc_id")
    if message.text == '❌ Cancel':
        shortcut = await db.select_shortcut(id=sc_id)
        sc_info = f"""SHORTCUT INFO
        \n📍Short: {shortcut.get('short')}
        \n📍Full text: \n\n{shortcut.get('full_text')}
        """
        await state.finish()
        await message.answer("Action canceled", reply_markup=get_main_keyboard())
        await message.answer(sc_info, reply_markup=get_sc_edit_keyboard(sc_id))
    else:
        if ' ' in message.text:
            await message.answer('Shortcut must be without spaces')
        else:
            shortcut = await db.select_shortcut(short=message.text)
            if shortcut is not None:
                await message.answer('This shortcut already exists, try another one')
            else:
                await state.update_data(short=message.text)
                await state.set_state('edit_short_confirm')
                await message.answer('Confirm the action on the keyboard', reply_markup=get_confirm_keyboard())


@dp.message_handler(IsPrivate(), state='edit_full')
async def edit_full(message: types.Message, state: FSMContext):
    data = await state.get_data()
    sc_id = data.get("sc_id")
    shortcut = await db.select_shortcut(id=sc_id)
    if message.text == '❌ Cancel':
        sc_info = f"""SHORTCUT INFO
         \n📍Short: {shortcut.get('short')}
         \n📍Full text: \n\n{shortcut.get('full_text')}
         """
        await state.finish()
        await message.answer("Action canceled", reply_markup=get_main_keyboard())
        await message.answer(sc_info, reply_markup=get_sc_edit_keyboard(sc_id))
    else:
        full_text = message.parse_entities()
        if len(full_text) >= 4096:
            await message.answer('Full text is too long! Write something shorter')
            logger.warning('Trying to EDIT shortcut with too long text')
        else:
            await state.update_data(full_text=full_text)
            await state.set_state('edit_full_confirm')
            await message.answer('Confirm the action on the keyboard', reply_markup=get_confirm_keyboard())


@dp.message_handler(IsPrivate(), state='edit_short_confirm')
async def confirm_edit(message: types.Message, state: FSMContext):
    data = await state.get_data()
    sc_id, short = data.get("sc_id"), data.get('short')
    shortcut = await db.select_shortcut(id=sc_id)
    if message.text == "✅ Yes":
        await db.edit_shortcut_short(short, sc_id)
        await state.finish()
        old_short = shortcut.get("short")
        logger.info(f'The shortcut ({old_short}->{short}) was successfully updated')
        await message.answer(f'The shortcut ({old_short}->{short}) was successfully updated 🦄',
                             reply_markup=get_main_keyboard())

    elif message.text == "🚫 No":
        await message.answer('Send new Short', reply_markup=get_cancel_keyboard())
        await state.set_state('edit_short')

    elif message.text == "❌ Cancel":
        sc_info = f"""SHORTCUT INFO
         \n📍Short: {shortcut.get('short')}
         \n📍Full text: \n\n{shortcut.get('full_text')}
         """
        await state.finish()
        await message.answer("Action canceled", reply_markup=get_main_keyboard())
        await message.answer(sc_info, reply_markup=get_sc_edit_keyboard(sc_id))


@dp.message_handler(IsPrivate(), state='edit_full_confirm')
async def confirm_edit(message: types.Message, state: FSMContext):
    data = await state.get_data()
    sc_id, full_text = data.get("sc_id"), data.get('full_text')
    shortcut = await db.select_shortcut(id=sc_id)
    if message.text == "✅ Yes":
        await db.edit_shortcut_full_text(full_text, sc_id)
        await state.finish()
        logger.info(f'The shortcut ({shortcut.get("short")}) full text was successfully updated')
        await message.answer(f'The shortcut Full Text was successfully updated 🦄',
                             reply_markup=get_main_keyboard())
    elif message.text == "🚫 No":
        await message.answer('Send new Full Text', reply_markup=get_cancel_keyboard())
        await state.set_state('edit_full')

    elif message.text == "❌ Cancel":
        sc_info = f"""SHORTCUT INFO
         \n📍Short: {shortcut.get('short')}
         \n📍Full text: \n\n{shortcut.get('full_text')}
         """
        await state.finish()
        await message.answer("Action canceled", reply_markup=get_main_keyboard())
        await message.answer(sc_info, reply_markup=get_sc_edit_keyboard(sc_id))
