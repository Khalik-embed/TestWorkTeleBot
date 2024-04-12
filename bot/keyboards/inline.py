from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon_ru import MENU_LEVEL0_BUTTONS, NAVIGATION
from database.models import  Category, SubCategory

class MenuCallBack(CallbackData, prefix="menu"):
    level: int
    menu_name: str
    category: int | None = None
    subcategory: int | None = None
    page: int = 1
    product_id: int | None = None


def get_user_main_btns(*, level: int, sizes: tuple[int] = (1,)):
    keyboard = InlineKeyboardBuilder()
    for menu_name, text  in MENU_LEVEL0_BUTTONS.items():
        if menu_name == 'catalog':
            keyboard.add(InlineKeyboardButton(text=text,
                    callback_data=MenuCallBack(level=level+1, menu_name=menu_name).pack()))
        elif menu_name == 'backet':
            keyboard.add(InlineKeyboardButton(text=text,
                    callback_data=MenuCallBack(level=4, menu_name=menu_name).pack()))
        else:
            keyboard.add(InlineKeyboardButton(text=text,
                    callback_data=MenuCallBack(level=level, menu_name=menu_name).pack()))

    return keyboard.adjust(*sizes).as_markup()


def get_user_category_btns(*, level: int, categories: Category, sizes: tuple[int] = (1,)):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text=MENU_LEVEL0_BUTTONS['backet'],
                callback_data=MenuCallBack(level=4, menu_name='cart').pack()))

    for category in categories:
        keyboard.add(InlineKeyboardButton(text=category.name,
                callback_data=MenuCallBack(level=level+1, menu_name=category.slug, category=category.id).pack()))

    keyboard.add(InlineKeyboardButton(text=NAVIGATION['back'],
                callback_data=MenuCallBack(level=level-1, menu_name='menu_0').pack()))

    return keyboard.adjust(*sizes).as_markup()

def get_user_subcategory_btns(*, level: int, subcategories: SubCategory, sizes: tuple[int] = (1,)):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text=MENU_LEVEL0_BUTTONS['backet'],
                callback_data=MenuCallBack(level=4, menu_name='cart').pack()))
    for subcategory in subcategories:
        keyboard.add(InlineKeyboardButton(text=subcategory.name,
                callback_data=MenuCallBack(level=level+1, menu_name=subcategory.slug, subcategory=subcategory.id).pack()))

    keyboard.adjust(*sizes)
    row = []
    row.append(InlineKeyboardButton(text=NAVIGATION['back'],
                callback_data=MenuCallBack(level=level-1, menu_name='catalog').pack()))
    row.append(InlineKeyboardButton(text=NAVIGATION['menu_0'],
                callback_data=MenuCallBack(level=0, menu_name='menu_0').pack()))

    return keyboard.row(*row).as_markup()


def get_products_btns(
    *,
    level: int,
    subcategory: int,
    page: int,
    pagination_btns: dict,
    product_id: int
):
    keyboard = InlineKeyboardBuilder()


    keyboard.add(InlineKeyboardButton(text=MENU_LEVEL0_BUTTONS['backet'],
                callback_data=MenuCallBack(level=4, menu_name='cart').pack()))
    keyboard.add(InlineKeyboardButton(text=NAVIGATION['buy'],
                callback_data=MenuCallBack(level=level, menu_name='add_to_cart', product_id=product_id).pack()))

    button_next, button_prev = False, False
    for menu_name, text in pagination_btns.items():
        if menu_name == "next":
            button_next = True
            keyboard.add(InlineKeyboardButton(text=text,
                    callback_data=MenuCallBack(
                        level=level,
                        menu_name=menu_name,
                        subcategory=subcategory,
                        page=page + 1).pack()))


        elif menu_name == "prev":
            button_prev = True
            keyboard.add(InlineKeyboardButton(text=text,
                    callback_data=MenuCallBack(
                        level=level,
                        menu_name=menu_name,
                        subcategory=subcategory,
                        page=page - 1).pack()))

    if button_next and button_prev:
        sizes: tuple[int] = (1, 1, 2, 2,)
    elif button_next or button_prev:
        sizes: tuple[int] = (1, 1, 1, 2,)
    else:
        sizes: tuple[int] = (1, 1, 2,)

    keyboard.add(InlineKeyboardButton(text=NAVIGATION['back'],
                callback_data=MenuCallBack(level=1, menu_name='catalog').pack()))
    keyboard.add(InlineKeyboardButton(text=NAVIGATION['menu_0'],
                callback_data=MenuCallBack(level=0, menu_name='menu_0').pack()))

    keyboard.adjust(*sizes)
    return keyboard.as_markup()


def get_user_cart(
    *,
    level: int,
    page: int | None,
    pagination_btns: dict | None,
    product_id: int | None,
    sizes: tuple[int] = (3,)
):
    keyboard = InlineKeyboardBuilder()
    if page:
        keyboard.add(InlineKeyboardButton(text='Удалить',
                    callback_data=MenuCallBack(level=level, menu_name='delete', product_id=product_id, page=page).pack()))
        keyboard.add(InlineKeyboardButton(text='-1',
                    callback_data=MenuCallBack(level=level, menu_name='decrement', product_id=product_id, page=page).pack()))
        keyboard.add(InlineKeyboardButton(text='+1',
                    callback_data=MenuCallBack(level=level, menu_name='increment', product_id=product_id, page=page).pack()))

        keyboard.adjust(*sizes)

        row = []
        for text, menu_name in pagination_btns.items():
            if menu_name == "next":
                row.append(InlineKeyboardButton(text=text,
                        callback_data=MenuCallBack(level=level, menu_name=menu_name, page=page + 1).pack()))
            elif menu_name == "previous":
                row.append(InlineKeyboardButton(text=text,
                        callback_data=MenuCallBack(level=level, menu_name=menu_name, page=page - 1).pack()))

        keyboard.row(*row)

        row2 = [
        InlineKeyboardButton(text='На главную 🏠',
                    callback_data=MenuCallBack(level=0, menu_name='main').pack()),
        InlineKeyboardButton(text='Заказать',
                    callback_data=MenuCallBack(level=0, menu_name='order').pack()),
        ]
        return keyboard.row(*row2).as_markup()
    else:
        keyboard.add(
            InlineKeyboardButton(text='На главную 🏠',
                    callback_data=MenuCallBack(level=0, menu_name='main').pack()))

        return keyboard.adjust(*sizes).as_markup()


def get_callback_btns(*, btns: dict[str, str], sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()

    for text, data in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()

def get_url_btns( btns: dict[str, str], sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()

    for text, url in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, url=url))

    return keyboard.adjust(*sizes).as_markup()
