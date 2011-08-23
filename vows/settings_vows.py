#!/usr/bin/python
# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

from pyvows import Vows, expect

from django_pyvows.context import DjangoContext, DjangoHTTPContext
from django_pyvows.settings_manager import settings_tracker, VowsSettings


@Vows.batch
class SettingsVows(DjangoContext):

    class WhenIUseTheSettingsTracker(DjangoContext):

        def topic(self):
            settings_tracker.install()

        class WhenImportFromDjangoConf(DjangoContext):

            def topic(self):
                from django.conf import settings
                return settings

            def should_be_the_vows_settings(self, topic):
                expect(topic).to_be_instance_of(VowsSettings)

        class WhenIImportOnlyConfAndThenUseSettings(DjangoContext):

            def topic(self):
                from django import conf
                return conf.settings

            def should_be_the_vows_settings(self, topic):
                expect(topic).to_be_instance_of(VowsSettings)

        class WhenIImportTheCompletePathAndThenUseSettings(DjangoContext):

            def topic(self):
                import django.conf
                return django.conf.settings

            def should_be_the_vows_settings(self, topic):
                expect(topic).to_be_instance_of(VowsSettings)

    class CannotSayHelloWithoutName(DjangoHTTPContext):

        def topic(self):
            self.settings['SAY_HELLO_WITHOUT_NAME'] = False
            self.start_server(port=8002)
            return self.get('/say/')

        def should_be_ok(self, topic):
            expect(topic.code).to_equal(200)

        def should_ask_for_my_name(self, topic):
            expect(topic.read()).to_equal("What's your name?")

    class SayHelloWithoutName(DjangoHTTPContext):

        def topic(self):
            self.settings['SAY_HELLO_WITHOUT_NAME'] = True
            self.start_server(port=8003)
            return self.get('/say/')

        def should_be_ok(self, topic):
            expect(topic.code).to_equal(200)

        def should_(self, topic):
            expect(topic.read()).to_equal("Hello, guess!")

