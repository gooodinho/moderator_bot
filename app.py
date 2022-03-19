from aiogram import executor
from loader import dp, db
from util.misc.logging import logger
from util.notify_admins import on_startup_notify


async def on_startup(dispatcher):
    import filters
    filters.setup(dp)
    await db.create()

    # await db.drop_table_admins()
    await db.create_table_admins()

    # await db.drop_table_links()
    await db.create_table_links()

    # await db.drop_table_shortcuts()
    await db.create_table_shortcuts()

    logger.info("Bot has been launched")
    await on_startup_notify(dp)

if __name__ == '__main__':
    from handlers import dp
    executor.start_polling(dp, on_startup=on_startup)
