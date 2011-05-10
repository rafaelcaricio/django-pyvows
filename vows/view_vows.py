#!/usr/bin/python
# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

from pyvows import Vows, expect
from django_pyvows.context import DjangoContext, DjangoSubContext
from django.http import HttpResponse

from sandbox.main.views import home

@Vows.batch
class ViewVows(DjangoContext):

    def _get_settings(self):
        return 'sandbox.settings'

    class Home(DjangoSubContext):

        def topic(self):
            return home(self._request())

        def should_be_instance_of_http_response(self, topic):
            expect(topic).to_be_http_response()

        def should_be_hello_world(self, topic):
            expect(topic).to_have_contents_of('Hello World')
