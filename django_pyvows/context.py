#!/usr/bin/python
# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

import os

import django
from pyvows import Vows

from django_pyvows import http_helpers


class DjangoContext(Vows.Context):

    @classmethod
    def start_environment(cls, settings_path):
        if not settings_path:
            raise ValueError('The settings_path argument is required.')

        os.environ.update({'DJANGO_SETTINGS_MODULE': settings_path})
        django.setup()

        from django.test.utils import setup_test_environment
        setup_test_environment()

    def __init__(self, parent):
        super(DjangoContext, self).__init__(parent)
        self.ignore('start_environment', 'settings', 'get', 'post')

    def settings(self, **kwargs):
        from django.test.utils import override_settings
        return override_settings(**kwargs)

    def get(self, *args, **kwargs):
        return http_helpers.get(*args, **kwargs)

    def post(self, *args, **kwargs):
        return http_helpers.post(*args, **kwargs)
