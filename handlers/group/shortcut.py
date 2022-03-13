from filters import AdminFilter, IsGroup
from loader import dp, db
from aiogram import types


@dp.message_handler(IsGroup(), AdminFilter(), regexp='^!\S*$')
async def change_shortcut(message: types.Message):
    await message.delete()
    short = message.text[1:]
    shortcut = await db.select_shortcut(short=short)
    await message.answer(shortcut.get('full_text'))
