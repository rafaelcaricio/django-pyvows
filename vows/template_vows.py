#!/usr/bin/python
# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

from pyvows import Vows, expect

from django_pyvows.context import DjangoContext
from django_pyvows.assertions import *

@Vows.batch
class TemplateVows(DjangoContext):

    def _get_settings(self):
        return 'sandbox.settings'

    class IndexTemplate(DjangoContext):

        def topic(self):
            return self.template('index.html', {
                'some': 'thing'
            })

        def should_have_container_div(self, topic):
            expect(topic).to_contain('div.container')

        def should_not_have_a_hello_div(self, topic):
            expect(topic).Not.to_contain('div.hello')

        def should_be_index_file(self, topic):
            expect(unicode(topic)).to_equal('index.html')

        class Paragraph(DjangoContext):

            def topic(self, template):
                return template.get_text('p.my-text')

            def should_have_paragraph_with_text(self, topic):
                expect(topic).to_be_like('some text')


