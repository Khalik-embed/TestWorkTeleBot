from django.db import models

class Users(models.Model):
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=255,blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

class Categories(models.Model):
    category_name = models.CharField(max_length=255)

class SubCategories(models.Model):
    sub_category_name = models.CharField(max_length=255)

class Items(models.Model):
    item_code = models.IntegerField()
    item_name = models.CharField(max_length=255)
    item_description = models.TextField(blank=True)
    sub_category_name = models.CharField(max_length=255)
    category_name = models.CharField(max_length=255)
#    photo =

class Mailings(models.Model):
    mailling_text = models.CharField(max_length=255)
    time_to_send = models.DateTimeField()
# photo =

class Basket(models.Model):
    item_code = models.CharField(max_length=255)
    item_name = models.CharField(max_length=255)
    count =  models.IntegerField()
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=255, blank=True)
    count =  models.IntegerField()
    delivery_place = models.TextField(blank=True)
