import os
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config.config import CONFIG

# from database.models import Base
# from database.orm_query import orm_add_banner_description, orm_create_categories

# from common.texts_for_db import categories, description_for_info_pages


DB_URL="postgresql+asyncpg://{login}:{password}@{host}:{port}/{db_name}".format(
        login = CONFIG.db_config.user,
        password = CONFIG.db_config.password,
        host = CONFIG.db_config.host,
        port = CONFIG.db_config.port,
        db_name = CONFIG.db_config.name,
    )

engine = create_async_engine(DB_URL, echo=True)

session_maker = async_sessionmaker(bind=engine)
