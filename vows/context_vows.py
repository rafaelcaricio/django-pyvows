#!/usr/bin/python
# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

from pyvows import Vows, expect
from pyvows.decorators import capture_error

from django_pyvows.context import DjangoContext


@Vows.batch
class ContextTest(Vows.Context):

    @capture_error
    def topic(self):
        return DjangoContext.setup_environment(None)

    def should_be_an_error(self, topic):
        expect(topic).to_be_an_error()

    def should_be_runtime_error(self, topic):
        expect(topic).to_be_an_error_like(ValueError)

    def should_have_nice_error_message(self, topic):
        expect(topic).to_have_an_error_message_of('The settings_path argument is required.')
