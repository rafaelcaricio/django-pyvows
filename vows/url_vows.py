#!/usr/bin/python
# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

from pyvows import expect

from django_pyvows.context import DjangoContext
from django_pyvows.assertions import *  # NOQA

DjangoContext.start_environment("sandbox.settings")

from sandbox.main.views import home  # NOQA


class UrlVows(DjangoContext):

    class Home(DjangoContext):

        def topic(self):
            return self.url('^$')

        def should_have_home_url_mapped(self, topic):
            expect(topic).to_be_mapped()

        def should_have_url_mapped_to_home_view(self, topic):
            expect(topic).to_match_view(home)
