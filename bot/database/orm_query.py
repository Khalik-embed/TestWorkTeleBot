import math
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from datetime import datetime, timezone
from database.models import Users, Banners


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

######## Banners ##############
async def orm_get_banner (async_session: AsyncSession, slug : str) -> Banners:
    async with async_session() as session:
        query = select(Banners).where(Banners.slug == slug)
        result = await session.execute(query)
    return result.scalar()

async def orm_set_banner_photo_id (async_session: AsyncSession, banner : Banners, file_id :str) -> Banners:
    async with async_session() as session:
        query = update(Banners).where(Banners.id == banner.id).values(photo_tg_id=file_id)
        await session.execute(query)
        result = await session.commit()


# async def orm_set_banner_photo_id (async_session: AsyncSession, slug : str) -> Banners:
#     async with async_session() as session:
#         query = select(Banners).where(Banners.slug == slug)

# async def insert_objects(async_session: async_sessionmaker[AsyncSession]) -> None:
#     async with async_session() as session:
#         async with session.begin():
#             session.add_all(
#             [
#                 A(bs=[B(data="b1"), B(data="b2")], data="a1"),
#                 A(bs=[], data="a2"),
#                 A(bs=[B(data="b3"), B(data="b4")], data="a3"),
#             ]
#         )



# ############### Работа с баннерами (информационными страницами) ###############

# async def orm_add_banner_description(session: AsyncSession, data: dict):
#     #Добавляем новый или изменяем существующий по именам
#     #пунктов меню: main, about, cart, shipping, payment, catalog
#     query = select(Banner)
#     result = await session.execute(query)
#     if result.first():
#         return
#     session.add_all([Banner(name=name, description=description) for name, description in data.items()])
#     await session.commit()


# async def orm_change_banner_image(session: AsyncSession, name: str, image: str):
#     query = update(Banner).where(Banner.name == name).values(image=image)
#     await session.execute(query)
#     await session.commit()


# async def orm_get_banner(session: AsyncSession, page: str):
#     query = select(Banner).where(Banner.name == page)
#     result = await session.execute(query)
#     return result.scalar()


# async def orm_get_info_pages(session: AsyncSession):
#     query = select(Banner)
#     result = await session.execute(query)
#     return result.scalars().all()


# ############################ Категории ######################################

# async def orm_get_categories(session: AsyncSession):
#     query = select(Category)
#     result = await session.execute(query)
#     return result.scalars().all()

# async def orm_create_categories(session: AsyncSession, categories: list):
#     query = select(Category)
#     result = await session.execute(query)
#     if result.first():
#         return
#     session.add_all([Category(name=name) for name in categories])
#     await session.commit()

# ############ Админка: добавить/изменить/удалить товар ########################

# async def orm_add_product(session: AsyncSession, data: dict):
#     obj = Product(
#         name=data["name"],
#         description=data["description"],
#         price=float(data["price"]),
#         image=data["image"],
#         category_id=int(data["category"]),
#     )
#     session.add(obj)
#     await session.commit()


# async def orm_get_products(session: AsyncSession, category_id):
#     query = select(Product).where(Product.category_id == int(category_id))
#     result = await session.execute(query)
#     return result.scalars().all()


# async def orm_get_product(session: AsyncSession, product_id: int):
#     query = select(Product).where(Product.id == product_id)
#     result = await session.execute(query)
#     return result.scalar()


# async def orm_update_product(session: AsyncSession, product_id: int, data):
#     query = (
#         update(Product)
#         .where(Product.id == product_id)
#         .values(
#             name=data["name"],
#             description=data["description"],
#             price=float(data["price"]),
#             image=data["image"],
#             category_id=int(data["category"]),
#         )
#     )
#     await session.execute(query)
#     await session.commit()


# async def orm_delete_product(session: AsyncSession, product_id: int):
#     query = delete(Product).where(Product.id == product_id)
#     await session.execute(query)
#     await session.commit()

# ##################### Добавляем юзера в БД #####################################

# async def orm_add_user(
#     session: AsyncSession,
#     user_id: int,
#     first_name: str | None = None,
#     last_name: str | None = None,
#     phone: str | None = None,
# ):
#     query = select(User).where(User.user_id == user_id)
#     result = await session.execute(query)
#     if result.first() is None:
#         session.add(
#             User(user_id=user_id, first_name=first_name, last_name=last_name, phone=phone)
#         )
#         await session.commit()


# ######################## Работа с корзинами #######################################

# async def orm_add_to_cart(session: AsyncSession, user_id: int, product_id: int):
#     query = select(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id)
#     cart = await session.execute(query)
#     cart = cart.scalar()
#     if cart:
#         cart.quantity += 1
#         await session.commit()
#         return cart
#     else:
#         session.add(Cart(user_id=user_id, product_id=product_id, quantity=1))
#         await session.commit()



# async def orm_get_user_carts(session: AsyncSession, user_id):
#     query = select(Cart).filter(Cart.user_id == user_id).options(joinedload(Cart.product))
#     result = await session.execute(query)
#     return result.scalars().all()


# async def orm_delete_from_cart(session: AsyncSession, user_id: int, product_id: int):
#     query = delete(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id)
#     await session.execute(query)
#     await session.commit()


# async def orm_reduce_product_in_cart(session: AsyncSession, user_id: int, product_id: int):
#     query = select(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id)
#     cart = await session.execute(query)
#     cart = cart.scalar()

#     if not cart:
#         return
#     if cart.quantity > 1:
#         cart.quantity -= 1
#         await session.commit()
#         return True
#     else:
#         await orm_delete_from_cart(session, user_id, product_id)
#         await session.commit()
#         return False
