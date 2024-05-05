from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message, InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from config.config import CONFIG
from config.commands import MenuLevel, BANNERS
from handlers.menu_processing import get_menu_content
from keyboards.inline import MenuCallBack

users_router = Router()

@users_router.message(CommandStart())
async def start_cmd(message: Message):
    menu : MenuCallBack = MenuCallBack(level = MenuLevel.start_menu.value, menu_name = MenuLevel.start_menu.name)
    await get_menu_content(message = message, callback_data = menu)

@users_router.callback_query(MenuCallBack.filter())
async def user_menu(callback: CallbackQuery,
                    callback_data: MenuCallBack,
                    bot : Bot):
    print("____________________________________________________callback_data")
    print(callback_data)
    print(callback)
    await get_menu_content(callback_data = callback_data,
                           callback = callback,
                           bot = bot)
