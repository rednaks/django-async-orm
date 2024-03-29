import concurrent
import warnings

from channels.db import database_sync_to_async as sync_to_async
from django.db.models import QuerySet

from django_async_orm.iter import AsyncIter


def __deprecation_warning():
    warnings.warn(
        "Methods starting with `async_*` are deprecated and will be "
        "removed in a future release. Use `a*` methods instead.",
        category=DeprecationWarning,
        stacklevel=2,
    )


def _prefer_django(method):
    """Decorator used to prioritize Django's QuerySet methods over our custom ones.

    This will help maintain performance when Django adds real async support."""

    def _wrapper(self, *args, **kwargs):
        return getattr(super(QuerySet, self), method.__name__, method)(
            self, *args, **kwargs
        )

    return _wrapper


class QuerySetAsync(QuerySet):
    def __init__(self, model=None, query=None, using=None, hints=None):
        super().__init__(model, query, using, hints)

    @_prefer_django
    async def aget(self, *args, **kwargs):
        return await sync_to_async(self.get, thread_sensitive=True)(*args, **kwargs)

    @_prefer_django
    async def acreate(self, **kwargs):
        return await sync_to_async(self.create, thread_sensitive=True)(**kwargs)

    @_prefer_django
    async def abulk_create(self, obs, batch_size=None, ignore_conflicts=False):
        return await sync_to_async(self.bulk_create, thread_sensitive=True)(
            obs, batch_size=batch_size, ignore_conflicts=ignore_conflicts
        )

    @_prefer_django
    async def abulk_update(self, objs, fields, batch_size=None):
        return await sync_to_async(self.bulk_update, thread_sensitive=True)(
            objs=objs, fields=fields, batch_size=batch_size
        )

    @_prefer_django
    async def aget_or_create(self, defaults=None, **kwargs):
        return await sync_to_async(self.get_or_create, thread_sensitive=True)(
            defaults=defaults, **kwargs
        )

    @_prefer_django
    async def aupdate_or_create(self, defaults=None, **kwargs):
        return await sync_to_async(self.update_or_create, thread_sensitive=True)(
            defaults=defaults, **kwargs
        )

    @_prefer_django
    async def aearliest(self, *fields):
        return await sync_to_async(self.earliest, thread_sensitive=True)(*fields)

    @_prefer_django
    async def alatest(self, *fields):
        return await sync_to_async(self.latest, thread_sensitive=True)(*fields)

    @_prefer_django
    async def afirst(self):
        return await sync_to_async(self.first, thread_sensitive=True)()

    @_prefer_django
    async def anone(self):
        return await sync_to_async(self.none, thread_sensitive=True)()

    @_prefer_django
    async def alast(self):
        return await sync_to_async(self.last, thread_sensitive=True)()

    @_prefer_django
    async def ain_bulk(self, id_list=None, *_, field_name="pk"):
        return await sync_to_async(self.in_bulk, thread_sensitive=True)(
            id_list=id_list, *_, field_name=field_name
        )

    @_prefer_django
    async def adelete(self):
        return await sync_to_async(self.delete, thread_sensitive=True)()

    @_prefer_django
    async def aupdate(self, **kwargs):
        return await sync_to_async(self.update, thread_sensitive=True)(**kwargs)

    @_prefer_django
    async def aexists(self):
        return await sync_to_async(self.exists, thread_sensitive=True)()

    @_prefer_django
    async def acount(self):
        return await sync_to_async(self.count, thread_sensitive=True)()

    @_prefer_django
    async def aexplain(self, *_, format=None, **options):
        return await sync_to_async(self.explain, thread_sensitive=True)(
            *_, format=format, **options
        )

    @_prefer_django
    async def araw(self, raw_query, params=None, translations=None, using=None):
        return await sync_to_async(self.raw, thread_sensitive=True)(
            raw_query, params=params, translations=translations, using=using
        )

    @_prefer_django
    def __aiter__(self):
        self._fetch_all()
        return AsyncIter(self._result_cache)

    def _fetch_all(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future_fetch_all = executor.submit(super(QuerySetAsync, self)._fetch_all)

    ##################################################################
    # PUBLIC METHODS THAT ALTER ATTRIBUTES AND RETURN A NEW QUERYSET #
    ##################################################################

    @_prefer_django
    async def aall(self):
        return await sync_to_async(self.all, thread_sensitive=True)()

    @_prefer_django
    async def afilter(self, *args, **kwargs):
        return await sync_to_async(self.filter, thread_sensitive=True)(*args, **kwargs)

    @_prefer_django
    async def aexclude(self, *args, **kwargs):
        return await sync_to_async(self.exclude, thread_sensitive=True)(*args, **kwargs)

    @_prefer_django
    async def acomplex_filter(self, filter_obj):
        return await sync_to_async(self.complex_filter, thread_sensitive=True)(
            filter_obj
        )

    @_prefer_django
    async def aunion(self, *other_qs, all=False):
        return await sync_to_async(self.union, thread_sensitive=True)(
            *other_qs, all=all
        )

    @_prefer_django
    async def aintersection(self, *other_qs):
        return await sync_to_async(self.intersection, thread_sensitive=True)(*other_qs)

    @_prefer_django
    async def adifference(self, *other_qs):
        return await sync_to_async(self.difference, thread_sensitive=True)(*other_qs)

    @_prefer_django
    async def aselect_for_update(self, nowait=False, skip_locked=False, of=()):
        return await sync_to_async(self.select_for_update, thread_sensitive=True)(
            nowait=nowait, skip_locked=skip_locked, of=of
        )

    @_prefer_django
    async def aprefetch_related(self, *lookups):
        return await sync_to_async(self.prefetch_related, thread_sensitive=True)(
            *lookups
        )

    @_prefer_django
    async def aannotate(self, *args, **kwargs):
        return await sync_to_async(self.annotate, thread_sensitive=True)(
            *args, **kwargs
        )

    @_prefer_django
    async def aorder_by(self, *field_names):
        return await sync_to_async(self.order_by, thread_sensitive=True)(*field_names)

    @_prefer_django
    async def adistinct(self, *field_names):
        return await sync_to_async(self.distinct, thread_sensitive=True)(*field_names)

    @_prefer_django
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

    @_prefer_django
    async def areverse(self):
        return await sync_to_async(self.reverse, thread_sensitive=True)()

    @_prefer_django
    async def adefer(self, *fields):
        return await sync_to_async(self.defer, thread_sensitive=True)(*fields)

    @_prefer_django
    async def aonly(self, *fields):
        return await sync_to_async(self.only, thread_sensitive=True)(*fields)

    @_prefer_django
    async def ausing(self, alias):
        return await sync_to_async(self.using, thread_sensitive=True)(alias)

    @_prefer_django
    async def aresolve_expression(self, *args, **kwargs):
        return await sync_to_async(self.resolve_expression, thread_sensitive=True)(
            *args, **kwargs
        )

    @property
    @_prefer_django
    async def aordered(self):
        def _ordered():
            return super(QuerySetAsync, self).ordered

        return await sync_to_async(_ordered, thread_sensitive=True)()

    #################################
    ### START OF DEPRECATION ZONE ###
    #################################

    async def async_get(self, *args, **kwargs):
        __deprecation_warning()
        return await sync_to_async(self.get, thread_sensitive=True)(*args, **kwargs)

    async def async_create(self, **kwargs):
        __deprecation_warning()
        return await sync_to_async(self.create, thread_sensitive=True)(**kwargs)

    async def async_bulk_create(self, obs, batch_size=None, ignore_conflicts=False):
        __deprecation_warning()
        return await sync_to_async(self.bulk_create, thread_sensitive=True)(
            obs, batch_size=batch_size, ignore_conflicts=ignore_conflicts
        )

    async def async_bulk_update(self, objs, fields, batch_size=None):
        __deprecation_warning()
        return await sync_to_async(self.bulk_update, thread_sensitive=True)(
            objs=objs, fields=fields, batch_size=batch_size
        )

    async def async_get_or_create(self, defaults=None, **kwargs):
        __deprecation_warning()
        return await sync_to_async(self.get_or_create, thread_sensitive=True)(
            defaults=defaults, **kwargs
        )

    async def async_update_or_create(self, defaults=None, **kwargs):
        __deprecation_warning()
        return await sync_to_async(self.update_or_create, thread_sensitive=True)(
            defaults=defaults, **kwargs
        )

    async def async_earliest(self, *fields):
        __deprecation_warning()
        return await sync_to_async(self.earliest, thread_sensitive=True)(*fields)

    async def async_latest(self, *fields):
        __deprecation_warning()
        return await sync_to_async(self.latest, thread_sensitive=True)(*fields)

    async def async_first(self):
        __deprecation_warning()
        return await sync_to_async(self.first, thread_sensitive=True)()

    async def async_none(self):
        __deprecation_warning()
        return await sync_to_async(self.none, thread_sensitive=True)()

    async def async_last(self):
        __deprecation_warning()
        return await sync_to_async(self.last, thread_sensitive=True)()

    async def async_in_bulk(self, id_list=None, *_, field_name="pk"):
        __deprecation_warning()
        return await sync_to_async(self.in_bulk, thread_sensitive=True)(
            id_list=id_list, *_, field_name=field_name
        )

    async def async_delete(self):
        __deprecation_warning()
        return await sync_to_async(self.delete, thread_sensitive=True)()

    async def async_update(self, **kwargs):
        __deprecation_warning()
        return await sync_to_async(self.update, thread_sensitive=True)(**kwargs)

    async def async_exists(self):
        __deprecation_warning()
        return await sync_to_async(self.exists, thread_sensitive=True)()

    async def async_count(self):
        __deprecation_warning()
        return await sync_to_async(self.count, thread_sensitive=True)()

    async def async_explain(self, *_, format=None, **options):
        __deprecation_warning()
        return await sync_to_async(self.explain, thread_sensitive=True)(
            *_, format=format, **options
        )

    async def async_raw(self, raw_query, params=None, translations=None, using=None):
        __deprecation_warning()
        return await sync_to_async(self.raw, thread_sensitive=True)(
            raw_query, params=params, translations=translations, using=using
        )

    async def async_all(self):
        __deprecation_warning()
        return await sync_to_async(self.all, thread_sensitive=True)()

    async def async_filter(self, *args, **kwargs):
        __deprecation_warning()
        return await sync_to_async(self.filter, thread_sensitive=True)(*args, **kwargs)

    async def async_exclude(self, *args, **kwargs):
        __deprecation_warning()
        return await sync_to_async(self.exclude, thread_sensitive=True)(*args, **kwargs)

    async def async_complex_filter(self, filter_obj):
        __deprecation_warning()
        return await sync_to_async(self.complex_filter, thread_sensitive=True)(
            filter_obj
        )

    async def async_union(self, *other_qs, all=False):
        __deprecation_warning()
        return await sync_to_async(self.union, thread_sensitive=True)(
            *other_qs, all=all
        )

    async def async_intersection(self, *other_qs):
        __deprecation_warning()
        return await sync_to_async(self.intersection, thread_sensitive=True)(*other_qs)

    async def async_difference(self, *other_qs):
        __deprecation_warning()
        return await sync_to_async(self.difference, thread_sensitive=True)(*other_qs)

    async def async_select_for_update(self, nowait=False, skip_locked=False, of=()):
        __deprecation_warning()
        return await sync_to_async(self.select_for_update, thread_sensitive=True)(
            nowait=nowait, skip_locked=skip_locked, of=of
        )

    async def async_prefetch_related(self, *lookups):
        __deprecation_warning()
        return await sync_to_async(self.prefetch_related, thread_sensitive=True)(
            *lookups
        )

    async def async_annotate(self, *args, **kwargs):
        __deprecation_warning()
        return await sync_to_async(self.annotate, thread_sensitive=True)(
            *args, **kwargs
        )

    async def async_order_by(self, *field_names):
        __deprecation_warning()
        return await sync_to_async(self.order_by, thread_sensitive=True)(*field_names)

    async def async_distinct(self, *field_names):
        __deprecation_warning()
        return await sync_to_async(self.distinct, thread_sensitive=True)(*field_names)

    async def async_extra(
        self,
        select=None,
        where=None,
        params=None,
        tables=None,
        order_by=None,
        select_params=None,
    ):
        __deprecation_warning()
        return await sync_to_async(self.extra, thread_sensitive=True)(
            select, where, params, tables, order_by, select_params
        )

    async def async_reverse(self):
        __deprecation_warning()
        return await sync_to_async(self.reverse, thread_sensitive=True)()

    async def async_defer(self, *fields):
        __deprecation_warning()
        return await sync_to_async(self.defer, thread_sensitive=True)(*fields)

    async def async_only(self, *fields):
        __deprecation_warning()
        return await sync_to_async(self.only, thread_sensitive=True)(*fields)

    async def async_using(self, alias):
        __deprecation_warning()
        return await sync_to_async(self.using, thread_sensitive=True)(alias)

    async def async_resolve_expression(self, *args, **kwargs):
        __deprecation_warning()
        return await sync_to_async(self.resolve_expression, thread_sensitive=True)(
            *args, **kwargs
        )

    @property
    async def async_ordered(self):
        __deprecation_warning()

        def _ordered():
            return super(QuerySetAsync, self).ordered

        return await sync_to_async(_ordered, thread_sensitive=True)()

    ###############################
    ### END OF DEPRECATION ZONE ###
    ###############################
