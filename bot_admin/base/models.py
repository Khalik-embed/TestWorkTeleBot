from django.db import models
from lexicon import (
    USER,           USERS,          CATEGORY,
    CATEGORYES,     SUB_CATEGORY,   SUB_CATEGORES,
    ITEM,           ITEMS,          MAILING,
    MAILINGS,       BANNER,         BANNERS,
    PAID_ORDER,     PAID_ORDERS,    BACKET,
    FAQ)

class Users(models.Model):
    user_id = models.BigIntegerField(unique = True)
    user_name = models.CharField(max_length = 255, blank = True)
    time_create = models.DateTimeField(auto_now_add = True)
    time_update = models.DateTimeField(auto_now = True)
    class Meta:
        verbose_name = USER
        verbose_name_plural = USERS

class Categories(models.Model):
    name = models.CharField(max_length = 255, db_index = True)
    slug = models.SlugField(max_length = 255, unique = True, db_index = True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = CATEGORY
        verbose_name_plural = CATEGORYES

class SubCategories(models.Model):
    name = models.CharField(max_length = 255, db_index = True)
    slug = models.SlugField(max_length = 255, unique = True, db_index = True)
    category = models.ForeignKey('Categories', on_delete=models.PROTECT)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = SUB_CATEGORY
        verbose_name_plural = SUB_CATEGORES

class Items(models.Model):
    articul = models.IntegerField()
    item_name = models.CharField(max_length = 255)
    item_description = models.TextField(blank = True)
    category = models.ForeignKey('Categories', on_delete = models.PROTECT)
    subcategory = models.ForeignKey('SubCategories', on_delete = models.PROTECT)
    cost = models.FloatField()
    photo = models.ImageField(upload_to = "photos",
                              default = None,
                              blank = True,
                              null = True)
    photo_tg_id = models.SlugField(max_length = 255, blank = True)
    class Meta:
        verbose_name = ITEM
        verbose_name_plural = ITEMS

class Mailings(models.Model):
    mailling_text = models.TextField(blank = True)
    photo = models.ImageField(upload_to = "photos",
                              default = None,
                              blank = True,
                              null = True)
    photo_tg_id = models.SlugField(max_length = 255,
                                   blank = True)
    is_sended = models.BooleanField(default = False)
    class Meta:
        verbose_name = MAILING
        verbose_name_plural = MAILINGS

class Banners(models.Model):
    name = models.CharField(max_length = 255)
    slug =  models.SlugField(max_length = 255,
                             unique = True,
                             db_index = True)
    text = models.TextField(blank = True)
    photo = models.ImageField(upload_to = "photos",
                              default = None,
                              blank = True,
                              null = True)
    photo_tg_id = models.SlugField(max_length = 255,
                                   blank = True)
    class Meta:
        verbose_name = BANNER
        verbose_name_plural = BANNERS

class PaidOrder(models.Model):
    total_amount =  models.IntegerField(blank = True, null = True)
    telegram_payment_charge_id = models.SlugField(max_length = 255,
                                                  blank = True,
                                                  null = True)
    provider_payment_charge_id = models.SlugField(max_length = 255,
                                                  null = True)
    shipping_option = models.TextField(blank = True, null = True)
    contact_name = models.TextField(blank = True, null = True)
    contact_phone_number = models.TextField(blank = True, null = True)
    shipping_state = models.TextField(blank = True, null = True)
    shipping_city = models.TextField(blank = True, null = True)
    shipping_street_line1 = models.TextField(blank = True, null = True)
    shipping_street_line2 = models.TextField(blank = True, null = True)
    shipping_post_code = models.TextField(blank = True, null = True)
    time_create = models.DateTimeField(auto_now_add = True)
    class Meta:
        verbose_name = PAID_ORDER
        verbose_name_plural = PAID_ORDERS

class Basket(models.Model):
    item = models.ForeignKey('Items', on_delete = models.PROTECT)
    user = models.ForeignKey('Users', on_delete = models.PROTECT)
    count =  models.IntegerField()
    paid_order = models.ForeignKey('PaidOrder', on_delete = models.PROTECT, blank=True, null=True)
    paid = models.BooleanField(default = False)
    time_create = models.DateTimeField(auto_now_add = True)
    class Meta:
        verbose_name = BACKET
        verbose_name_plural = BACKET

class FAQ(models.Model):
    question = models.TextField(null=True)
    answer = models.TextField(null=True)
    class Meta:
        verbose_name = FAQ
        verbose_name_plural = FAQ
