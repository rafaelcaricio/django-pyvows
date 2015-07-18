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
from django.http import HttpRequest

from django_pyvows import http_helpers
from django_pyvows.assertions import Url, Model, Template


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
        self.ignore('get_settings', 'template', 'request', 'model', 'url', 'find_in_parent',
                'start_environment', 'settings', 'modify_settings', 'get_url', 'get', 'post')

    def settings(self, **kwargs):
        from django.test.utils import override_settings
        return override_settings(**kwargs)

    def modify_settings(self, **kwargs):
        from django.test.utils import modify_settings
        return modify_settings(**kwargs)

    def url(self, path):
        return Url(self, path)

    def template(self, template_name, context):
        return Template(template_name, context)

    def request(self, **kw):
        return HttpRequest(**kw)

    def model(self, model_class):
        return Model(self, model_class)

    def get(self, path):
        return http_helpers.get(path)

    def post(self, path, params):
        return http_helpers.post(path, params)


class DjangoHTTPContext(DjangoContext):
    pass
