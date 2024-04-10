from typing import Any, Dict, Optional, Union
from aiogram.types import Message, User
from aiogram.filters import Filter
from aiogram import Bot, types
from aiogram.types import Message, Update
from aiogram.types.chat_member_left import ChatMemberLeft

class IsChatMember(Filter):
    def __init__(self, name: Optional[str] = None) -> None:
        self.name = name

    async def __call__(
        self,
        update: Update,
        event_from_user: User
        # Filters also can accept keyword parameters like in handlers
    ) -> bool:
        user_channel_status = await bot.get_chat_member(chat_id=CONFIG.tg_bot.public_name,
                                                            user_id=user_id)
        if type(user_channel_status) == ChatMemberLeft:
            return True
        else :
            return False