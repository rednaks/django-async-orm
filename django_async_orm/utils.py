from django_async_orm.manager import AsyncManager


def mixin_async_manager_factory(model):
    """
    Creates a new type a mixin between the base manager and the async manager.

    :param model:  A django model class
    :type model:  models.Model
    :return: A mixin type
    :rtype: object
    """

    base_manager_cls = model.objects.__class__
    if not base_manager_cls.__name__.startswith('MixinAsync'):
        mixin_async_manager = type(f'MixinAsync{base_manager_cls.__name__}', (AsyncManager, base_manager_cls), dict())
        return mixin_async_manager


def patch_manager(model):
    """
    Patches django models to add async capabilities
    :param model: A django model class
    :type model: models.Model
    :return: None
    :rtype: None
    """
    async_manager_cls = mixin_async_manager_factory(model)
    if async_manager_cls:
        model.objects = async_manager_cls()
        model.objects.model = model
