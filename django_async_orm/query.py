import concurrent

from asgiref.sync import sync_to_async

# Create your models here.
from django.db.models import QuerySet

from django_async_orm.iter import AsyncIter

conf = {"thread_sensitive": True}
executor_ = concurrent.futures.ThreadPoolExecutor

try:
    from gevent.threadpool import ThreadPoolExecutor as GThreadPoolExecutor
    from django.conf import settings
    if settings.GEVENT_DJANGO_ASYNC_ORM:
        from gevent import monkey
        monkey.patch_all()
        def monkey_patch_the_monkey_patchers(ex):
            from .patch_gevent import _FutureProxy
            def submit(ex, fn, *args, **kwargs): # pylint:disable=arguments-differ
                with ex._shutdown_lock: # pylint:disable=not-context-manager
                    if ex._shutdown:
                        raise RuntimeError('cannot schedule new futures after shutdown')

                    future = ex._threadpool.spawn(fn, *args, **kwargs)
                    proxy_future = _FutureProxy(future)
                    print('yeah i see the _condition?', _FutureProxy, proxy_future._condition)
                    proxy_future.__class__ = concurrent.futures.Future
                    return proxy_future
            ex.submit = submit
            return ex
        MonkeyPoolExecutor = monkey_patch_the_monkey_patchers(GThreadPoolExecutor)
        conf = {"thread_sensitive": False, "executor": MonkeyPoolExecutor()}
        executor_ = MonkeyPoolExecutor
except Exception as e:
    print(e)
    print('defaulting django_async_orm')
    pass


class QuerySetAsync(QuerySet):

    def __init__(self, model=None, query=None, using=None, hints=None):
        super().__init__(model, query, using, hints)

    async def async_get(self, *args, **kwargs):
        return await sync_to_async(self.get, **conf)(*args, **kwargs)

    async def async_create(self, **kwargs):
        return await sync_to_async(self.create, **conf)(**kwargs)

    async def async_bulk_create(self, obs, batch_size=None, ignore_conflicts=False):
        return await sync_to_async(self.bulk_create, **conf)(obs, batch_size=batch_size,
                                                                            ignore_conflicts=ignore_conflicts)

    async def async_bulk_update(self, objs, fields, batch_size=None):
        return await sync_to_async(self.bulk_update, **conf)(objs=objs, fields=fields,
                                                                            batch_size=batch_size)

    async def async_get_or_create(self, defaults=None, **kwargs):
        return await sync_to_async(self.get_or_create, **conf)(defaults=defaults, **kwargs)

    async def async_update_or_create(self, defaults=None, **kwargs):
        return await sync_to_async(self.update_or_create, **conf)(defaults=defaults, **kwargs)

    async def async_earliest(self, *fields):
        return await sync_to_async(self.earliest, **conf)(*fields)

    async def async_latest(self, *fields):
        return await sync_to_async(self.latest, **conf)(*fields)

    async def async_first(self):
        return await sync_to_async(self.first, **conf)()

    async def async_last(self):
        return await sync_to_async(self.last, **conf)()

    async def async_in_bulk(self, id_list=None, *_, field_name='pk'):
        return await sync_to_async(self.in_bulk, **conf)(id_list=id_list, *_, field_name=field_name)

    async def async_delete(self):
        return await sync_to_async(self.delete, **conf)()

    async def async_update(self, **kwargs):
        return await sync_to_async(self.update, **conf)(**kwargs)

    async def async_exists(self):
        return await sync_to_async(self.exists, **conf)()

    async def async_explain(self, *_, format=None, **options):
        return await sync_to_async(self.explain, **conf)(*_, format=format, **options)

    async def async_raw(self, raw_query, params=None, translations=None, using=None):
        return await sync_to_async(self.raw, **conf)(raw_query, params=params, translations=translations,
                                                                    using=using)

    def __aiter__(self):
        with executor_(max_workers=1) as executor:
            f = executor.submit(self._fetch_all)
            f.result()

        return AsyncIter(self._result_cache)

    def __repr__(self):
        with executor_(max_workers=1) as executor:
            future_repr = executor.submit(super(QuerySetAsync, self).__repr__)

        return future_repr.result()

    ##################################################################
    # PUBLIC METHODS THAT ALTER ATTRIBUTES AND RETURN A NEW QUERYSET #
    ##################################################################

    async def async_all(self):
        return await sync_to_async(self.all, **conf)()

    async def async_filter(self, *args, **kwargs):
        return await sync_to_async(self.filter, **conf)(*args, **kwargs)

    async def async_exclude(self, *args, **kwargs):
        return await sync_to_async(self.exclude, **conf)(*args, **kwargs)

    async def async_complex_filter(self, filter_obj):
        return await sync_to_async(self.complex_filter, **conf)(filter_obj)

    async def async_union(self, *other_qs, all=False):
        return await sync_to_async(self.union, **conf)(*other_qs, all=all)

    async def async_intersection(self, *other_qs):
        return await sync_to_async(self.intersection, **conf)(*other_qs)

    async def async_difference(self, *other_qs):
        return await sync_to_async(self.difference, **conf)(*other_qs)

    async def async_select_for_update(self, nowait=False, skip_locked=False, of=()):
        return await sync_to_async(self.select_for_update, **conf)(nowait=nowait,
                                                                                  skip_locked=skip_locked, of=of)

    async def async_prefetch_related(self, *lookups):
        return await sync_to_async(self.prefetch_related, **conf)(*lookups)

    async def async_annotate(self, *args, **kwargs):
        return await sync_to_async(self.annotate, **conf)(*args, **kwargs)

    async def async_order_by(self, *field_names):
        return await sync_to_async(self.order_by, **conf)(*field_names)

    async def async_distinct(self, *field_names):
        return await sync_to_async(self.distinct, **conf)(*field_names)

    async def async_extra(self, select=None, where=None, params=None, tables=None, order_by=None, select_params=None):
        return await sync_to_async(self.extra, **conf)(select, where, params, tables, order_by,
                                                                      select_params)

    async def async_reverse(self):
        return await sync_to_async(self.reverse, **conf)()

    async def async_defer(self, *fields):
        return await sync_to_async(self.defer, **conf)(*fields)

    async def async_only(self, *fields):
        return await sync_to_async(self.only, **conf)(*fields)

    async def async_using(self, alias):
        return await sync_to_async(self.using, **conf)(alias)

    async def async_resolve_expression(self, *args, **kwargs):
        return await sync_to_async(self.resolve_expression, **conf)(*args, **kwargs)

    @property
    async def async_ordered(self):
        def _ordered():
            return super(QuerySetAsync, self).ordered
        return await sync_to_async(_ordered, **conf)()

