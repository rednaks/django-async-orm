#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.db import models


class TestModel(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    obj_type = models.CharField(max_length=50, null=True, blank=True)
