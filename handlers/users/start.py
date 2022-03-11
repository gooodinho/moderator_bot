from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data import config
from loader import dp, db


@dp.message_handler(CommandStart())
async def start_msg(message: types.Message):
    full_name, user_name, telegram_id = message.from_user.full_name,\
                                        message.from_user.username,\
                                        message.from_user.id
    is_admin = await db.check_admin(telegram_id)
    if is_admin:
        await message.answer('Hello admin')
    else:
        if str(telegram_id) in config.DEVELOPERS:
            await db.add_admin(full_name, user_name, telegram_id)
            await message.answer('You\'ve been promoted to admins')
        else:
            await message.answer('You aren\'t an admin')
