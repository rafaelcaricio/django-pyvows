#!/usr/bin/python
# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

from pyvows import Vows, expect

from test_config import ConfiguredVowsContext as DjangoContext


@Vows.batch
class DjangoHTTPTestClientCompatibilityVows(DjangoContext):

    class SimpleGet(DjangoContext):
        def topic(self):
            return self.get('/say/')

        def should_be_ok(self, topic):
            expect(topic.status_code).to_equal(200)

        def should_ask_for_my_name(self, topic):
            expect(topic).contains('What\'s your name?')

    class SimpleGetWithParams(DjangoContext):
        def topic(self):
            return self.get('/say/?name=Rafael')

        def should_say_hello_to_me(self, topic):
            expect(topic).contains('Hello, Rafael!')

    class SimplePost(DjangoContext):
        def topic(self):
            return self.post('/post_it/', {'value': 'posted!'})

        def should_be_posted(self, topic):
            expect(topic).contains('posted!')

        class PostFile(DjangoContext):
            def topic(self):
                return self.post('/post_file/', {'the_file': open(self.TEST_FILE_PATH)})

            def should_be_posted_to_the_server(self, topic):
                expect(topic).contains("the contents")

        class WhenNotFound(DjangoContext):
            def topic(self):
                return self.post('/post_/', {'the_file': open(self.TEST_FILE_PATH)})

            def should_be_404(self, topic):
                expect(topic.status_code).to_equal(404)
