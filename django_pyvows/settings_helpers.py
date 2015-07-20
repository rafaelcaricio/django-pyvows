# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com


class SettingsOverrideSupport(object):
    def __init__(self):
        self.ignore('settings')

    def settings(self, **kwargs):
        from django.test.utils import override_settings
        return override_settings(**kwargs)
