from aiogram import Bot
from aiogram.types import FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Banners
from database.orm_query import orm_set_banner_photo_id

def get_photo_id(banner : Banners) -> str:
    if banner.photo_tg_id:
        return banner.photo_tg_id
    else:
        local_path = "./media/" + banner.photo
        return FSInputFile(local_path)

async def set_photo_id(async_session: AsyncSession,
                       banner : Banners,
                       file_id :str):
    await orm_set_banner_photo_id(async_session = async_session,
                                  banner = banner, file_id = file_id)