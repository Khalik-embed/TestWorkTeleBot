from aiogram import Bot
from aiogram.types import FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Banners, Items, Mailings
from database.orm_query import orm_set_photo_tg_id

def get_photo_id(orm_object : Banners | Items | Mailings) -> str:
    if orm_object.photo_tg_id:
        return orm_object.photo_tg_id
    else:
        local_path = "./media/" + orm_object.photo
        return FSInputFile(local_path)

async def set_photo_id(orm_object : Banners | Items | Mailings,
                       file_id : str) -> None:
    if orm_object.photo_tg_id:
        return
    else:
        await orm_set_photo_tg_id(orm_object = orm_object, file_id = file_id)
