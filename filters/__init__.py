from aiogram import Dispatcher

from util.misc.logging import logger
from .is_admin import AdminFilter
from .chat_type import IsGroup, IsPrivate


def setup(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsPrivate)
    logger.info("Filters are set up")
