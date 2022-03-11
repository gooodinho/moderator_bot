import handlers
import logging
# from util.misc import logging
from aiogram import executor
from loader import dp, db


async def on_startup(dispatcher):
    import filters
    logging.info("Filters setup")
    filters.setup(dp)
    logging.info("Bot has been launched.")
    await db.create()
    logging.info("Connection created.")
    await db.create_table_admins()
    logging.info("Admin table created.")
    # await db.drop_table_admins()
    # await db.add_admin('test', 'test', 123123)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
