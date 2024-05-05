# Generated by Django 5.0.4 on 2024-05-02 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_rename_paidorder_basket_paid_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paidorder',
            name='contact_name',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='paidorder',
            name='contact_phone_number',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='paidorder',
            name='provider_payment_charge_id',
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='paidorder',
            name='shipping_city',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='paidorder',
            name='shipping_option',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='paidorder',
            name='shipping_post_code',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='paidorder',
            name='shipping_state',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='paidorder',
            name='shipping_street_line1',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='paidorder',
            name='shipping_street_line2',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='paidorder',
            name='telegram_payment_charge_id',
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='paidorder',
            name='total_amount',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]