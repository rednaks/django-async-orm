import asyncio

from django.test import TestCase
from django.conf import settings
from django.apps import apps
import time

from .models import TestModel


class ModelTestCase(TestCase):
    def __init__(self, *args, **kwargs):
        self._event_loop = asyncio.get_event_loop()

        super().__init__(*args, **kwargs)

    def setUp(self):
        async def _create_async():
            return await TestModel.objects.async_create(name="setup")
        self._event_loop.run_until_complete(_create_async())

    def tearDown(self):
        async def _delete_async():
            return await TestModel.objects.async_delete()
        self._event_loop.run_until_complete(_delete_async())


    def test_dao_loaded(self):
        self.assertTrue(apps.is_installed('django_async_orm'))


    def test_manager_is_async(self):
        manager_class_name = TestModel.objects.__class__.__name__
        self.assertTrue(
            manager_class_name.startswith('MixinAsync'),
            'Manager class name is %s but should start with "MixinAsync"' % (manager_class_name) )

    def test_create(self):
        async def _create_async():
            return await TestModel.objects.async_create(name="test")

        result = self._event_loop.run_until_complete(_create_async())
        print(result)
        self.assertEqual(result.name, 'test')

    def test_bulk_create(self):
        async def _async_bulk_create():
            return await TestModel.objects.async_bulk_create([
                TestModel(name='bulk create 1'),
                TestModel(name='bulk create 2'),
            ])

        objs = self._event_loop.run_until_complete(_async_bulk_create())
        self.assertEqual(len(objs), 2)

    def test_async_get(self):
        async def get_object():
            return await TestModel.objects.async_get(name="setup")

        result = self._event_loop.run_until_complete(get_object())
        self.assertEqual(result.name, "setup")

    def test_async_all(self):
        async def _get_all():
            return await TestModel.objects.async_all()


        async def _len(queryset):
            count = 0
            async for obj in queryset:
                count += 1
            return count

        result = self._event_loop.run_until_complete(_get_all())
        print(result)
        count = self._event_loop.run_until_complete(_len(result))
        self.assertEqual(count, 1)


    def test_async_first_in_all(self):
        async def _get_all():
            res = await TestModel.objects.async_all()
            print(res[0])
            return res

        async def _get_first(query_set):
            return await query_set.async_first()


        all_result = self._event_loop.run_until_complete(_get_all())
        print(all_result[0])
        first = self._event_loop.run_until_complete(_get_first(all_result))

        self.assertEqual(all_result[0].name, first.name)



