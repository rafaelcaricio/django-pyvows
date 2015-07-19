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

from django_pyvows.http_helpers import HttpClientSupport
from django_pyvows.settings_helpers import SettingsOverrideSupport


class DjangoContext(Vows.Context, HttpClientSupport, SettingsOverrideSupport):
    def __init__(self, parent):
        super(DjangoContext, self).__init__(parent)
        HttpClientSupport.__init__(self)
        SettingsOverrideSupport.__init__(self)
        self.ignore('start_environment', 'settings_module')

    def settings_module(self):
        return 'settings'

    @classmethod
    def start_environment(cls, settings_module):
        if not settings_module:
            raise ValueError('The settings_path argument is required.')

        os.environ.update({'DJANGO_SETTINGS_MODULE': settings_module})
        django.setup()

        from django.test.utils import setup_test_environment
        setup_test_environment()
