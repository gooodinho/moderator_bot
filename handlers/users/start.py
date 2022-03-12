import logging

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data import config
from loader import dp, db, bot


@dp.message_handler(CommandStart())
async def start_msg(message: types.Message):
    msg_args = message.get_args()
    full_name, user_name, telegram_id = message.from_user.full_name,\
                                        message.from_user.username,\
                                        message.from_user.id
    is_admin = await db.check_admin(telegram_id)
    if is_admin:
        if msg_args:
            await message.answer('You are already admin. Welcome.')
        else:
            await message.answer('Hello admin')
    else:
        if str(telegram_id) in config.DEVELOPERS:
            await db.add_admin(full_name, user_name, telegram_id)
            await message.answer('You\'ve been promoted to admins')
            logging.info(f'Add new developer as admin - {user_name}')
        else:
            if msg_args:
                link = await db.select_link(code=msg_args)
                admin_id = link.get('admin_id')
                admin = await db.select_admin(id=admin_id)
                admin_tg_id = admin.get('telegram_id')
                admin_full_name = admin.get("full_name")
                await db.delete_link(msg_args, admin_id)
                logging.info(f"Remove {admin_full_name} \"add admin\" link")
                await db.add_admin(full_name, user_name, telegram_id)
                logging.info(f"Add new admin - {user_name}")
                await message.answer(f'You\'ve been promoted to admins by {admin_full_name}')
                await bot.send_message(admin_tg_id,
                                       text="Your 'add admin' link has been successfully used ✅")
            else:
                await message.answer('You aren\'t an admin')
