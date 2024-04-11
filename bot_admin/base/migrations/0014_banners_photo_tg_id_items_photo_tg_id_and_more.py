# Generated by Django 5.0.4 on 2024-04-10 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_banners_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='banners',
            name='photo_tg_id',
            field=models.SlugField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='items',
            name='photo_tg_id',
            field=models.SlugField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='mailings',
            name='photo_tg_id',
            field=models.SlugField(blank=True, max_length=255),
        ),
    ]