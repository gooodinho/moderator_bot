from aiogram.dispatcher.filters import Command

from filters.is_admin import AdminFilter
from loader import dp, db
from aiogram import types


@dp.message_handler(AdminFilter(), Command('add_admin'))
async def add_admin(message: types.Message):
    pass
