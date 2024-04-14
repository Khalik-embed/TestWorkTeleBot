from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import (Users,
                     Categories,
                     SubCategories,
                     Items,
                     Mailings,
                     Banners,
                     Basket)




@admin.register(Items)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('articul', 'item_name', 'cost', 'category', 'subcategory', 'post_photo')
    list_display_links = ('item_name', 'articul')

    @admin.display(description="Изображение")
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
    list_display = ('mailling_text', 'time_to_send', 'post_photo')
    list_display_links = ('mailling_text',)

    @admin.display(description="Изображение")
    def post_photo(self, mailing: Mailings):
        if mailing.photo:
            return mark_safe(f"<img src='{mailing.photo.url}' width=50>")
        return "None"

@admin.register(Banners)
class BannersAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'text', 'post_photo')
    list_display_links = ('name',)

    @admin.display(description="Изображение")
    def post_photo(self, banner: Banners):
        if banner.photo:
            return mark_safe(f"<img src='{banner.photo.url}' width=50>")
        return "None"

# @admin.register(UploadImages)
# class UploadImagesAdmin(admin.ModelAdmin):
#     list_display = ('Image', 'post_photo')
#     list_display_links = ('Image',)

#     @admin.display(description="Изображение")
#     def post_photo(self, image: UploadImages):
#         if image.photo:
#             return mark_safe(f"<img src='{image.photo.url}' width=50>")
#         return "None"

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('order_number','item', 'count', 'paid', 'user','delivery_place', 'time_create')
    list_display_links = ('item',)
