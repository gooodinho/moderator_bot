from aiogram.dispatcher.filters import Command

from data import config
from filters.is_admin import AdminFilter
from loader import dp, db
from aiogram import types

from util import get_random_string


@dp.message_handler(AdminFilter(), Command('add_admin'))
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
