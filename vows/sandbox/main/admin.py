#!/usr/bin/python
# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

from django.contrib import admin

from models import StringModel


class StringModelAdmin(admin.ModelAdmin):
    list_display = ('name', )

admin.site.register(StringModel, StringModelAdmin)
