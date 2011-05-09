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
class UrlVows(DjangoContext):

    def _get_settings(self):
        return 'sandbox.settings'

    class Home(DjangoSubContext):

        def topic(self):
            return self._url('^$')

        def should_have_home_url_mapped(self, topic):
            expect(topic).to_be_mapped()

        def should_have_url_mapped_to_home_view(self, topic):
            expect(topic).to_match_view(home)
