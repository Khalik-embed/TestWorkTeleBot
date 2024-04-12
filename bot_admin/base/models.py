from django.db import models

class Users(models.Model):
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=255,blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

class Categories(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class SubCategories(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    category = models.ForeignKey('Categories', on_delete=models.PROTECT)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"

class Items(models.Model):
    articul = models.IntegerField()
    item_name = models.CharField(max_length=255)
    item_description = models.TextField(blank=True)
    category = models.ForeignKey('Categories', on_delete=models.PROTECT)
    subcategory = models.ForeignKey('SubCategories', on_delete=models.PROTECT)
    cost = models.FloatField()
    photo = models.ImageField(upload_to="photos", default=None, blank=True, null=True)
    photo_tg_id = models.SlugField(max_length=255, blank=True)
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

class Mailings(models.Model):
    mailling_text = models.TextField(blank=True)
    time_to_send = models.DateTimeField()
    photo = models.ImageField(upload_to="photos", default=None, blank=True, null=True)
    photo_tg_id = models.SlugField(max_length=255, blank=True)
    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

class Banners(models.Model):
    name = models.CharField(max_length=255)
    slug =  models.SlugField(max_length=255, unique=True, db_index=True)
    text = models.TextField(blank=True)
    photo = models.ImageField(upload_to="photos", default=None, blank=True, null=True)
    photo_tg_id = models.SlugField(max_length=255, blank=True)
    class Meta:
        verbose_name = "Баннер"
        verbose_name_plural = "Баннеры"

# class UploadImages(models.Model):
#     #name = models.CharField(max_length=255)
#     Image = models.ImageField(upload_to='uploads_model')
#     Tg_id = models.TextField(max_length=255, blank=True, null=True)
#     class Meta:
#         verbose_name = "Фото"
#         verbose_name_plural = "Фотографии"


class Basket(models.Model):
    item = models.ForeignKey('Items', on_delete=models.PROTECT)
    user = models.ForeignKey('Users', on_delete=models.PROTECT)
    count =  models.IntegerField()
    delivery_place = models.TextField(blank=True)
    order_number = models.IntegerField()
    time_create = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
