from typing import Any, Awaitable, Callable, Dict
from aiogram.types.chat_member_left import ChatMemberLeft

from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject

from handlers.media_handlings import get_photo_id, set_photo_id
from config.config import CONFIG
from config.commands import BANNERS
from keyboards.inline import get_url_btns
from database.orm_query import (
    orm_check_if_user_exist,
    orm_add_user,
    orm_update_user,
    orm_get_user_ids,
    orm_get_dont_sended_mailing,
    orm_set_sended_mailing,
    orm_get_banner)
from database.models import Mailings


class UpdateUser(BaseMiddleware):
    def __init__(self, bot :Bot):
        self.bot = bot
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        [chat_id,   user_name,  user_id,    chat_type] = get_event_data(event)

        if chat_type in ['private', 'pre_checkout_query', 'shipping_query', 'inline_query']:
            is_chat_member = await subscibtion_protect(bot = self.bot, chat_type = chat_type, user_id = user_id)
            if not is_chat_member:
                return
            await handler(event, data)
            if user_id:
                await user_db_updating(user_name = user_name, user_id = user_id)
            await check_mailing(bot = self.bot)

def get_event_data(event: TelegramObject) -> [str | int | None]:
    user_name = None
    user_id = None
    chat_id = None
    chat_type = None

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

async def check_mailing(bot : Bot) -> None:
    mailings : [Mailings] = await orm_get_dont_sended_mailing()
    for mailing in mailings:
        await start_mailing(bot = bot, mailing = mailing)

async def start_mailing(bot : Bot, mailing : Mailings) -> None:
    users : [int] = await orm_get_user_ids()
    for user in users:
        if not mailing.photo:
            await bot.send_message(chat_id = user, text = mailing.mailling_text)
        else:
            photo_id = get_photo_id(orm_object = mailing)
            result  = await bot.send_photo(chat_id = user, photo = photo_id, parse_mode = 'HTML',
                                        caption =  mailing.mailling_text)
            await set_photo_id(orm_object = mailing, file_id = result.photo[0].file_id)
    await orm_set_sended_mailing(mailing)

async def subscibtion_protect(bot : Bot, chat_type : str | None,
                              user_id : str | int) -> bool:
    if chat_type == 'private':
        user_channel_status = await bot.get_chat_member(
            chat_id = CONFIG.tg_bot.public_name,
            user_id = user_id)

        if type(user_channel_status) == ChatMemberLeft:
            await subscription_requriment_send(bot = bot , chat_id = user_id)
            return False
    return True

async def user_db_updating(user_name : str, user_id : str | int) -> None:
    if user_name:
        exist = await orm_check_if_user_exist(user_id = user_id)
        if exist == False:
            await orm_add_user(user_id = int(user_id), user_name = user_name)
        else:
            await orm_update_user(user_id = int(user_id), user_name = user_name)


async def subscription_requriment_send(bot : Bot, chat_id : int | str):
    banner : Banners =  await orm_get_banner(slug = BANNERS.subscrion_required.name)
    if banner:
        text = banner.text
        buttons = {CONFIG.tg_bot.public_name : 'https://t.me/' + CONFIG.tg_bot.public_name[1:]}
        keyboard = get_url_btns(buttons, (1,))

        photo_id = get_photo_id(banner)
        result = await bot.send_photo(chat_id = chat_id, photo = photo_id, parse_mode = 'HTML',
            caption = text, reply_markup = keyboard)
        await set_photo_id(orm_object = banner, file_id = result.photo[0].file_id)
