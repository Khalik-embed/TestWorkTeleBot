#from aiogram import bot
from aiogram import F, types, Router, Bot
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, ShippingOption, ShippingQuery
from aiogram.methods import SendInvoice
from lexicon.lexicon_ru import PAYMENT_INVOICE
from config.config import CONFIG
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from database.orm_query import orm_get_last_unpayed_user_basket
from database.models import Basket


SELF_SHIPPING = ShippingOption(
    id = "self_shiping",
    title ="Самовывоз",
    prices = [
        LabeledPrice(
            label = 'self_shiping',
            amount = 0
        )
    ])

DELIVERY_SHIPPING = ShippingOption(
    id = "delivery_shiping",
    title ="Доставка курьером",
    prices = [
        LabeledPrice(
            label = 'delivery_shiping',
            amount = 100
        )
    ])


async def shipping_check(shipping_query: ShippingQuery, bot : Bot):
    shipping_options = []
    countries = ['AR']
    if shipping_query.shipping_address.country_code not in countries:
        return await bot.answer_shipping_query(shipping_query.id, ok=False, error_message="not for you")
    else:
        shipping_options.append(SELF_SHIPPING)
        shipping_options.append(DELIVERY_SHIPPING)
        return await bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=shipping_options)

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
        need_name = True,
        need_phone_number = True,
        need_shipping_address = True,
        is_flexible = True,
        request_timeout = 15
    )
    await callback.answer()



async def succesful_payment(message : Message):
    await message.answer(ANSWERS['greeting_for_payment'])