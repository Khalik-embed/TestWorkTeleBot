# Generated by Django 5.0.4 on 2024-05-05 13:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_alter_users_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailings',
            name='time_to_send',
        ),
    ]