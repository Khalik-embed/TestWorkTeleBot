# Generated by Django 5.0.4 on 2024-04-10 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_alter_banners_options_alter_categories_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='banners',
            name='slug',
            field=models.SlugField(default=1, max_length=255, unique=True),
            preserve_default=False,
        ),
    ]
