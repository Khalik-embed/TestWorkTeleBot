from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon_ru import NAVIGATION
from database.models import  Category, SubCategory
from config.commands import MenuLevel, BANNERS, COMMANDS

class MenuCallBack(CallbackData, prefix="m"):
    level: int
    menu_name: str
    category: int | None = None
    subcategory: int | None = None
    page: int = 1
    product_id: int | None = None


def get_user_main_btns(*, sizes: tuple[int] = (1,)):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(
        text = NAVIGATION[MenuLevel.categories.name],
        callback_data = MenuCallBack(
            level = MenuLevel.categories.value,
            menu_name = MenuLevel.categories.name).pack()))

    keyboard.add(InlineKeyboardButton(
        text = NAVIGATION[MenuLevel.basket.name],
        callback_data = MenuCallBack(
            level = MenuLevel.basket.value,
            menu_name = MenuLevel.basket.name).pack()))

    keyboard.add(InlineKeyboardButton(
        text = NAVIGATION[MenuLevel.faq.name],
        callback_data = MenuCallBack(
            level = MenuLevel.faq.value,
            menu_name = MenuLevel.faq.name).pack()))

    return keyboard.adjust(*sizes).as_markup()


def get_user_category_btns(*, categories: Category, sizes: tuple[int] = (1,)):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text = NAVIGATION[MenuLevel.basket.name],
                callback_data = MenuCallBack(level = MenuLevel.basket.value, menu_name = MenuLevel.basket.name).pack()))

    for category in categories:
        keyboard.add(InlineKeyboardButton(text = category.name,
                callback_data = MenuCallBack(level = MenuLevel.subcategories.value, menu_name = category.slug, category = category.id).pack()))

    keyboard.add(InlineKeyboardButton(text = NAVIGATION[COMMANDS.back.name],
                callback_data = MenuCallBack(level = MenuLevel.start_menu.value, menu_name =  MenuLevel.start_menu.name).pack()))

    return keyboard.adjust(*sizes).as_markup()

def get_user_subcategory_btns(*, subcategories: SubCategory, sizes: tuple[int] = (1,)):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text = NAVIGATION[MenuLevel.basket.name],
                callback_data = MenuCallBack(level = MenuLevel.basket.value, menu_name = MenuLevel.basket.name).pack()))
    for subcategory in subcategories:
        keyboard.add(InlineKeyboardButton(text = subcategory.name,
                callback_data = MenuCallBack(level = MenuLevel.items.value, menu_name = subcategory.slug, subcategory = subcategory.id).pack()))

    keyboard.adjust(*sizes)
    row = []
    row.append(InlineKeyboardButton(text = NAVIGATION[COMMANDS.back.name],
                callback_data = MenuCallBack(level = MenuLevel.categories.value, menu_name =  MenuLevel.categories.name).pack()))
    row.append(InlineKeyboardButton(text = NAVIGATION[MenuLevel.start_menu.name],
                callback_data = MenuCallBack(level = MenuLevel.start_menu.value, menu_name =  MenuLevel.start_menu.name).pack()))

    return keyboard.row(*row).as_markup()


def get_products_btns(
    *,
    subcategory: int,
    page: int,
    pagination_btns: dict,
    product_id: int
):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text = NAVIGATION[MenuLevel.basket.name],
                callback_data = MenuCallBack(level = MenuLevel.basket.value, menu_name = MenuLevel.basket.name).pack()))
    keyboard.add(InlineKeyboardButton(text = NAVIGATION[COMMANDS.add_to_basket.name],
                callback_data = MenuCallBack(level = MenuLevel.items.value, menu_name = COMMANDS.add_to_basket.name, product_id = product_id).pack()))

    button_next, button_prev = False, False
    for menu_name, text in pagination_btns.items():
        if menu_name == COMMANDS.next.name:
            button_next = True
            keyboard.add(InlineKeyboardButton(text = text,
                    callback_data = MenuCallBack(
                        level = MenuLevel.items.value,
                        menu_name = MenuLevel.items.name,
                        subcategory = subcategory,
                        page = page + 1).pack()))

        elif menu_name ==  COMMANDS.prev.name:
            button_prev = True
            keyboard.add(InlineKeyboardButton(text = text,
                    callback_data = MenuCallBack(
                        level =  MenuLevel.items.value,
                        menu_name = menu_name,
                        subcategory = MenuLevel.items.name,
                        page = page - 1).pack()))

    if button_next and button_prev:
        sizes: tuple[int] = (1, 1, 2, 2,)
    elif button_next or button_prev:
        sizes: tuple[int] = (1, 1, 1, 2,)
    else:
        sizes: tuple[int] = (1, 1, 2,)

    keyboard.add(InlineKeyboardButton(text = NAVIGATION[COMMANDS.back.name],
                callback_data = MenuCallBack(level = MenuLevel.categories.value, menu_name =  MenuLevel.categories.name).pack()))

    keyboard.add(InlineKeyboardButton(text = NAVIGATION[MenuLevel.start_menu.name],
                callback_data = MenuCallBack(level = MenuLevel.start_menu.value, menu_name =  MenuLevel.start_menu.name).pack()))


    keyboard.adjust(*sizes)
    return keyboard.as_markup()


def get_user_basket(
    *,
    page: int | None,
    pagination_btns: dict | None,
    product_id: int | None,
    sizes: tuple[int] = (3,)
):
    keyboard = InlineKeyboardBuilder()
    if page:
        keyboard.add(InlineKeyboardButton(text = NAVIGATION[COMMANDS.delete.name],
                    callback_data = MenuCallBack(level = MenuLevel.basket.value,
                                                 menu_name = COMMANDS.delete.name,
                                                 product_id = product_id,
                                                 page = page).pack()))

        keyboard.add(InlineKeyboardButton(text = NAVIGATION[COMMANDS.decrement.name],
                    callback_data = MenuCallBack(level = MenuLevel.basket.value,
                                                 menu_name = COMMANDS.decrement.name,
                                                 product_id = product_id,
                                                 page = page).pack()))

        keyboard.add(InlineKeyboardButton(text = NAVIGATION[COMMANDS.increment.name],
                    callback_data = MenuCallBack(level = MenuLevel.basket.value,
                                                 menu_name = COMMANDS.increment.name,
                                                 product_id =product_id,
                                                 page = page).pack()))

        keyboard.adjust(*sizes)

        row = []
        for menu_name, text in pagination_btns.items():
            if menu_name ==  COMMANDS.next.name:
                row.append(InlineKeyboardButton(text = text,
                        callback_data=MenuCallBack(level = MenuLevel.basket.value,
                                                   menu_name = menu_name,
                                                   page = page + 1).pack()))
            elif menu_name ==  COMMANDS.prev.name:
                row.append(InlineKeyboardButton(text = text,
                        callback_data = MenuCallBack(level = MenuLevel.basket.value,
                                                     menu_name = menu_name,
                                                     page = page - 1).pack()))

        keyboard.row(*row)

        row2 = []
        row2.append(InlineKeyboardButton(text = NAVIGATION[COMMANDS.payment.name],
                callback_data = COMMANDS.payment.name))
        keyboard.row(*row2)

        row3 = []
        row3.append(InlineKeyboardButton(text = NAVIGATION[MenuLevel.start_menu.name],
                    callback_data = MenuCallBack(level = MenuLevel.start_menu.value,
                                                 menu_name = MenuLevel.start_menu.name).pack()))

        return keyboard.row(*row3).as_markup()
    else:
        keyboard.add(InlineKeyboardButton(text = NAVIGATION[MenuLevel.start_menu.name],
                    callback_data = MenuCallBack(level = MenuLevel.start_menu.value,
                                                 menu_name = MenuLevel.start_menu.name).pack()))

        return keyboard.adjust(*sizes).as_markup()

def get_callback_btns(*, btns: dict[str, str], sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()

    for text, data in btns.items():
        keyboard.add(InlineKeyboardButton(text = text, callback_data = data))

    return keyboard.adjust(*sizes).as_markup()

def get_url_btns( btns: dict[str, str], sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()

    for text, url in btns.items():
        keyboard.add(InlineKeyboardButton(text = text, url = url))

    return keyboard.adjust(*sizes).as_markup()
