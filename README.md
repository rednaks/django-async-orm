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
To be

example:

```python
class MyModel(models.Model):
    name = models.CharField(max_length=250)

```

you can use it as follow:

```python
async def get_model():
    return await  MyModel.objects.async_get(name="something")
```

you can also iterate over a query set with `async for`:

```python
async def all_models():
    all_result_set = await MyModel.objects.async_all()
    async for obj in all_result_set:
        print(obj)
```

Some wrappers are also available for template rendering, form validation and login/logout


#### Async login
```python
from django_async_orm.wrappers import async_login

async def my_async_view(request):
    await async_login(request)
    ...
```

#### Form validation
```python

from django_async_orm.wrappers import async_form_is_valid
async def a_view(request):
    form = MyForm(request.POST)
    is_valid_form = await async_form_is_valid(form)
    if is_valid_form:
        ...
    
```


# Django ORM support:

This is an on going projects, not all model methods are ported.

### Manager:

| methods                    | supported  | comments |
|----------------------------|------------|----------|
| `Model.objects.async_get`                | ✅ |  |
| `Model.objects.async_create`             | ✅ |  |
| `Model.objects.async_bulk_create`        | ✅ |  |
| `Model.objects.async_bulk_update`        | ✅ |  |
| `Model.objects.async_get_or_create`      | ✅ |  |
| `Model.objects.async_update_or_create`   | ✅ |  |
| `Model.objects.async_earliest`           | ✅ |  |
| `Model.objects.async_latest`             | ✅ |  |
| `Model.objects.async_first`              | ✅ |  |
| `Model.objects.async_last`               | ✅ |  |
| `Model.objects.async_in_bulk`            | ✅ |  |
| `Model.objects.async_delete`             | ✅ |  |
| `Model.objects.async_update`             | ✅ |  |
| `Model.objects.async_exists`             | ✅ |  |
| `Model.objects.async_explain`            | ✅ |  |
| `Model.objects.async_raw`                | ✅ |  |
| `Model.objects.async_all`                | ✅ |  |
| `Model.objects.async_filter`             | ✅ |  |
| `Model.objects.async_exclude`            | ✅ |  |
| `Model.objects.async_complex_filter`     | ✅ |  |
| `Model.objects.async_union`              | ✅ |  |
| `Model.objects.async_intersection`       | ✅ |  |
| `Model.objects.async_difference`         | ✅ |  |
| `Model.objects.async_select_for_update`  | ✅ |  |
| `Model.objects.async_prefetch_related`   | ✅ |  |
| `Model.objects.async_annotate`           | ✅ |  |
| `Model.objects.async_order_by`           | ✅ |  |
| `Model.objects.async_distinct`           | ✅ |  |
| `Model.objects.async_difference`         | ✅ |  |
| `Model.objects.async_extra`              | ✅ |  |
| `Model.objects.async_reverse`            | ✅ |  |
| `Model.objects.async_defer`              | ✅ |  |
| `Model.objects.async_only`               | ✅ |  |
| `Model.objects.async_using`              | ✅ |  |
| `Model.objects.async_resolve_expression` | ✅ |  |
| `Model.objects.async_ordered`            | ✅ |  |
| `__aiter__`                              | ✅ |  |
| `__repr__`                               | ✅ |  |
| `Model.objects.async_iterator            | ❌ |  |


### Model:

| methods                    | supported  | comments |
|----------------------------|------------|----------|
| `Model.async_save`                      | ❌ |  |
| `Model.async_update`                    | ❌ |  |
| `Model.async_delete`                    | ❌ |  |
| `...`                                   | ❌ |  |


### User Model / Manager
| methods                    | supported  | comments |
|----------------------------|------------|----------|
| `UserModel.is_authenticated`            | ✅ |  |
| `UserModel.is_super_user`               | ✅ |  |
| `UserModel.objects.async_create_user`   | ❌ |  |
| `...`                                   | ❌ |  |


### Foreign object lazy loading:
Not supported ❌


### Wrappers:
| methods                    | supported  | comments |
|----------------------------|------------|----------|
| `wrappers.async_render`            | ✅  |  |
| `wrappers.async_login`            | ✅  |  |
| `wrappers.async_logout`            | ✅  |  |



