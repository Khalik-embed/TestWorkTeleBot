from aiogram import F, types, Router, Bot
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types.chat_member_left import ChatMemberLeft
from aiogram.types import CallbackQuery, PreCheckoutQuery, Message, ContentType
from filters.filters import IsChatMember
from config.config import CONFIG
#from lexicon.lexicon_ru import BOT_MESSAGES
from sqlalchemy.ext.asyncio import AsyncSession
from database.orm_query import orm_add_to_basket
# from filters.chat_types import ChatTypeFilter
from handlers.media_handlings import set_photo_id
from handlers.menu_processing import get_menu_content, delivery
from handlers.payment import payment
from keyboards.inline import MenuCallBack
from lexicon.lexicon_ru import ANSWERS
#get_callback_btns

storage = MemoryStorage()

class FSMUser(StatesGroup):
    add_delivery  = State()

user_private_router = Router()

@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message, session_pool: AsyncSession):
    media, reply_markup, banner = await get_menu_content(session_pool, level=0, menu_name="menu_0")

    result = await message.answer_photo(media.media, caption=media.caption, reply_markup=reply_markup)

    if not  banner.photo_tg_id:
        await set_photo_id(async_session = session_pool,
                    orm_object = orm_object,
                    file_id = result.photo[0].file_id)

@user_private_router.message(StateFilter(FSMUser.add_delivery))
async def read_delivery_adress(message: types.Message,
                               bot : Bot,
                               session_pool: AsyncSession,
                               state: FSMContext):
    fms_data =  await state.get_data()
    await message.delete()
    media, reply_markup, orm_object = await delivery(session_pool)
    delivery_place = ANSWERS['delivery_place']
    media.caption = media.caption + delivery_place.format(delivery_place = message.text)
    await bot.edit_message_media( chat_id=message.chat.id,
                                        message_id=fms_data['message_id'],
                                        media=media,
                                        reply_markup=reply_markup)
    await callback.answer()


async def add_to_basket(callback: CallbackQuery,
                        callback_data: MenuCallBack,
                        session: AsyncSession):
    await orm_add_to_basket(session,
                            user_id=callback.from_user.id,
                            product_id=callback_data.product_id)
    await callback.answer(ANSWERS['item_in_basket'])


@user_private_router.callback_query(MenuCallBack.filter())
async def user_menu(callback: CallbackQuery,
                    callback_data: MenuCallBack,
                    session_pool: AsyncSession,
                    state: FSMContext,
                    bot : Bot):
    print("__________________get_callback_query")
    print(callback_data)
    if callback_data.menu_name == "add_to_basket":
        print("__________________add_to_basket")

        await add_to_basket(callback, callback_data, session_pool)
        return

    # if callback_data.menu_name == "delivery":
    #     await state.set_state(FSMUser.add_delivery)
    #     await state.update_data(message_id = callback.message.message_id)
    # else:
    #     await state.set_state(default_state)

    if callback_data.menu_name == "payment":
        await payment(session_pool, callback, bot)
        return
        # await state.set_state(FSMUser.add_delivery)
        #await state.update_data(message_id = callback.message.message_id)


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


@user_private_router.pre_checkout_query()
async def pre_checkout_query(pre_checkout_query : PreCheckoutQuery,bot : Bot):
    print(pre_checkout_query)
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok = True)

# @user_private_router.message()
# async def succesful_payment(message : Message):
#     print(message)
#     await message.answer("лошара!!!")
