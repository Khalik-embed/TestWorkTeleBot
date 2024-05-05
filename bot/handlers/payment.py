from aiogram import F, Router, Bot
from aiogram.types import (
    Message,            LabeledPrice,       PreCheckoutQuery,
    ShippingOption,     ShippingQuery,      ContentType,
    SuccessfulPayment)
from aiogram.methods import SendInvoice
from aiogram.types import CallbackQuery

from lexicon import PAYMENT_INVOICE, ANSWERS
from config.config import CONFIG
from config.commands import COMMANDS, MenuLevel
from database.orm_query import (
    orm_get_last_unpayed_user_basket,
    orm_add_payment_packet,
    orm_create_invoice_order,
    orm_add_succesful_payment,
    orm_set_paed_packet)
from database.models import Basket
from keyboards.inline import MenuCallBack
from handlers.menu_processing import get_menu_content

payment_router = Router()

@payment_router.pre_checkout_query()
async def pre_checkout_query(pre_checkout_query : PreCheckoutQuery,bot : Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok = True)

@payment_router.shipping_query()
async def shipping_query(shipping_query: ShippingQuery, bot : Bot):
    await shipping_check(shipping_query, bot)

@payment_router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def succesful_payment(message : Message):
    print(message)
    await orm_add_succesful_payment(payment = message.successful_payment)
    await orm_set_paed_packet(payment = message.successful_payment)

    await message.answer(ANSWERS['greeting_for_payment'])

    menu : MenuCallBack = MenuCallBack(level = MenuLevel.start_menu.value, menu_name = MenuLevel.start_menu.name)
    await get_menu_content(message = message, callback_data = menu)

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
        return await bot.answer_shipping_query(shipping_query.id, ok = False, error_message = ANSWERS['no_shipping_to_country'])
    else:
        shipping_options.append(SELF_SHIPPING)
        shipping_options.append(DELIVERY_SHIPPING)
        return await bot.answer_shipping_query(shipping_query.id, ok = True, shipping_options = shipping_options)

def get_items_and_prices_from_baskets(baskets : Basket) -> [LabeledPrice]:
    prices : [LabeledPrice] = []

    for basket in baskets:
        prices.append(LabeledPrice(label = f"{basket.item.item_name} : {basket.item.cost} x {basket.count}",
            amount = int(basket.item.cost * basket.count  * 100)))
    return prices


@payment_router.callback_query(F.data == COMMANDS.payment.name)
async def make_invoice(callback : CallbackQuery, bot : Bot):

    baskets : Basket = await orm_get_last_unpayed_user_basket(callback.from_user.id)
    create_new_order = False
    for basket in baskets:
        if not basket.paid_order_id:
            create_new_order = True
    if create_new_order:
        await orm_add_payment_packet(baskets)
        baskets = await orm_get_last_unpayed_user_basket(callback.from_user.id)

    if not baskets:
        await callback.answer()
        return
    else :
        prices : LabeledPrice = get_items_and_prices_from_baskets(baskets)

    result = await orm_create_invoice_order(baskets)
    payload : str = str(baskets[0].paid_order_id)

    await bot.send_invoice (
        chat_id = callback.message.chat.id,
        title = PAYMENT_INVOICE['title'],
        description = PAYMENT_INVOICE['description'],
        provider_token = CONFIG.payment.provider_token,
        currency = 'rub',
        prices = prices,
        payload = payload,
        need_name = True,
        need_phone_number = True,
        need_shipping_address = True,
        is_flexible = True,
        request_timeout = 15
    )
    await callback.answer()