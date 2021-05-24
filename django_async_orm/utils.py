
from django_async_orm.manager import AsyncManager


def async_user_manager_factory():
    from django.contrib.auth.models import UserManager

    class AsyncUserManager(UserManager, AsyncManager):
        pass

    return AsyncUserManager


def patch_manager(model):
    from django.contrib.auth.models import UserManager
    async_manager_cls = AsyncManager
    if isinstance(model.objects, UserManager):
        async_manager_cls = async_user_manager_factory()

    model.objects = async_manager_cls()
    model.objects.model = model
