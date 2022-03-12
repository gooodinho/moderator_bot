from aiogram import Dispatcher
from .is_admin import AdminFilter
from .chat_type import IsGroup, IsPrivate


def setup(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsPrivate)
