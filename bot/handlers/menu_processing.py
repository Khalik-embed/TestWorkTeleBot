from aiogram.types import InputMediaPhoto
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
    get_callback_btns,
    get_delivery_btns,
)
from handlers.media_handlings import get_photo_id
from lexicon.lexicon_ru import NAVIGATION, ITEM_PAGE, ANSWERS

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
                \n{product.item_description}\n{ITEM_PAGE['cost']}: {round(product.cost, 2)}\n\
                {ITEM_PAGE['item']} {paginator.page} {ITEM_PAGE['from']} {paginator.pages}",
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


async def basket(session, level, menu_name, page, user_id, product_id):
    if menu_name == "delete":
        await orm_delete_from_basket(session, user_id, product_id)
        if page > 1:
            page -= 1
    elif menu_name == "decrement":
        is_basket = await orm_reduce_product_in_basket(session, user_id, product_id)
        if page > 1 and not is_basket:
            page -= 1
    elif menu_name == "increment":
        await orm_add_to_basket(session, user_id, product_id)

    baskets = await orm_get_last_unpayed_user_basket(session, user_id)
    orm_photo_object : Items | Banners = None
    if not baskets:
        banner = await orm_get_banner(session, "basket_page")
        photo_id = get_photo_id(banner)
        orm_photo_object = banner
        image = InputMediaPhoto(
            media=photo_id, caption=f"{banner.text}"
        )

        kbds = get_user_basket(
            level=level,
            page=None,
            pagination_btns=None,
            product_id=None,
        )

    else:
        paginator = Paginator(baskets, page=page)

        basket = paginator.get_page()[0]
        orm_photo_object = basket.item
        photo_id = get_photo_id(basket.item)

        basket_price = round(basket.count * basket.item.cost, 2)
        total_price = round(
            sum(basket.count * basket.item.cost for basket in baskets), 2
        )
        image = InputMediaPhoto(
            media=photo_id,
            caption=f"{basket.item.item_name}\n{basket.item.cost} x {basket.count} = {basket_price} \
                    \n{ITEM_PAGE['item']} {paginator.page} {ITEM_PAGE['item']} {paginator.pages} {ITEM_PAGE['in_backet']} .\
                    \n{ITEM_PAGE['total_price_in_backet']} {total_price}",
        )

        pagination_btns = pages(paginator)

        kbds = get_user_basket(
            level=level,
            page=page,
            pagination_btns=pagination_btns,
            product_id=basket.item.id,
        )

    return image, kbds, orm_photo_object


async def delivery(session):
    banner = await orm_get_banner(async_session = session, slug = "delivery_page")
    photo_id = get_photo_id(banner)
    image = InputMediaPhoto(
        media=photo_id,
        caption=banner.text,
        )

    kbds = get_delivery_btns()

    return image, kbds, banner


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
    elif level == 4:
        return await basket(session, level, menu_name, page, user_id, product_id)
    elif level == 5:
        return await delivery(session)


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
