from typing import Annotated
from sqlalchemy import (
    Column,     Integer,    Boolean,
    Text,       Float,      DateTime,
    ForeignKey, String,     UUID,
    Double,     func)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

intpk = Annotated[int, mapped_column(primary_key = True)]


class Users(Base):
    __tablename__ = 'base_users'
    id : Mapped[intpk]
    user_id : Mapped[int] = Column(Double, unique = True)
    user_name : Mapped[str] = Column(String(255), nullable = True)
    time_create =  Column(DateTime, server_default = func.now())
    time_update = Column(DateTime, server_default = func.now(), onupdate = func.now())

class Category(Base):
    __tablename__ = 'base_categories'

    id: Mapped[intpk]
    name = Column(String(255), index = True)
    slug = Column(String(255), unique = True, index = True)

    def __repr__(self):
        return f"<Category(name={self.name}, slug={self.slug})>"


class SubCategory(Base):
    __tablename__ = 'base_subcategories'

    id: Mapped[intpk]
    name = Column(String(255), index = True)
    slug = Column(String(255), unique = True, index = True)
    category_id = Column(Integer, ForeignKey('base_categories.id'), nullable = False)
    category = relationship("Category", backref = "subcategories")


class Items(Base):
    __tablename__ = 'base_items'

    id: Mapped[intpk]
    articul = Column(Integer)
    item_name = Column(String(255))
    item_description = Column(Text, nullable = True)
    cost = Column(Float)
    category_id = Column(Integer, ForeignKey('base_categories.id'), nullable = False)
    subcategory_id = Column(Integer, ForeignKey('base_subcategories.id'), nullable = False)
    photo = Column(String, nullable = True)
    category = relationship("Category", backref = "items")
    sub_category = relationship("SubCategory", backref = "items")

    photo_tg_id = Column(Text)
    def __repr__(self):
        return f"<Item(articul={self.articul}, item_name={self.item_name})>"

class Banners(Base):
    __tablename__ = 'base_banners'
    id: Mapped[intpk]

    name : Mapped[str] = Column(String(255))
    slug : Mapped[str] = Column(String(255))
    text = Column(Text)
    photo =  Column(Text)
    photo_tg_id = Column(Text)

class PaidOrder(Base):
    __tablename__ = 'base_paidorder'
    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    total_amount = Column(Integer, nullable = True)
    telegram_payment_charge_id = Column(Text, nullable = True)
    provider_payment_charge_id = Column(Text, nullable = True)
    shipping_option = Column(Text, nullable = True)
    contact_name = Column(Text, nullable = True)
    contact_phone_number = Column(Text, nullable = True)
    shipping_state = Column(Text, nullable = True)
    shipping_city = Column(Text, nullable = True)
    shipping_street_line1 = Column(Text, nullable = True)
    shipping_street_line2 = Column(Text, nullable = True)
    shipping_post_code = Column(Text, nullable = True)
    time_create = Column(DateTime, server_default = func.now())

class Basket(Base):
    __tablename__ = 'base_basket'
    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    item_id = Column(Integer, ForeignKey('base_items.id'), nullable = False)
    user_id = Column(Integer, ForeignKey('base_users.id'), nullable = False)
    count =  Column(Integer)
    paid_order_id = Column(Integer, ForeignKey('base_paidorder.id'), nullable = True)
    paid = Column(Boolean, default = False)
    time_create = Column(DateTime, server_default = func.now())

    item = relationship("Items", lazy = "joined")
    user = relationship("Users", lazy = "joined")
    paid_order = relationship("PaidOrder", lazy = "joined")

class Mailings(Base):
    __tablename__ = 'base_mailings'
    id: Mapped[int] = mapped_column(primary_key = True,
                                    autoincrement = True)
    mailling_text = Column(Text, nullable = True)
    photo = Column(String, nullable = True)
    photo_tg_id = Column(Text)
    is_sended = Column(Boolean, default = False)

class FAQ(Base):
    __tablename__ = 'base_faq'
    id: Mapped[int] = mapped_column(primary_key = True,
                                    autoincrement = True)
    question = Column(String, nullable = True)
    answer = Column(String, nullable = True)