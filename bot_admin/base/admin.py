from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import (
    Users,      Categories,     SubCategories,
    Items,      Mailings,       Banners,
    Basket,     PaidOrder,      FAQ)

from lexicon import (
    PICTURE,        TG_USER_NAME,       NAME_OF_ITEM,
    ARTICUL_OF_ITEM,   PICTURE_OF_ITEM, PAID_ORDER_ID)



@admin.register(Items)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('articul', 'item_name', 'cost', 'category', 'subcategory', 'post_photo')
    list_display_links = ('item_name', 'articul')

    @admin.display(description=PICTURE)
    def post_photo(self, item: Items):
        if item.photo:
            return mark_safe(f"<img src='{item.photo.url}' width=50>")
        return "None"

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user_name', 'time_create', 'time_update')
    list_display_links = ('user_id', 'user_name')

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_display_links = ('name',)

@admin.register(SubCategories)
class SubCategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug')
    list_display_links = ('name',)

@admin.register(Mailings)
class MailingsAdmin(admin.ModelAdmin):
    list_display = ('mailling_text', 'post_photo', 'is_sended')
    list_display_links = ('mailling_text',)

    @admin.display(description=PICTURE)
    def post_photo(self, mailing: Mailings):
        if mailing.photo:
            return mark_safe(f"<img src='{mailing.photo.url}' width=50>")
        return "None"

@admin.register(Banners)
class BannersAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'text', 'post_photo')
    list_display_links = ('name',)

    @admin.display(description=PICTURE)
    def post_photo(self, banner: Banners):
        if banner.photo:
            return mark_safe(f"<img src='{banner.photo.url}' width=50>")
        return "None"

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'paid_order_id',
        'post_item_articul',
        'post_item_name',
        'post_item_photo',
        'count',
        'paid',
        'user_name',
        'time_create')
    list_display_links = ('id',)

    @admin.display(description=PICTURE_OF_ITEM)
    def post_item_photo(self, basket: Basket):
        if basket.item.photo:
            return mark_safe(f"<img src='{basket.item.photo.url}' width=50>")
        return "None"

    @admin.display(description=ARTICUL_OF_ITEM)
    def post_item_articul(self, basket: Basket):
        return f"{basket.item.articul}"

    @admin.display(description=NAME_OF_ITEM)
    def post_item_name(self, basket: Basket):
        return f"{basket.item.item_name}"

    @admin.display(description=TG_USER_NAME)
    def user_name(self, basket: Basket):
        return f"{basket.user.user_name}"

    @admin.display(description=PAID_ORDER_ID)
    def paid_order_id(self, basket: Basket):
        return f"{basket.paid_order.id}"

@admin.register(PaidOrder)
class PaidOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'total_amount','shipping_option', 'contact_name', 'shipping_street_line1', 'time_create')
    list_display_links = ('id',)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question','answer')
    list_display_links = ('question',)
