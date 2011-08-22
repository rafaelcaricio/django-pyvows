#!/usr/bin/python
# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

from pyvows import Vows, expect

from django_pyvows.context import DjangoContext, DjangoHTTPContext
#from django_pyvows.settings_manager import settings_tracker


@Vows.batch
class SettingsVows(DjangoContext):

    #class WhenIUseTheModulesTracker(DjangoContext):

        #def topic(self):
            #settings_tracker.install()
            #import to_test
            #return modules_tracker

        #def should_track_the_new_imported_module(self, topic):
            #expect('to_test' in topic.new_modules).to_be_true()

        #class WhenIReloadTheImportedModule(DjangoContext):

            #def topic(self, modules_tracker):
                #import to_test
                #imported_first_time_at = to_test.imported_at
                #modules_tracker.reload()
                #import to_test
                #return (modules_tracker, imported_first_time_at, to_test.imported_at)

            #def should_be_different_instances(self, topic):
                #expect(topic[1]).not_to_equal(topic[2])

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

