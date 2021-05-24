import asyncio

from django_async_orm.manager import AsyncManager


class AsyncIter:
    def __init__(self, iterable):
        self._iter = iter(iterable)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            element = next(self._iter)
        except StopIteration:
            raise StopAsyncIteration
        await asyncio.sleep(0)
        return element


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
