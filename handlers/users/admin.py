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
from loader import dp, db
from aiogram import types

from states.new_shortcut import NewShortcut
from util import get_random_string


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
        await state.update_data(full_text=message.parse_entities())
        await NewShortcut.Confirm.set()
        await message.answer('Confirm the action on the keyboard', reply_markup=get_confirm_keyboard())


@dp.message_handler(IsPrivate(), AdminFilter(), state=NewShortcut.Confirm)
async def confirm_add_shortcut(message: types.Message, state: FSMContext):
    if message.text == "✅ Yes":
        data = await state.get_data()
        short, full_text = data.get('short'), data.get('full_text')
        await db.add_shortcut(short, full_text)
        logging.info(f"add new shortcut - {short}")

        await message.answer('The shortcut was successfully added 🎉', reply_markup=get_main_keyboard())

    elif message.text == "🚫 No":
        await message.answer('Send the text to replace the shortcut:', reply_markup=get_full_text_keyboard())
        await NewShortcut.FullText.set()

    elif message.text == "❌ Cancel":
        await state.finish()
        await message.answer("Action cancelled", reply_markup=get_main_keyboard())


@dp.message_handler(IsPrivate(), AdminFilter(), text='↙️ Show all shortcuts')
async def show_all_shortcuts(message: types.Message):
    pass
