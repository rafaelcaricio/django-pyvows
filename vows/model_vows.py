#!/usr/bin/python
# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

from pyvows import Vows, expect
from django_pyvows.context import DjangoContext

DjangoContext.start_environment("sandbox.settings")

from django.db import models
from sandbox.main.models import StringModel

@Vows.batch
class ModelVows(DjangoContext):

    class MainModel(DjangoContext):

        def topic(self):
            return self.model(StringModel)

        def should_be_cruddable_when_model_only_has_a_string(self, topic):
            expect(topic).to_be_cruddable()

        def should_be_cruddable_when_string_passed(self, topic):
            expect(topic).to_be_cruddable({
                'name': 'something'
            })

        def should_be_possible_to_use_the_assertion_in_model_instance(self, topic):
            expect(topic).to_have_field('name')

        def should_have_a_method_to_call(self, topic):
            expect(hasattr(topic, '__call__')).to_be_true()

        class WhenICreateANewInstance(DjangoContext):

            def topic(self, model):
                return model()

            def should_be_an_instance_of_django_model_class(self, topic):
                expect(isinstance(topic, models.Model)).to_be_true()

            def should_have_a_name_field(self, topic):
                expect(topic).to_have_field('name')

            def should_have_a_name_field_as_charfield(self, topic):
                expect(topic).to_have_field('name', models.CharField)

            def should_have_a_name_field_as_charfield_and_max_length_100(self, topic):
                expect(topic).to_have_field('name', models.CharField, max_length=100)

        class AdminModel(DjangoContext):

            def should_be_registred_in_admin(self, topic):
                expect(topic).to_be_in_admin()

            class StringModelInAdminOptions(DjangoContext):

                def topic(self, model):
                    return model.admin

                def should_be_listed_by_name(self, topic):
                    expect('name' in topic.list_display).to_be_true()

