from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from loader import db


class AdminFilter(BoundFilter):
    async def check(self, message: types.Message):
        get_admin = await db.select_admin(telegram_id=message.from_user.id)
        result = False if get_admin is None else True
        return result
