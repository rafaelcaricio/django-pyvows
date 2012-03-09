#!/usr/bin/python
# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

from threading import current_thread

class SettingsTracker(object):

    def install(self):
        actual_import = __builtins__['__import__']
        if actual_import != self._import:
            self.real_import = actual_import
            __builtins__['__import__'] = self._import

    def _import(self, name, globals=None, locals=None, fromlist=[], level=-1):
        result = apply(self.real_import, (name, globals, locals, fromlist, level))
        fromlist = (fromlist or [])
        if name == 'django.conf' and 'settings' in fromlist:
            result.settings = VowsSettings(result.settings)
        elif name == 'django' and 'conf' in fromlist:
            result.conf.settings = VowsSettings(result.conf.settings)
        return result

class VowsSettings(object):

    def __init__(self, original_settings):
        self.original_settings = original_settings

    def __getattr__(self, attr_name):
        thread = current_thread()
        if hasattr(thread, 'settings'):
            if attr_name in thread.settings:
                return thread.settings[attr_name]
        return getattr(self.original_settings, attr_name)

settings_tracker = SettingsTracker()
