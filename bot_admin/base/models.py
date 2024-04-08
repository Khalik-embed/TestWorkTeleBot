from django.db import models

class Users(models.Model):
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=255,blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

class Categories(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    def __str__(self):
        return self.name

class SubCategories(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    def __str__(self):
        return self.name

class Items(models.Model):
    item_code = models.IntegerField()
    item_name = models.CharField(max_length=255)
    item_description = models.TextField(blank=True)
    category = models.ForeignKey('Categories', on_delete=models.PROTECT)
    sub_category = models.ForeignKey('SubCategories', on_delete=models.PROTECT)
#    photo =

class Mailings(models.Model):
    mailling_text = models.CharField(max_length=255)
    time_to_send = models.DateTimeField()
# photo =

# class Basket(models.Model):
#     item_code = models.CharField(max_length=255)
#     # LIST OF ITEM
#     # item_name = models.CharField(max_length=255)
#     # count =  models.IntegerField()
#     user_id = models.IntegerField()
#     user_name = models.CharField(max_length=255, blank=True)
#     count =  models.IntegerField()
#     delivery_place = models.TextField(blank=True)
