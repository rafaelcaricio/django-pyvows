#!/usr/bin/python
# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

from django_pyvows.context import DjangoContext, DjangoHttpContext
from django_pyvows.assertions import *

@Vows.batch
class HttpContextVows(DjangoHttpContext):

    def _get_settings(self):
        return "sandbox.settings"

    def topic(self):
        self._start_server()
        return self._get("/")

    def the_return_code_should_be_200(self, topic):
        expect(topic.getcode()).to_equal(200)

    def should_return_the_success_response(self, topic):
        expect(topic.read()).to_equal("hello world")

