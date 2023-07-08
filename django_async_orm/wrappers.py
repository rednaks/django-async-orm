from channels.db import database_sync_to_async as sync_to_async
from django.contrib.auth import login, logout
from django.shortcuts import render


def _sync_form_is_valid(form_instance):
    return form_instance.is_valid()


arender = sync_to_async(render, thread_sensitive=True)
alogin = sync_to_async(login, thread_sensitive=True)
alogout = sync_to_async(logout, thread_sensitive=True)
aform_is_valid = sync_to_async(_sync_form_is_valid, thread_sensitive=True)
