import asyncio
import logging

from aiogram import Bot, Dispatcher

from config.config import CONFIG
from middlewares.users_filtering import UpdateUser
from handlers.user_handlers import users_router
from handlers.payment import payment_router
from handlers.inline_mode import inline_router



logger = logging.getLogger(__name__)

async def main():
    bot : Bot = Bot(token=CONFIG.tg_bot.token)

    dp : Dispatcher = Dispatcher()

    dp.include_router(users_router)
    dp.include_router(inline_router)
    dp.include_router(payment_router)
    dp.update.middleware(UpdateUser(bot = bot))

    await bot.delete_webhook(drop_pending_updates = True)
    await dp.start_polling(
        bot,
        allowed_updates = ["message",
                           "edited_channel_post",
                           "callback_query",
                           "inline_query",
                           "chosen_inline_result",
                           "shipping_query",
                           "pre_checkout_query"])

asyncio.run(main())
