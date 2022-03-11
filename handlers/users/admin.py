from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from data import config
from filters.is_admin import AdminFilter
from loader import dp, db
from aiogram import types

from util import get_random_string


@dp.message_handler(AdminFilter(), Command('add_admin'))
async def add_admin(message: types.Message):
    ref_string = get_random_string(15)
    ref_link = f"https://t.me/{config.BOT_USERNAME}?start=" + ref_string
    await message.answer("Your link to add a new admin, it will only work for one user.\n"
                         f"\n{ref_link}")
