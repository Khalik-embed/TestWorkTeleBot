# Generated by Django 5.0.4 on 2024-04-08 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_uploadimages_alter_categories_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='photo',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='photos'),
        ),
    ]