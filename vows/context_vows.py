#!/usr/bin/python
# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

from pyvows import Vows, expect

from django_pyvows.context import DjangoContext, DjangoHTTPContext

DjangoContext.start_environment("sandbox.settings")

@Vows.batch
class ContextTest(Vows.Context):

    def topic(self):
        return DjangoContext.start_environment(None)

    def should_be_an_error(self, topic):
        expect(topic).to_be_an_error()

    def should_be_runtime_error(self, topic):
        expect(topic).to_be_an_error_like(RuntimeError)

    def should_have_nice_error_message(self, topic):
        expect(topic).to_have_an_error_message_of('The settings_path argument is required.')

    class WithinANoDjangoContext(Vows.Context):

        class TheGetUrlMethod(DjangoContext):

            def topic(self):
                return self.get_url('/')

            def should_return_the_same_path(self, topic):
                expect(topic).to_equal('/')

        class TheHost(DjangoHTTPContext):

            def topic(self):
                return self.host

            def should_return_an_error(self, topic):
                expect(topic).to_be_an_error_like(ValueError)

        class ThePort(DjangoHTTPContext):

            def topic(self):
                return self.port

            def should_return_an_error(self, topic):
                expect(topic).to_be_an_error_like(ValueError)

    class WithinAServer(DjangoHTTPContext):

        def setup(self):
            self.start_server(port=8085)

        class WithinDjangoHTTPContextTheGetUrlMethod(DjangoHTTPContext):

            def topic(self):
                return self.get_url('http://127.0.0.1:8085/complete_url/')

            def when_passed_a_complete_url_should_return_the_url_without_modification(self, topic):
                expect(topic).to_equal('http://127.0.0.1:8085/complete_url/')

            class InADjangoHTTPContext(DjangoHTTPContext):

                def topic(self):
                    return self.get_url('/')

                def the_get_url_should_return_a_well_formed_url(self, topic):
                    expect(topic).to_equal('http://127.0.0.1:8085/')

        class ANoDjangoContext(Vows.Context):

            class TheHost(DjangoHTTPContext):

                def topic(self):
                    return self.host

                def should_be_equal_to_the_host_in_out_context(self, topic):
                    expect(topic).to_equal('127.0.0.1')

            class ThePort(DjangoHTTPContext):

                def topic(self):
                    return self.port

                def should_be_equal_to_the_port_in_out_context(self, topic):
                    expect(topic).to_equal(8085)

            class AnDjangoContext(DjangoContext):

                def topic(self):
                    return self.get_url('/')

                def the_get_url_method_should_return_a_well_formed_url(self, topic):
                    expect(topic).to_equal('http://127.0.0.1:8085/')

