from aiogram import F, types, Router, Bot
from aiogram.filters import CommandStart
from aiogram.types.chat_member_left import ChatMemberLeft

from filters.filters import IsChatMember
from config.config import CONFIG
#from lexicon.lexicon_ru import BOT_MESSAGES
from sqlalchemy.ext.asyncio import AsyncSession
# from database.orm_query import (
#     orm_add_to_cart,
#     orm_add_user,
# )

# from filters.chat_types import ChatTypeFilter
from handlers.media_handlings import set_photo_id
from handlers.menu_processing import get_menu_content
from keyboards.inline import MenuCallBack
#get_callback_btns



user_private_router = Router()

@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message, session_pool: AsyncSession):
    media, reply_markup, banner = await get_menu_content(session_pool, level=0, menu_name="menu_0")

    result = await message.answer_photo(media.media, caption=media.caption, reply_markup=reply_markup)

    if not  banner.photo_tg_id:
        await set_photo_id(async_session = session_pool,
                    orm_object = orm_object,
                    file_id = result.photo[0].file_id)

# @user_private_router.message()
# async def start_cmd(message: types.Message, session: AsyncSession):

# async def add_to_cart(callback: types.CallbackQuery, callback_data: MenuCallBack, session: AsyncSession):
#     user = callback.from_user
#     await orm_add_user(
#         session,
#         user_id=user.id,
#         first_name=user.first_name,
#         last_name=user.last_name,
#         phone=None,
#     )
#     await orm_add_to_cart(session, user_id=user.id, product_id=callback_data.product_id)
#     await callback.answer("Товар добавлен в корзину.")


@user_private_router.callback_query(MenuCallBack.filter())
async def user_menu(callback: types.CallbackQuery, callback_data: MenuCallBack, session_pool: AsyncSession):
    print("__________________get_callback_query")
    print(callback_data.level)
    # if callback_data.menu_name == "add_to_cart":
    #     await add_to_cart(callback, callback_data, session)
    #     return

    media, reply_markup, orm_object = await get_menu_content(
        session = session_pool,
        level=callback_data.level,
        menu_name=callback_data.menu_name,
        category=callback_data.category,
        subcategory = callback_data.subcategory,
        page=callback_data.page,
        product_id=callback_data.product_id,
        user_id=callback.from_user.id,
    )

    await callback.message.edit_media(media=media, reply_markup=reply_markup)
    await callback.answer()