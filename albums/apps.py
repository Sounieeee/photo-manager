"""Albums application configuration"""
from django.apps import AppConfig  # type: ignore


class AlbumsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'albums'
    verbose_name = 'Photo Albums'
