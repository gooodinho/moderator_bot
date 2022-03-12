from filters import AdminFilter, IsGroup
from loader import dp, db
from aiogram import types


@dp.message_handler(IsGroup(), AdminFilter(), regexp='^!\S*$')
async def change_shortcut(message: types.Message):
    pass
