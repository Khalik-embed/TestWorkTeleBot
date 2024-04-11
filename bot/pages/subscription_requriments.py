from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession
from database.orm_query import orm_get_banner
from database.models import Banners
from keyboards.inline import get_url_btns
from services.media_handlings import get_photo_id, set_photo_id
from config.config import CONFIG

async def subscription_requriment_send(async_session: AsyncSession, bot : Bot, chat_id : int | str):
    banner : Banners =  await orm_get_banner(async_session = async_session, slug = "subscrion_required")
    if banner:
        text = banner.text
        buttons = {CONFIG.tg_bot.public_name : 'https://t.me/' + CONFIG.tg_bot.public_name[1:]}
        keyboard = get_url_btns(buttons, (1,))
        photo_id = get_photo_id(banner)

        result = await bot.send_photo(chat_id = chat_id, photo=photo_id, parse_mode = 'HTML',
            caption = text, reply_markup=keyboard)

        if not  banner.photo_tg_id:
            await set_photo_id(async_session = async_session,
                           banner = banner,
                           file_id = result.photo[0].file_id)
    else:
        print("нет записи") #####
        return None
