import concurrent

from channels.db import database_sync_to_async as sync_to_async
from django.db.models import QuerySet

from django_async_orm.iter import AsyncIter


class QuerySetAsync(QuerySet):
    def __init__(self, model=None, query=None, using=None, hints=None):
        super().__init__(model, query, using, hints)

    async def aget(self, *args, **kwargs):
        return await sync_to_async(self.get, thread_sensitive=1)(*args, **kwargs)

    async def acreate(self, **kwargs):
        return await sync_to_async(self.create, thread_sensitive=True)(**kwargs)

    async def abulk_create(self, obs, batch_size=None, ignore_conflicts=False):
        return await sync_to_async(self.bulk_create, thread_sensitive=True)(
            obs, batch_size=batch_size, ignore_conflicts=ignore_conflicts
        )

    async def abulk_update(self, objs, fields, batch_size=None):
        return await sync_to_async(self.bulk_update, thread_sensitive=True)(
            objs=objs, fields=fields, batch_size=batch_size
        )

    async def aget_or_create(self, defaults=None, **kwargs):
        return await sync_to_async(self.get_or_create, thread_sensitive=True)(
            defaults=defaults, **kwargs
        )

    async def aupdate_or_create(self, defaults=None, **kwargs):
        return await sync_to_async(self.update_or_create, thread_sensitive=True)(
            defaults=defaults, **kwargs
        )

    async def aearliest(self, *fields):
        return await sync_to_async(self.earliest, thread_sensitive=True)(*fields)

    async def alatest(self, *fields):
        return await sync_to_async(self.latest, thread_sensitive=True)(*fields)

    async def afirst(self):
        return await sync_to_async(self.first, thread_sensitive=True)()

    async def anone(self):
        return await sync_to_async(self.none, thread_sensitive=True)()

    async def alast(self):
        return await sync_to_async(self.last, thread_sensitive=True)()

    async def ain_bulk(self, id_list=None, *_, field_name="pk"):
        return await sync_to_async(self.in_bulk, thread_sensitive=True)(
            id_list=id_list, *_, field_name=field_name
        )

    async def adelete(self):
        return await sync_to_async(self.delete, thread_sensitive=True)()

    async def aupdate(self, **kwargs):
        return await sync_to_async(self.update, thread_sensitive=True)(**kwargs)

    async def aexists(self):
        return await sync_to_async(self.exists, thread_sensitive=True)()

    async def acount(self):
        return await sync_to_async(self.count, thread_sensitive=True)()

    async def aexplain(self, *_, format=None, **options):
        return await sync_to_async(self.explain, thread_sensitive=True)(
            *_, format=format, **options
        )

    async def araw(self, raw_query, params=None, translations=None, using=None):
        return await sync_to_async(self.raw, thread_sensitive=True)(
            raw_query, params=params, translations=translations, using=using
        )

    def __aiter__(self):
        self._fetch_all()
        return AsyncIter(self._result_cache)

    def _fetch_all(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future_fetch_all = executor.submit(super(QuerySetAsync, self)._fetch_all)

    ##################################################################
    # PUBLIC METHODS THAT ALTER ATTRIBUTES AND RETURN A NEW QUERYSET #
    ##################################################################

    async def aall(self):
        return await sync_to_async(self.all, thread_sensitive=True)()

    async def afilter(self, *args, **kwargs):
        return await sync_to_async(self.filter, thread_sensitive=True)(*args, **kwargs)

    async def aexclude(self, *args, **kwargs):
        return await sync_to_async(self.exclude, thread_sensitive=True)(*args, **kwargs)

    async def acomplex_filter(self, filter_obj):
        return await sync_to_async(self.complex_filter, thread_sensitive=True)(
            filter_obj
        )

    async def aunion(self, *other_qs, all=False):
        return await sync_to_async(self.union, thread_sensitive=True)(
            *other_qs, all=all
        )

    async def aintersection(self, *other_qs):
        return await sync_to_async(self.intersection, thread_sensitive=True)(*other_qs)

    async def adifference(self, *other_qs):
        return await sync_to_async(self.difference, thread_sensitive=True)(*other_qs)

    async def aselect_for_update(self, nowait=False, skip_locked=False, of=()):
        return await sync_to_async(self.select_for_update, thread_sensitive=True)(
            nowait=nowait, skip_locked=skip_locked, of=of
        )

    async def aprefetch_related(self, *lookups):
        return await sync_to_async(self.prefetch_related, thread_sensitive=True)(
            *lookups
        )

    async def aannotate(self, *args, **kwargs):
        return await sync_to_async(self.annotate, thread_sensitive=True)(
            *args, **kwargs
        )

    async def aorder_by(self, *field_names):
        return await sync_to_async(self.order_by, thread_sensitive=True)(*field_names)

    async def adistinct(self, *field_names):
        return await sync_to_async(self.distinct, thread_sensitive=True)(*field_names)

    async def aextra(
        self,
        select=None,
        where=None,
        params=None,
        tables=None,
        order_by=None,
        select_params=None,
    ):
        return await sync_to_async(self.extra, thread_sensitive=True)(
            select, where, params, tables, order_by, select_params
        )

    async def areverse(self):
        return await sync_to_async(self.reverse, thread_sensitive=True)()

    async def adefer(self, *fields):
        return await sync_to_async(self.defer, thread_sensitive=True)(*fields)

    async def aonly(self, *fields):
        return await sync_to_async(self.only, thread_sensitive=True)(*fields)

    async def ausing(self, alias):
        return await sync_to_async(self.using, thread_sensitive=True)(alias)

    async def aresolve_expression(self, *args, **kwargs):
        return await sync_to_async(self.resolve_expression, thread_sensitive=True)(
            *args, **kwargs
        )

    @property
    async def aordered(self):
        def _ordered():
            return super(QuerySetAsync, self).ordered

        return await sync_to_async(_ordered, thread_sensitive=True)()
