#!/usr/bin/python
# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

from django_pyvows.context import DjangoContext, DjangoHTTPContext
from django_pyvows.assertions import *

@Vows.batch
class HttpContextVows(DjangoHTTPContext):

    def topic(self):
        self.start_server()
        return self.get("/")

    def the_return_code_should_be_200(self, topic):
        expect(topic.getcode()).to_equal(200)

    def should_return_the_success_response(self, topic):
        expect(topic.read()).to_equal("hello world")

    class Methods(DjangoContext):

        def topic(self):
            return self.get('/?name=rafael')

        def should_be_possible_to_pass_get_parameters(self, topic):
            expect(topic.getcode()).to_equal(200)

    class AskMyName(DjangoContext):

        def topic(self):
            return self.get('/say/')

        def should_ask_for_my_name(self, topic):
            expect(topic.read()).to_equal('What\'s your name?')

    class SayHelloToMe(DjangoContext):

        def topic(self):
            return self.get('/say/?name=Rafael')

        def should_say_hello_to_me(self, topic):
            expect(topic.read()).to_equal('Hello, Rafael!')

    class PostIt(DjangoContext):

        def topic(self):
            return self.post('/post_it/', {'value': 'posted!'})

        def should_be_posted(self, topic):
            expect(topic.read()).to_equal('posted!')

