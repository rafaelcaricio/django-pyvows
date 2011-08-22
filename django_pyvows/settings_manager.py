#!/usr/bin/python
# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

import sys

class ModulesTracker(object):

    def install(self):
        self.previous_modules = sys.modules.copy()
        self.real_import = __builtins__['__import__']
        __builtins__['__import__'] = self._import
        self.new_modules = {}

    def _import(self, name, globals=None, locals=None, fromlist=[], level=-1):
        result = apply(self.real_import, (name, globals, locals, fromlist, level))
        self.new_modules[name] = 1
        return result

    def reload(self):
        for modname in self.new_modules.keys():
            if not self.previous_modules.has_key(modname):
                del(sys.modules[modname])

    def uninstall(self):
        __builtins__['__import__'] = self.real_import

