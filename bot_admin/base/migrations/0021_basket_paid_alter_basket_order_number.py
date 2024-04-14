# Generated by Django 5.0.4 on 2024-04-12 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0020_alter_basket_delivery_place'),
    ]

    operations = [
        migrations.AddField(
            model_name='basket',
            name='paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='basket',
            name='order_number',
            field=models.IntegerField(null=True),
        ),
    ]
