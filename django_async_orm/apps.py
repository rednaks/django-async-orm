import logging
from django.apps import AppConfig, apps

from django_async_orm.manager import AsyncManager


class AsyncOrmConfig(AppConfig):
    name = 'django_async_orm'

    def ready(self):
        logging.info('AsyncORM: patching models')
        for model in apps.get_models(include_auto_created=True):
            model.objects = AsyncManager()
            model.objects.model = model
