import datetime
from typing import Annotated
from sqlalchemy import Column, Integer, String, Text, ForeignKey, text
from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text, BigInteger, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass

intpk = Annotated[int, mapped_column(primary_key=True)]
# created_at: Mapped[datetime] = mapped_column(server_default=func.now())
# updated_at: Mapped[datetime] = mapped_column(
#         server_default=FetchedValue(), server_onupdate=FetchedValue()
#     )

class Users(Base):
    __tablename__ = 'base_users'
    id: Mapped[intpk]
    user_id: Mapped[int] = Column(Integer, primary_key=True)
    user_name: Mapped[str] = Column(String(255), nullable=True)
    time_create =  Column(DateTime, server_default=func.now())
    time_update = Column(DateTime, server_default=func.now(), onupdate=func.now())

class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[intpk]
    name = Column(String(255), index=True)
    slug = Column(String(255), unique=True, index=True)

    def __repr__(self):
        return f"<Category(name={self.name}, slug={self.slug})>"


class SubCategory(Base):
    __tablename__ = 'subcategories'

    id: Mapped[intpk]
    name = Column(String(255), index=True)
    slug = Column(String(255), unique=True, index=True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    category = relationship("Category", backref="subcategories")


class Items(Base):
    __tablename__ = 'items'

    id: Mapped[intpk]
    item_code = Column(Integer)
    item_name = Column(String(255))
    item_description = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    sub_category_id = Column(Integer, ForeignKey('subcategories.id'), nullable=False)
    photo = Column(String, nullable=True)
    category = relationship("Category", backref="items")
    sub_category = relationship("SubCategory", backref="items")
    photo_tg_id = Column(Text)
    def __repr__(self):
        return f"<Item(item_code={self.item_code}, item_name={self.item_name})>"

class Banners(Base):
    __tablename__ = 'base_banners'
    id: Mapped[intpk]

    name : Mapped[str] = Column(String(255))
    slug : Mapped[str] = Column(String(255))
    text = Column(Text)
    photo =  Column(Text)
    photo_tg_id = Column(Text)