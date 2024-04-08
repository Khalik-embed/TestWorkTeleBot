from django.db import models

class Users(models.Model):
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=255,blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователи"

class Categories(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категории"
        verbose_name_plural = "Категории"

class SubCategories(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    category = models.ForeignKey('Categories', on_delete=models.PROTECT)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Подкатегории"
        verbose_name_plural = "Подкатегории"

class Items(models.Model):
    item_code = models.IntegerField()
    item_name = models.CharField(max_length=255)
    item_description = models.TextField(blank=True)
    category = models.ForeignKey('Categories', on_delete=models.PROTECT)
    sub_category = models.ForeignKey('SubCategories', on_delete=models.PROTECT)
    photo = models.ImageField(upload_to="photos", default=None, blank=True, null=True)
    class Meta:
        verbose_name = "Товары"
        verbose_name_plural = "Товары"

class Mailings(models.Model):
    mailling_text = models.CharField(max_length=255)
    time_to_send = models.DateTimeField()
    photo = models.ImageField(upload_to="photos", default=None, blank=True, null=True)
    class Meta:
        verbose_name = "Рассылки"
        verbose_name_plural = "Рассылки"

class UploadImages(models.Model):
    #name = models.CharField(max_length=255)
    Image = models.ImageField(upload_to='uploads_model')
    Tg_id = models.TextField(max_length=255, blank=True, null=True)
    class Meta:
        verbose_name = "Фото"
        verbose_name_plural = "Фотографии"


# class Basket(models.Model):
#     item_code = models.CharField(max_length=255)
#     # LIST OF ITEM
#     # item_name = models.CharField(max_length=255)
#     # count =  models.IntegerField()
#     user_id = models.IntegerField()
#     user_name = models.CharField(max_length=255, blank=True)
#     count =  models.IntegerField()
#     delivery_place = models.TextField(blank=True)
