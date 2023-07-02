import logging

from django.apps import AppConfig, apps

from django_async_orm.utils import patch_manager


class AsyncOrmConfig(AppConfig):
    name = "django_async_orm"

    def ready(self):
        logging.info("Patching models to add async ORM capabilities...")
        for model in apps.get_models(include_auto_created=True):
            patch_manager(model)
            # TODO: patch_model(model)
