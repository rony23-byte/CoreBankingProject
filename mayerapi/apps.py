from django.apps import AppConfig
from mayerapi import models


class MayerapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mayerapi'
