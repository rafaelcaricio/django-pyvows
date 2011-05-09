#!/usr/bin/python
# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

from pyvows import Vows, expect

from django_pyvows.context import DjangoContext

class DjangoFailedContext(DjangoContext):
    pass

@Vows.batch
class ContextTest(Vows.Context):

    def topic(self):
        return DjangoFailedContext(self)

    def should_be_an_error(self, topic):
        expect(topic).to_be_an_error()

    def should_be_runtime_error(self, topic):
        expect(topic).to_be_an_error_like(RuntimeError)

    def should_have_nice_error_message(self, topic):
        expect(topic).to_have_an_error_message_of('The context DjangoFailedContext needs a _get_settings method that returns the DJANGO_SETTINGS_MODULE environment variable value.')
