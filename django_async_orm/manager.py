

from django.db.models.manager import BaseManager

from django_async_orm.query import QuerySetAsync


class AsyncManager(BaseManager.from_queryset(QuerySetAsync)):
    pass
