import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode

from database.engine import session_maker
from middlewares.users import UpdateUser
from handlers.user_private import user_private_router
from config.config import CONFIG

#from handlers.user_group import user_group_router

logger = logging.getLogger(__name__)

async def main():
    # logging.basicConfig(level=logging.WARNING,
    #                     filename="ba_guide.log",
    #                     format='%(filename)s:%(lineno)d #%(levelname)-8s'
    #                             '[%(active)s] - %(name)s - %(message)s')
    # logger.info("starting bot")

    bot = Bot(token=CONFIG.tg_bot.token)
    bot.my_admins_list = []

    dp = Dispatcher()

    dp.include_router(user_private_router)

    # dp.startup.register(on_startup)
    # dp.shutdown.register(on_shutdown)

    dp.update.middleware(UpdateUser(session_pool=session_maker, bot = bot))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())
