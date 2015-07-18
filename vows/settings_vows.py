#!/usr/bin/python
# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

from pyvows import Vows, expect

from django_pyvows.context import DjangoContext

DjangoContext.start_environment("sandbox.sandbox.settings")


@Vows.batch
class SettingsOverridingVows(DjangoContext):

    class CannotSayHelloWithoutName(DjangoContext):

        def topic(self):
            with self.settings(SAY_HELLO_WITHOUT_NAME=False):
                return self.get('/say/')

        def should_be_ok(self, topic):
            expect(topic.status_code).to_equal(200)

        def should_ask_for_my_name(self, topic):
            expect(topic.content).to_equal("What's your name?")

    class SayHelloWithoutName(DjangoContext):

        def topic(self):
            with self.settings(SAY_HELLO_WITHOUT_NAME=True):
                return self.get('/say/')

        def should_be_ok(self, topic):
            expect(topic.status_code).to_equal(200)

        def should_(self, topic):
            expect(topic.content).to_equal("Hello, guess!")
