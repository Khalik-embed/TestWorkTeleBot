import math
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from datetime import datetime, timezone
from database.models import (Users,
                             Banners,
                             Category,
                             SubCategory,
                             Items,
                             Basket,
                             FAQ,
                             Mailings)


######## users ##############
async def orm_check_if_user_exist (async_session: AsyncSession, user_id: int) -> bool:
    async with async_session() as session:
        query = select(Users).where(Users.user_id == user_id)
        result = await session.execute(query)
    if result.scalar():
        return True
    else:
        return False

async def orm_add_user (async_session: AsyncSession, user_id: int, user_name:str) -> bool:
    async with async_session() as session:
        user = Users(user_id = user_id,
                     user_name = user_name,
                     time_create = datetime.now(),
                     time_update = datetime.now(), )
        session.add(user)
        result = await session.flush()
        result = await session.commit()

async def orm_update_user (async_session: AsyncSession, user_id: int, user_name:str) -> bool:
    async with async_session() as session:
        query = update(Users).where(Users.user_id == user_id).values(user_name=user_name,
                                                                    time_update = datetime.now())
        await session.execute(query)
        await session.commit()

async def orm_get_user_ids (async_session: AsyncSession) -> bool:
    async with async_session() as session:
        query = select(Users.user_id)
        result = await session.execute(query)
    return result.scalars().all()

######## Banners ##############
async def orm_get_banner (async_session: AsyncSession, slug : str) -> Banners:
    async with async_session() as session:
        query = select(Banners).where(Banners.slug == slug)
        result = await session.execute(query)
    return result.scalar()

######### Images ############################
async def orm_set_photo_tg_id (async_session: AsyncSession, orm_object : Items | Banners, file_id :str) -> Banners:
    async with async_session() as session:
        if type(orm_object) == Items:
            query = update(Items).where(Items.photo == orm_object.photo).values(photo_tg_id=file_id)
        else:
            query = update(Banners).where(Banners.photo == orm_object.photo).values(photo_tg_id=file_id)
        await session.execute(query)
        result = await session.commit()

######### Catalog  #############
async def orm_get_categories(async_session: AsyncSession) -> dict [str, str]:
    async with async_session() as session:
        query = select(Category).join(Items, Items.category_id == Category.id).distinct()
        result = await session.execute(query)
    return result.scalars().all()

async def orm_get_subcategories(async_session: AsyncSession, category_id : int) -> dict [str, str]:
    async with async_session() as session:
        query = select(SubCategory).join(Items, Items.subcategory_id == SubCategory.id).filter(SubCategory.category_id == category_id).distinct()
        result = await session.execute(query)
    return result.scalars().all()

async def orm_get_item(async_session: AsyncSession, subcategory_id : int) -> dict [str, str]:
    async with async_session() as session:
        query = select(Items).filter(Items.subcategory_id == subcategory_id)
        result = await session.execute(query)
    return result.scalars().all()

################# backet ######################
async def orm_get_last_unpayed_user_basket(async_session: AsyncSession, user_id: int | str):
    async with async_session() as session:
        query = select(Users).where(Users.user_id == int(user_id))
        user = await session.execute(query)
        user = user.scalar()
        query = select(Basket).filter(Basket.user_id == user.id, Basket.paid == False)
        result = await session.execute(query)
    return result.scalars().all()



async def orm_add_to_basket(async_session: AsyncSession, user_id : int | str, item_id : int | str):
    user : Users = None
    item : Items = None
    async with async_session() as session:
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

async def orm_delete_from_basket(async_session: AsyncSession, user_id: int | str, item_id: int | str):
    async with async_session() as session:
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

async def orm_reduce_product_in_basket(async_session: AsyncSession, user_id: int, item_id: int):
    async with async_session() as session:
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

####################### FAQ #######################################
async def orm_get_question_from_faq(async_session: AsyncSession):
    async with async_session() as session:
        query = select(FAQ.question)
        result = await session.execute(query)
    return result.scalars().all()

async def orm_get_answer_from_faq(async_session: AsyncSession, question : str):
    async with async_session() as session:
        query = select(FAQ.answer).where(FAQ.question == question)
        result = await session.execute(query)
    return result.scalars().all()

async def orm_add_question_to_faq(async_session: AsyncSession, question : str):
    async with async_session() as session:
        query = select(FAQ.answer).where(FAQ.question == question)
        result = await session.execute(query)
    return result.scalars().all()

######################### MAILINGS ####################################
async def orm_get_dont_sended_mailing(async_session: AsyncSession):
    async with async_session() as session:
        query = select(Mailings).where(Mailings.is_sended == False)
        result = await session.execute(query)
    return result.scalars().all()

async def orm_set_sended_mailing(async_session: AsyncSession, mailing : Mailings):
    async with async_session() as session:
        query = update(Mailings).where(Mailings.id == mailing.id).values(is_sended=True)
        await session.execute(query)
        await session.commit()
