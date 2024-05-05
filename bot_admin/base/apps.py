from django.apps import AppConfig


class BaseConfig(AppConfig):
    verbose_name = "Базы данных"
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'
