from aiogram.methods.get_me import GetMe
from aiogram.types import (
    InputMediaPhoto,
    Message,
    CallbackQuery,
    User
    )
from keyboards.inline import MenuCallBack
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import Bot
from database.orm_query import (
    orm_get_categories,
    orm_get_subcategories,
    orm_get_banner,
    orm_get_item,
    orm_get_last_unpayed_user_basket,
    orm_add_to_basket,
    orm_reduce_product_in_basket,
    orm_delete_from_basket,
    )

from services.paginator import Paginator

from config.config import CONFIG
from database.orm_query import orm_get_banner

from keyboards.inline import (
    get_products_btns,
    get_user_basket,
    get_user_category_btns,
    get_user_subcategory_btns,
    get_user_main_btns,
    get_url_btns,
    get_callback_btns)
from handlers.media_handlings import get_photo_id, set_photo_id
from lexicon.lexicon_ru import NAVIGATION, ITEM_PAGE, ANSWERS
from config.commands import MenuLevel, BANNERS, COMMANDS

async def main_menu(message : Message = None, callback : CallbackQuery = None):
    banner : Banners  = await orm_get_banner(slug = BANNERS.start_menu.name)
    if not banner:
        logging.CRITICAL('Banner does not exist')
    photo_id : str = get_photo_id(orm_object = banner)
    image = InputMediaPhoto(media=photo_id, caption=banner.text)
    reply_markup : InlineKeyboardMarkup = get_user_main_btns()
    if message:
        result : Message  = await message.answer_photo(
            photo = image.media,
            caption = image.caption,
            reply_markup = reply_markup)
    else:
        result : message  = await callback.message.edit_media(media = image, reply_markup = reply_markup)
    await set_photo_id(orm_object = banner, file_id = result.photo[0].file_id)


async def categories(
    callback_data : MenuCallBack | None = None,
    callback: CallbackQuery | None = None ):

    banner : Banners = await orm_get_banner(slug = BANNERS.categories.name)
    photo_id : str = get_photo_id(orm_object = banner)
    image : InputMediaPhoto = InputMediaPhoto(media = photo_id, caption = banner.text)
    categories : [Category] = await orm_get_categories()
    kbds : InlineKeyboardMarkup = get_user_category_btns(categories = categories)
    result : Message = await callback.message.edit_media(media = image, reply_markup = kbds)
    await set_photo_id(orm_object = banner, file_id = result.photo[0].file_id)


async def subcategories(
    callback_data : MenuCallBack | None = None,
    callback: CallbackQuery | None = None ):
    banner : Banners = await orm_get_banner(slug = BANNERS.subcategories.name)
    photo_id : str = get_photo_id(orm_object = banner)
    image : InputMediaPhoto = InputMediaPhoto(media = photo_id, caption=banner.text)
    subcategories : [SubCategory] = await orm_get_subcategories(callback_data.category)
    kbds : InlineKeyboardMarkup = get_user_subcategory_btns(subcategories = subcategories)
    result : Message = await callback.message.edit_media(media = image, reply_markup = kbds)
    await set_photo_id(orm_object = banner, file_id = result.photo[0].file_id)

def pages(paginator: Paginator) -> dict:
    btns = dict()
    if paginator.has_previous():
        btns["prev"] = NAVIGATION["prev"]

    if paginator.has_next():
        btns["next"] = NAVIGATION["next"]

    return btns

async def items(
    callback_data : MenuCallBack | None = None,
    callback: CallbackQuery | None = None ):
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(callback_data)
    print(COMMANDS.add_to_basket.name)
    if callback_data.menu_name == COMMANDS.add_to_basket.name:
        await add_to_basket(callback = callback, callback_data = callback_data)
        return

    item : [Items] = await orm_get_item(subcategory_id = callback_data.subcategory)

    paginator :  Paginator = Paginator(array = item, page=callback_data.page)
    product : Items = paginator.get_page()[0]

    photo_id : str = get_photo_id(orm_object = product)
    image = InputMediaPhoto(
        media = photo_id,
        caption = f"{product.item_name}\
                \n{product.item_description}\n{ITEM_PAGE['cost']}: {round(product.cost, 2)}\n\
                {ITEM_PAGE['item']} {paginator.page} {ITEM_PAGE['from']} {paginator.pages}",)

    pagination_btns = pages(paginator = paginator)

    kbds : InlineKeyboardMarkup = get_products_btns(
        subcategory = callback_data.subcategory,
        page = callback_data.page,
        pagination_btns = pagination_btns,
        product_id = product.id,
    )
    result : Message = await callback.message.edit_media(media = image, reply_markup = kbds)
    await set_photo_id(orm_object = product, file_id = result.photo[0].file_id)


async def basket( callback_data : MenuCallBack | None = None,
    callback: CallbackQuery | None = None ):
    if callback_data.menu_name == COMMANDS.delete.name:
        await orm_delete_from_basket(user_id = callback.from_user.id, item_id = callback_data.product_id)
        if callback_data.page > 1:
            callback_data.page -= 1
    elif callback_data.menu_name == COMMANDS.decrement.name:
        is_basket = await orm_reduce_product_in_basket(user_id = callback.from_user.id, item_id = callback_data.product_id)
        if callback_data.page > 1 and not is_basket:
            callback_data.page -= 1
    elif callback_data.menu_name == COMMANDS.increment.name:
        await orm_add_to_basket(user_id = callback.from_user.id, item_id = callback_data.product_id)
    # elif callback_data.menu_name == COMMANDS.payment:  ############
    #     await payment(callback, bot)
    #     return

    baskets : [baskets] = await orm_get_last_unpayed_user_basket(user_id = callback.from_user.id)
    print(baskets)
    orm_photo_object : Items | Banners = None
    if not baskets:
        banner : Banners = await orm_get_banner(MenuLevel.basket.name)
        photo_id : str = get_photo_id(banner)
        orm_photo_object = banner
        image = InputMediaPhoto(
            media=photo_id, caption=f"{banner.text}")

        kbds = get_user_basket(
            page=None,
            pagination_btns=None,
            product_id=None,)

    else:
        paginator : Paginator = Paginator(baskets, page = callback_data.page)

        basket : Basket = paginator.get_page()[0]
        orm_photo_object : Item = basket.item
        photo_id : str = get_photo_id(orm_object = orm_photo_object)

        basket_price : float = round(basket.count * basket.item.cost, 2)
        total_price : float = round(
            sum(basket.count * basket.item.cost for basket in baskets), 2)
        image : InputMediaPhoto = InputMediaPhoto(
            media = photo_id,
            caption = f"{basket.item.item_name}\n{basket.item.cost} x {basket.count} = {basket_price} \
                    \n{ITEM_PAGE['item']} {paginator.page} {ITEM_PAGE['item']} {paginator.pages} {ITEM_PAGE['in_backet']} .\
                    \n{ITEM_PAGE['total_price_in_backet']} {total_price}")

        pagination_btns : [] = pages(paginator)#######3

        kbds : InlineKeyboardMarkup = get_user_basket(
            page = callback_data.page,
            pagination_btns = pagination_btns,
            product_id = basket.item.id)

    result : as_response = await callback.message.edit_media(media = image, reply_markup = kbds)
    await set_photo_id(orm_object = orm_photo_object, file_id = result.photo[0].file_id)

async def add_to_basket(callback : CallbackQuery,
                        callback_data : MenuCallBack):
    await orm_add_to_basket(user_id = callback.from_user.id,
                            item_id = callback_data.product_id)
    await callback.answer(text = ANSWERS['item_in_basket'])

async def faq(callback : CallbackQuery,
                bot : Bot):
    print("__________________________________________________________________")
    me : User = await bot.get_me()
    print(me)
    await callback.answer(ANSWERS['faq_answer'].format(bot_name = me.username),
                          show_alert = True)

async def get_menu_content(callback_data : MenuCallBack | None = None,
        message : Message | None = None,
        callback: CallbackQuery | None = None,
        bot : Bot | None = None):

    if callback_data.level == MenuLevel.start_menu.value:
        await main_menu(message = message,  callback = callback)

    elif callback_data.level == MenuLevel.categories.value:
        await categories(callback = callback, callback_data = callback_data)

    elif callback_data.level == MenuLevel.subcategories.value:
        await subcategories(callback = callback, callback_data = callback_data)

    elif callback_data.level == MenuLevel.items.value:
        await items(callback = callback, callback_data = callback_data)

    elif callback_data.level == MenuLevel.basket.value:
        await basket(callback = callback, callback_data = callback_data)

    elif callback_data.level == MenuLevel.faq.value:
        await faq(callback = callback,
                  bot = bot)
