from typing import Any, Awaitable, Callable, Dict
from aiogram.types.chat_member_left import ChatMemberLeft

from aiogram import BaseMiddleware, Bot
from aiogram.types import Message, TelegramObject

from sqlalchemy.ext.asyncio import async_sessionmaker

from config.config import CONFIG
from database.orm_query import orm_check_if_user_exist, orm_add_user, orm_update_user, orm_get_dont_sended_mailing, orm_get_user_ids, orm_set_sended_mailing
from handlers.menu_processing import  subscription_requriment_send
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
scheduler = AsyncIOScheduler(timezone ="America/Sao_Paulo")

scheduler.start()

async def start_mailing(bot,async_session,  mailing):
    print("gopa")
    users= await orm_get_user_ids(async_session)
    print(users)
    for user in users:
        await bot.send_message(user, mailing.mailling_text)
    await orm_set_sended_mailing(async_session, mailing)


def schedule_message(bot, async_session, text, date_time):
    scheduler.add_job(start_mailing, 'date', run_date=date_time, args=(bot, async_session,  text))
    print(datetime.now())



class UpdateUser(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker, bot :Bot):
        self.session_pool = session_pool
        self.bot = bot
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        [chat_id, user_name, user_id, chat_type] = get_user_name_user_id(event)

        if chat_type in ['private', 'pre_checkout_query', 'shipping_query', 'inline_query']:
            if chat_id:
                user_channel_status = await self.bot.get_chat_member(chat_id=CONFIG.tg_bot.public_name,
                                                            user_id=user_id)
                if type(user_channel_status) == ChatMemberLeft:
                    await subscription_requriment_send(self.session_pool, self.bot, chat_id)
                    return
            data['session_pool'] = self.session_pool
            await handler(event, data)

            if user_name:
                exist = await orm_check_if_user_exist(self.session_pool, int(user_id))
                if exist == False:
                    await orm_add_user(self.session_pool, int(user_id), user_name)
                else:
                    await orm_update_user(self.session_pool, int(user_id), user_name)

            mailings = await orm_get_dont_sended_mailing(self.session_pool)
            for mailing in mailings:
                print(mailing.mailling_text)
                print(mailing.time_to_send)
                await start_mailing(bot = self.bot, async_session = self.session_pool, mailing=mailing)


def get_user_name_user_id(event: TelegramObject) -> [str, str]:
    user_name = None
    user_id = None
    chat_id = None
    chat_type = None
    print(event)

    if (hasattr(event, "message")
        and hasattr(event.message, "from_user")
        and hasattr(event.message.from_user, "id")):
        chat_type = event.message.chat.type
        user_id = event.message.from_user.id
        if hasattr(event.message.from_user, "username"):
            user_name = event.message.from_user.username
        if hasattr(event.message, "chat"):
            chat_id = event.message.chat.id

    elif (hasattr(event, "callback_query")
        and hasattr(event.callback_query, "from_user")
        and hasattr(event.callback_query.from_user, "id")):

        chat_type = event.callback_query.message.chat.type
        user_id = event.callback_query.from_user.id

        if hasattr(event.callback_query.from_user, "username"):
            user_name = event.callback_query.from_user.username
        if hasattr(event.callback_query.message, "chat"):
            chat_id = event.callback_query.message.chat.id

    elif (hasattr(event, "pre_checkout_query")
        and hasattr(event.pre_checkout_query, "from_user")
        and hasattr(event.pre_checkout_query.from_user, "id")):

        chat_type = "pre_checkout_query"
        user_id = event.pre_checkout_query.from_user.id
        if hasattr(event.pre_checkout_query.from_user, "username"):
            user_name = event.pre_checkout_query.from_user.username

    elif (hasattr(event, "shipping_query")
        and hasattr(event.shipping_query, "from_user")
        and hasattr(event.shipping_query.from_user, "id")):

        chat_type = "shipping_query"
        user_id = event.shipping_query.from_user.id
        if hasattr(event.shipping_query.from_user, "username"):
            user_name = event.shipping_query.from_user.username

    elif (hasattr(event, "inline_query")
        and hasattr(event.inline_query, "from_user")
        and hasattr(event.inline_query.from_user, "id")):

        chat_type = "inline_query"
        user_id = event.inline_query.from_user.id
        if hasattr(event.inline_query.from_user, "username"):
            user_name = event.inline_query.from_user.username

    return [chat_id, user_name, user_id, chat_type]
