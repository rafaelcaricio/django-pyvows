# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

from os.path import abspath, join, dirname

from django_pyvows.context import DjangoContext


class ConfiguredVowsContext(DjangoContext):
    def settings_module(self):
        return 'sandbox.sandbox.settings'

    def setup(self):
        self.TEST_FILE_PATH = abspath(join(dirname(__file__), 'fixtures/the_file.txt'))
