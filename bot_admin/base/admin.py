from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Users, Categories, SubCategories, Items, Mailings, UploadImages




@admin.register(Items)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_code', 'item_name', 'category', 'sub_category', 'post_photo')
    list_display_links = ('item_name', 'item_code')

    @admin.display(description="Изображение")
    def post_photo(self, item: Items):
        if item.photo:
            return mark_safe(f"<img src='{item.photo.url}' width=50>")
        return "Без фото"

admin.site.register(Users)
admin.site.register(Categories)
admin.site.register(SubCategories)
admin.site.register(Mailings)
admin.site.register(UploadImages)