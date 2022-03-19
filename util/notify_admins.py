from aiogram import Dispatcher

from keyboards.default.main import get_main_keyboard
from loader import db
from util.misc.logging import logger


async def on_startup_notify(dp: Dispatcher):
    admins = await db.get_admins()
    for admin in admins:
        try:
            await dp.bot.send_message(admin.get('telegram_id'), 'The bot is up and running',
                                      reply_markup=get_main_keyboard())
        except Exception as err:
            logger.exception(err)
