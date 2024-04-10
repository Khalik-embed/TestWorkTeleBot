from typing import Any, Awaitable, Callable, Dict
from aiogram.types.chat_member_left import ChatMemberLeft

from aiogram import BaseMiddleware, Bot
from aiogram.types import Message, TelegramObject

from sqlalchemy.ext.asyncio import async_sessionmaker

from lexicon.lexicon_ru import BOT_MESSAGES
from config.config import CONFIG
from database.orm_query import orm_check_if_user_exist, orm_add_user, orm_update_user

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

        [chat_id, user_name, user_id] = get_user_name_user_id(event)
        if chat_id and user_id:
            user_channel_status = await self.bot.get_chat_member(chat_id=CONFIG.tg_bot.public_name,
                                                            user_id=user_id)
            if type(user_channel_status) == ChatMemberLeft:
                await self.bot.send_message(chat_id = chat_id, text = BOT_MESSAGES['subscrion_required'])
            else :
                #await  self.bot.send_message(chat_id = chat_id, text = "hello1")
                await handler(event, data)
                exist = await orm_check_if_user_exist(self.session_pool, int(user_id))
                if exist == False:
                    await orm_add_user(self.session_pool, int(user_id), user_name)
                else:
                    await orm_update_user(self.session_pool, int(user_id), user_name)







def get_user_name_user_id(event: TelegramObject) -> [str, str]:
    user_name = None
    user_id = None
    chat_id = None
    if (hasattr(event, "message")
        and hasattr(event.message, "from_user")
        and hasattr(event.message.from_user, "id")):
        user_id = event.message.from_user.id
        if hasattr(event.message.from_user, "username"):
            user_name = event.message.from_user.username
        if hasattr(event.message, "chat"):
            chat_id = event.message.chat.id
    return [chat_id, user_name, user_id]

# class UpdateUser(BaseMiddleware):
#     # def __init__(self, session_pool: async_sessionmaker):
#     #     self.session_pool = session_pool
#     def __init__(self):
#     #     self.session_pool = session_pool


#     async def __call__(
#         self,
#         handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
#         event: TelegramObject,
#         data: Dict[str, Any],
#     ) -> Any:
#         async with self.session_pool() as session:
#             data['session'] = session
#             return await handler(event, data)


# class CounterMiddleware(BaseMiddleware):
#     def __init__(self) -> None:
#         self.counter = 0

#     async def __call__(
#         self,
#         handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
#         event: TelegramObject,
#         data: Dict[str, Any]
#     ) -> Any:
#         self.counter += 1
#         data['counter'] = self.counter
#         return await handler(event, data)