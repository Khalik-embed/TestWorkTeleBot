#from aiogram import bot
from aiogram import F, types, Router, Bot
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery
from aiogram.methods import SendInvoice
from lexicon.lexicon_ru import PAYMENT_INVOICE
from config.config import CONFIG
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from database.orm_query import orm_get_last_unpayed_user_basket
from database.models import Basket

def get_items_and_prices_from_baskets(baskets : Basket) -> [LabeledPrice]:
    prices : [LabeledPrice] = []

    for basket in baskets:
        prices.append(LabeledPrice(label = f"{basket.item.item_name} : {basket.item.cost} x {basket.count}",
            amount = int(basket.item.cost * basket.count  * 100)))
    return prices


async def payment(session : AsyncSession, callback : CallbackQuery, bot : Bot):
    ### some func for getting prices

    print(callback)
    baskets : Basket = await orm_get_last_unpayed_user_basket(session, callback.from_user.id)

    if not baskets:
        await callback.answer() ################
    else :
        prices : LabeledPrice = get_items_and_prices_from_baskets(baskets)

    await bot.send_invoice (
        chat_id = callback.message.chat.id,
        title = PAYMENT_INVOICE['title'],
        description = PAYMENT_INVOICE['description'],
        provider_token = CONFIG.payment.provider_token,
        currency = 'rub',
        prices = prices,
        payload = "Payment for items",
        request_timeout = 15
    )
    await callback.answer()

# async def pre_checkout(pre_checkout_query : PreCheckoutQuery):
#     await bot.answer_pre_checkout_query(pre_checkout_query.id, ok = True)

async def succesful_payment(message : Message):
    await message.answer("лошара!!!")