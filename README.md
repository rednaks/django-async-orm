[![Downloads](https://static.pepy.tech/badge/django-async-orm)](https://pepy.tech/project/django-async-orm)

## Disclaimer: Don't use this module in production it's still in active development.

# Django Async Orm

Django module that brings async to django ORM.

# Installing

```
python -m pip install django-async-orm
```

then add `django_async_orm` to your `INSTALLED_APPS` list:

```python
INSTALLED_APPS = [
    ...,
    'django_async_orm'
]
```

# Usage

Django Async Orm will patch all your existing models to add `async_*` prefixed methods.

_note:_ Only non-existing methods will be patched.

example:

```python
class MyModel(models.Model):
    name = models.CharField(max_length=250)

```

you can use it as follow:

```python
async def get_model():
    return await  MyModel.objects.aget(name="something")
```

you can also iterate over a query set with `async for`:

```python
async def all_models():
    all_result_set = await MyModel.objects.aall()
    async for obj in all_result_set:
        print(obj)
```

Some wrappers are also available for template rendering, form validation and login/logout

#### Async login

```python
from django_async_orm.wrappers import alogin

async def my_async_view(request):
    await alogin(request)
    ...
```

#### Form validation

```python

from django_async_orm.wrappers import aform_is_valid
async def a_view(request):
    form = MyForm(request.POST)
    is_valid_form = await aform_is_valid(form)
    if is_valid_form:
        ...

```

# Django ORM support:

This is an on going projects, not all model methods are ported.

### Manager:

| methods                             | supported | comments |
| ----------------------------------- | --------- | -------- |
| `Model.objects.aget`                | ✅        |          |
| `Model.objects.acreate`             | ✅        |          |
| `Model.objects.acount`              | ✅        |          |
| `Model.objects.anone`               | ✅        |          |
| `Model.objects.abulk_create`        | ✅        |          |
| `Model.objects.abulk_update`        | ✅        |          |
| `Model.objects.aget_or_create`      | ✅        |          |
| `Model.objects.aupdate_or_create`   | ✅        |          |
| `Model.objects.aearliest`           | ✅        |          |
| `Model.objects.alatest`             | ✅        |          |
| `Model.objects.afirst`              | ✅        |          |
| `Model.objects.alast`               | ✅        |          |
| `Model.objects.ain_bulk`            | ✅        |          |
| `Model.objects.adelete`             | ✅        |          |
| `Model.objects.aupdate`             | ✅        |          |
| `Model.objects.aexists`             | ✅        |          |
| `Model.objects.aexplain`            | ✅        |          |
| `Model.objects.araw`                | ✅        |          |
| `Model.objects.aall`                | ✅        |          |
| `Model.objects.afilter`             | ✅        |          |
| `Model.objects.aexclude`            | ✅        |          |
| `Model.objects.acomplex_filter`     | ✅        |          |
| `Model.objects.aunion`              | ✅        |          |
| `Model.objects.aintersection`       | ✅        |          |
| `Model.objects.adifference`         | ✅        |          |
| `Model.objects.aselect_for_update`  | ✅        |          |
| `Model.objects.aprefetch_related`   | ✅        |          |
| `Model.objects.aannotate`           | ✅        |          |
| `Model.objects.aorder_by`           | ✅        |          |
| `Model.objects.adistinct`           | ✅        |          |
| `Model.objects.adifference`         | ✅        |          |
| `Model.objects.aextra`              | ✅        |          |
| `Model.objects.areverse`            | ✅        |          |
| `Model.objects.adefer`              | ✅        |          |
| `Model.objects.aonly`               | ✅        |          |
| `Model.objects.ausing`              | ✅        |          |
| `Model.objects.aresolve_expression` | ✅        |          |
| `Model.objects.aordered`            | ✅        |          |
| `__aiter__`                         | ✅        |          |
| `__repr__`                          | ✅        |          |
| `__len__`                           | ✅        |          |
| `__getitem__`                       | ✅        |          |
| `Model.objects.aiterator`           | ❌        |          |

### RawQuerySet

Not supported ❌

You can still call `Model.object.araw()` but you will be unable to access the results.

### Model:

| methods         | supported | comments |
| --------------- | --------- | -------- |
| `Model.asave`   | ❌        |          |
| `Model.aupdate` | ❌        |          |
| `Model.adelete` | ❌        |          |
| `...`           | ❌        |          |

### User Model / Manager

| methods                     | supported | comments |
| --------------------------- | --------- | -------- |
| `User.is_authenticated`     | ✅        |          |
| `User.is_super_user`        | ✅        |          |
| `User.objects.acreate_user` | ❌        |          |
| `...`                       | ❌        |          |

### Foreign object lazy loading:

Not supported ❌

### Wrappers:

| methods   | supported | comments |
| --------- | --------- | -------- |
| `arender` | ✅        |          |
| `alogin`  | ✅        |          |
| `alogout` | ✅        |          |
