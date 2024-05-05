import math
import copy
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from database.models import (
    Users,          Banners,        Category,
    SubCategory,    Items,          Basket,
    FAQ,            Mailings,       PaidOrder)
from aiogram.types import SuccessfulPayment
from database.engine import SESSION_MAKER

######## users ##############
async def orm_check_if_user_exist (user_id : int) -> bool:
    async with SESSION_MAKER() as session:
        query = select(Users).where(Users.user_id == user_id)
        result = await session.execute(query)
    if result.scalar():
        return True
    else:
        return False

async def orm_add_user (user_id: int, user_name:str) -> bool:
    async with SESSION_MAKER() as session:
        user = Users(user_id = user_id,
                     user_name = user_name,
                     time_create = datetime.now(),
                     time_update = datetime.now(), )
        session.add(user)
        result = await session.flush()
        result = await session.commit()

async def orm_update_user (user_id: int, user_name:str) -> bool:
    async with SESSION_MAKER() as session:
        query = update(Users).where(Users.user_id == user_id).values(user_name=user_name,
                                                                    time_update = datetime.now())
        await session.execute(query)
        await session.commit()

async def orm_get_user_ids () -> bool:
    async with SESSION_MAKER() as session:
        query = select(Users.user_id)
        result = await session.execute(query)
    return result.scalars().all()

######## Banners ##############
async def orm_get_banner (slug : str) -> Banners:
    async with SESSION_MAKER() as session:
        query = select(Banners).where(Banners.slug == slug)
        result = await session.execute(query)
    return result.scalar()

######### Images ############################
async def orm_set_photo_tg_id (orm_object : Items | Banners, file_id :str) -> Banners:
    async with SESSION_MAKER() as session:
        if type(orm_object) == Items:
            query = update(Items).where(Items.photo == orm_object.photo).values(photo_tg_id=file_id)
        else:
            query = update(Banners).where(Banners.photo == orm_object.photo).values(photo_tg_id=file_id)
        await session.execute(query)
        result = await session.commit()

######### Catalog  #############
async def orm_get_categories() -> dict [str, str]:
    async with SESSION_MAKER() as session:
        query = select(Category).join(Items, Items.category_id == Category.id).distinct()
        result = await session.execute(query)
    return result.scalars().all()

async def orm_get_subcategories(category_id : int) -> dict [str, str]:
    async with SESSION_MAKER() as session:
        query = select(SubCategory).join(Items, Items.subcategory_id == SubCategory.id).filter(SubCategory.category_id == category_id).distinct()
        result = await session.execute(query)
    return result.scalars().all()

async def orm_get_item(subcategory_id : int) -> dict [str, str]:
    async with SESSION_MAKER() as session:
        query = select(Items).filter(Items.subcategory_id == subcategory_id)
        result = await session.execute(query)
    return result.scalars().all()

################# backet ######################
async def orm_get_last_unpayed_user_basket(user_id: int | str):
    async with SESSION_MAKER() as session:
        query = select(Users).where(Users.user_id == int(user_id))
        user = await session.execute(query)
        user = user.scalar()
        query = select(Basket).filter(Basket.user_id == user.id, Basket.paid == False)
        result = await session.execute(query)
        baskets = result.scalars().all()
    return baskets

async def orm_add_to_basket(user_id : int | str, item_id : int | str):
    user : Users = None
    item : Items = None
    async with SESSION_MAKER() as session:
        query = select(Users).where(Users.user_id == int(user_id))
        user = await session.execute(query)
        user = user.scalar()
        print(user.user_id)

        query = select(Items).where(Items.id == int(item_id))
        item = await session.execute(query)
        item = item.scalar()
        print(item.id)

        query = select(Basket).filter(Basket.user_id == user.id, Basket.item_id == item.id, Basket.paid == False)
        basket = await session.execute(query)
        basket = basket.scalar()
        if basket:
            basket.count += 1
            await session.commit()
            return basket
        else:
            session.add(Basket(user_id = user.id, item_id=item.id, count=1, time_create = datetime.now(), paid = False))
            await session.commit()

async def orm_delete_from_basket(user_id: int | str, item_id: int | str):
    async with SESSION_MAKER() as session:
        query = select(Users).where(Users.user_id == int(user_id))
        user = await session.execute(query)
        user = user.scalar()
        print(user.user_id)

        query = select(Items).where(Items.id == int(item_id))
        item = await session.execute(query)
        item = item.scalar()
        print(item.id)

        query = delete(Basket).filter(Basket.user_id == user.id, Basket.item_id == item.id, Basket.paid == False)
        await session.execute(query)
        await session.commit()

async def orm_reduce_product_in_basket(user_id: int, item_id: int):
    async with SESSION_MAKER() as session:
        query = select(Users).where(Users.user_id == int(user_id))
        user = await session.execute(query)
        user = user.scalar()
        print(user.user_id)

        query = select(Items).where(Items.id == int(item_id))
        item = await session.execute(query)
        item = item.scalar()
        print(item.id)

        query = select(Basket).filter(Basket.user_id == user.id, Basket.item_id == item.id, Basket.paid == False)
        basket = await session.execute(query)
        basket = basket.scalar()

        if not basket:
            return
        if basket.count > 1:
            basket.count -= 1
            await session.commit()
            return True
        else:
            await orm_delete_from_basket(session, user_id, item_id)
            await session.commit()
            return False


# async def orm_paid_update_basket():
#     async with SESSION_MAKER() as session:
#         user = Users(user_id = user_id,
#                      user_name = user_name,
#                      time_create = datetime.now(),
#                      time_update = datetime.now(), )
#         session.add(user)
#         result = await session.flush()
#         result = await session.commit()

async def orm_add_payment_packet(baskets : Basket):
    async with SESSION_MAKER() as session:
        order = PaidOrder(time_create = datetime.now())
        session.add(order)
        await session.flush()

        query = update(Basket).filter(Basket.user_id == baskets[0].user.id, Basket.paid == False).values(paid_order_id = order.id)
        await session.execute(query)
        await session.commit()

            # query = select(Users).where(Users.user_id == int(user_id))
            # user = await session.execute(query)
            # user = user.scalar()
            # query = select(Basket).filter(Basket.user_id == user.id, Basket.paid == False)
            # result = await session.execute(query)
            # baskets = result.scalars().all()

async def orm_set_paed_packet(payment : SuccessfulPayment):
    async with SESSION_MAKER() as session:
        query = update(Basket).where(Basket.paid_order_id == int(payment.invoice_payload)).values(paid = True)
        await session.execute(query)
        await session.commit()



################# PAID ORDERS ######################
async def orm_create_invoice_order(baskets : list[Basket]) -> int:
    result = None
    create_new_order = False
    print("__________________________________________________________")
    async with SESSION_MAKER() as session:
        for basket in baskets:
            print(basket)
            if not basket.paid_order_id:
                create_new_order = True
        print(create_new_order)
        if create_new_order:
            order = PaidOrder(time_create = datetime.now())
            session.add(order)
            await session.flush()
            for basket in baskets:
                basket.paid_order_id = order.id
            await session.flush()
            await session.commit()

async def orm_add_succesful_payment(payment : SuccessfulPayment):
    async with SESSION_MAKER() as session:
        query = update(PaidOrder).where(PaidOrder.id == int(payment.invoice_payload)).values(
            total_amount = payment.total_amount,
            telegram_payment_charge_id = payment.telegram_payment_charge_id,
            provider_payment_charge_id = payment.provider_payment_charge_id,
            shipping_option = payment.shipping_option_id,
            contact_name = payment.order_info.name,
            contact_phone_number = payment.order_info.phone_number,
            shipping_state = payment.order_info.shipping_address.state,
            shipping_city = payment.order_info.shipping_address.city,
            shipping_street_line1 = payment.order_info.shipping_address.street_line1,
            shipping_street_line2 = payment.order_info.shipping_address.street_line2,
            shipping_post_code = payment.order_info.shipping_address.post_code,
        )
        await session.execute(query)
        await session.commit()


####################### FAQ #######################################
async def orm_get_question_from_faq():
    async with SESSION_MAKER() as session:
        query = select(FAQ.question)
        result = await session.execute(query)
    return result.scalars().all()

async def orm_get_answer_from_faq(question : str):
    async with SESSION_MAKER() as session:
        query = select(FAQ.answer).where(FAQ.question == question)
        result = await session.execute(query)
    return result.scalars().all()

async def orm_add_question_to_faq(question : str):
    async with SESSION_MAKER() as session:
        query = select(FAQ.answer).where(FAQ.question == question)
        result = await session.execute(query)
    return result.scalars().all()

######################### MAILINGS ####################################
async def orm_get_dont_sended_mailing():
    async with SESSION_MAKER() as session:
        query = select(Mailings).where(Mailings.is_sended == False)
        result = await session.execute(query)
    return result.scalars().all()

async def orm_set_sended_mailing(mailing : Mailings):
    async with SESSION_MAKER() as session:
        query = update(Mailings).where(Mailings.id == mailing.id).values(is_sended=True)
        await session.execute(query)
        await session.commit()
