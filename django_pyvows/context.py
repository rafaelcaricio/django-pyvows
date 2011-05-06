#!/usr/bin/python
# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

from pyvows import Vows

from django.test.utils import setup_test_environment, teardown_test_environment


class DjangoContext(Vows.Context):

    def _set_up_enviroment(self):
        setup_test_environment()

    def __call__(self):
        self._setup_enviroment()
