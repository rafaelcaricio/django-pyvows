# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

from pyvows import Vows, expect

from test_config import ConfiguredVowsContext as DjangoContext


@Vows.batch
class DjangoAssertionsVows(DjangoContext):

    class RedirectsTo(DjangoContext):
        def topic(self):
            return self.get("/say")

        def should_redirect(self, topic):
            expect(topic).redirects_to('/say/', status_code=301)

    class Contains(DjangoContext):
        def topic(self):
            return self.get('/say/')

        def should_work(self, topic):
            expect(topic).contains('name')

    class WithFormError(DjangoContext):
        def topic(self):
            return self.post('/post-name/', {'another_field': 'filled'})

        def should_work(self, topic):
            expect(topic).with_form_error('form', 'your_name', 'This field is required.')
