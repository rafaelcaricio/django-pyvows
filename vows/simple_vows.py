#!/usr/bin/python
# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

from pyvows import Vows, expect
from django_pyvows.context import DjangoContext, DjangoSubContext
import django_pyvows.assertions

from sandbox.main.views import home

@Vows.batch
class DefaultsVows(DjangoContext):

    def topic(self):
        return self._get_settings()

    def should_be_using_the_default_settings(self, topic):
        expect(topic).to_equal('settings')

