#!/usr/bin/python
# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

from os.path import abspath, join, dirname

from pyvows import Vows, expect
from django_pyvows import DjangoContext, Assertions

from sandbox.main.views import home

class UrlVows(DjangoContext):

    def settings_path(self):
        return abspath(join(dirname(__file__), 'sandbox', 'settings.py'))

    class Home(Vows.Context):

        def topic(self):
            return self._url('/')

        def should_have_home_url_mapped(self, topic):
            expect(topic).to_be_mapped()

        def should_have_url_mapped_to_home_view(self, topic):
            expect(topic).to_match_view(home)
