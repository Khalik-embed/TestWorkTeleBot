# Generated by Django 5.0.4 on 2024-04-10 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_banners_alter_mailings_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailings',
            name='mailling_text',
            field=models.TextField(blank=True),
        ),
    ]
