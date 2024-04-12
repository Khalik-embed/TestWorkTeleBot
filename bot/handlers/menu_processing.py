from aiogram.types import InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import Bot
from database.orm_query import (
    # orm_add_to_cart,
    # orm_delete_from_cart,
    orm_get_categories,
    orm_get_subcategories,
    orm_get_banner,
    orm_get_item,
    # orm_get_catalog,
    # orm_get_products,
    # orm_get_user_carts,
    # orm_reduce_product_in_cart,
)

from services.paginator import Paginator

from config.config import CONFIG
from database.orm_query import orm_get_banner

from keyboards.inline import (
    get_products_btns,
    get_user_cart,
    get_user_category_btns,
    get_user_subcategory_btns,
    get_user_main_btns,
    get_url_btns,
)
from handlers.media_handlings import get_photo_id
from lexicon.lexicon_ru import NAVIGATION

async def main_menu(session_pool, level, menu_name):
    banner = await orm_get_banner(async_session = session_pool, slug = menu_name)
    photo_id = get_photo_id(banner)
    image = InputMediaPhoto(media=photo_id, caption=banner.text)

    kbds = get_user_main_btns(level=level)

    return image, kbds, banner


async def categories(session, level, menu_name):
    banner = await orm_get_banner(async_session = session, slug = "categories")
    photo_id = get_photo_id(banner)
    image = InputMediaPhoto(media=photo_id, caption=banner.text)

    categories = await orm_get_categories(session)

    kbds = get_user_category_btns(level=level, categories=categories)

    return image, kbds, banner

async def subcategories(session, level, category_id : int):
    banner = await orm_get_banner(async_session = session, slug = "subcategories")
    photo_id = get_photo_id(banner)
    image = InputMediaPhoto(media=photo_id, caption=banner.text)

    print("_________________subcategories_____________")
    print(category_id)
    subcategories = await orm_get_subcategories(session, category_id)

    for subcategory in subcategories:
        print(subcategory.name)
    kbds = get_user_subcategory_btns(level=level, subcategories=subcategories)

    return image, kbds, banner

def pages(paginator: Paginator):
    btns = dict()
    if paginator.has_previous():
        btns["prev"] = NAVIGATION["prev"]

    if paginator.has_next():
        btns["next"] = NAVIGATION["next"]

    return btns


async def items(session, level, subcategory, page):
    print("__________________subcategory={subcategory}".format(subcategory = subcategory))
    item = await orm_get_item(session, subcategory_id=subcategory)

    paginator = Paginator(item, page=page)
    product = paginator.get_page()[0]

    photo_id = get_photo_id(product)
    print(photo_id)
    image = InputMediaPhoto(
        media=photo_id,
        caption=f"{product.item_name}\
                \n{product.item_description}\nСтоимость: {round(product.cost, 2)}\n\
                Товар {paginator.page} из {paginator.pages}",
    )

    pagination_btns = pages(paginator)

    kbds = get_products_btns(
        level=level,
        subcategory=subcategory,
        page=page,
        pagination_btns=pagination_btns,
        product_id=product.id,
    )

    return image, kbds, item


# async def carts(session, level, menu_name, page, user_id, product_id):
#     if menu_name == "delete":
#         await orm_delete_from_cart(session, user_id, product_id)
#         if page > 1:
#             page -= 1
#     elif menu_name == "decrement":
#         is_cart = await orm_reduce_product_in_cart(session, user_id, product_id)
#         if page > 1 and not is_cart:
#             page -= 1
#     elif menu_name == "increment":
#         await orm_add_to_cart(session, user_id, product_id)

#     carts = await orm_get_user_carts(session, user_id)

#     if not carts:
#         banner = await orm_get_banner(session, "cart")
#         image = InputMediaPhoto(
#             media=banner.image, caption=f"<strong>{banner.description}</strong>"
#         )

#         kbds = get_user_cart(
#             level=level,
#             page=None,
#             pagination_btns=None,
#             product_id=None,
#         )

#     else:
#         paginator = Paginator(carts, page=page)

#         cart = paginator.get_page()[0]

#         cart_price = round(cart.quantity * cart.product.price, 2)
#         total_price = round(
#             sum(cart.quantity * cart.product.price for cart in carts), 2
#         )
#         image = InputMediaPhoto(
#             media=cart.product.image,
#             caption=f"<strong>{cart.product.name}</strong>\n{cart.product.price}$ x {cart.quantity} = {cart_price}$\
#                     \nТовар {paginator.page} из {paginator.pages} в корзине.\nОбщая стоимость товаров в корзине {total_price}",
#         )

#         pagination_btns = pages(paginator)

#         kbds = get_user_cart(
#             level=level,
#             page=page,
#             pagination_btns=pagination_btns,
#             product_id=cart.product.id,
#         )

#     return image, kbds


async def get_menu_content(
    session: AsyncSession,
    level: int,
    menu_name: str,
    category: int | None = None,
    subcategory: str | None = None,
    page: int | None = None,
    product_id: int | None = None,
    user_id: int | None = None,
):
    print("get_menu_content")
    if level == 0:
        print("__________________get_main_menu")
        return await main_menu(session, level, menu_name)
    elif level == 1:
        print("__________________get_categories")
        return await categories(session, level, menu_name)
    elif level == 2:
        return await subcategories(session, level, category)
    elif level == 3:
        return await items(session, level, subcategory, page)
    # elif level == 3:
    #     return await carts(session, level, menu_name, page, user_id, product_id)

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

# async def get_media(orm_object : Banners, keyboard_in : InlineKeyboardBuilder):
#     text = ''
#     keyboard = None
#     photo_id = None
#     if orm_object.text:
#         text = orm_object.text
#     if keyboard_in:
#         keyboard = keyboard_in

#     if orm_object.photo:
#         photo_id = get_photo_id(banner)

#         result = await bot.send_photo(chat_id = chat_id, photo=photo_id, parse_mode = 'HTML',
#             caption = text, reply_markup=keyboard)

#         if not  banner.photo_tg_id:
#             await set_photo_id(async_session = async_session,
#                            banner = banner,
#                            file_id = result.photo[0].file_id)
#     elif keyboard:
#         result = await bot.send_message(chat_id = chat_id, photo=photo_id, parse_mode = 'HTML',
#             caption = text, reply_markup=keyboard)
