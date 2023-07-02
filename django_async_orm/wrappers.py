from channels.db import database_sync_to_async as sync_to_async
from django.contrib.auth import login, logout


def _sync_render(*args, **kwargs):
    from django.shortcuts import render

    return render(*args, **kwargs)


arender = sync_to_async(_sync_render, thread_sensitive=True)


def _sync_login(*args, **kwargs):
    return login(*args, *kwargs)


alogin = sync_to_async(_sync_login, thread_sensitive=True)


def _sync_logout(request):
    return logout(request)


alogout = sync_to_async(_sync_logout, thread_sensitive=True)


def _sync_form_is_valid(form_instance):
    return form_instance.is_valid()


aform_is_valid = sync_to_async(_sync_form_is_valid, thread_sensitive=True)
