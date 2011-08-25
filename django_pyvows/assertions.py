#!/usr/bin/python
# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

from pyvows import Vows, expect

from lxml.cssselect import CSSSelector
from lxml.etree import fromstring

from django.http import HttpResponse
from django.template.loader import render_to_string


class Url(object):
    def __init__(self, context, path):
        self.context = context
        self.path = path

class Model(object):
    def __init__(self, context, model):
        self.context = context
        self.model = model

    def __call__(self, *args, **kwargs):
        return self.model(*args, **kwargs)

class Template(object):
    def __init__(self, template_name, context):
        self.template_name = template_name
        self.context = context
        self.doc = None

    def load(self):
        if self.doc is None:
            self.doc = fromstring(render_to_string(self.template_name, self.context))
        return self.doc

    def select_element(self, selector):
        sel = CSSSelector(selector)
        return sel(self.load())

    def _to_contain(self, selector):
        return len(self.select_element(selector)) > 0

    def get_text(self, selector):
        return "".join((c.text for c in self.select_element(selector)))

    def __unicode__(self):
        return self.template_name

@Vows.assertion
def to_be_mapped(topic):
    verify_url_is_mapped_to_method(topic)

@Vows.assertion
def to_match_view(topic, view):
    verify_url_is_mapped_to_method(topic, view, True)

def verify_url_is_mapped_to_method(topic, method=None, assert_method_as_well=False):
    assert isinstance(topic, Url), "Only django_pyvows.Url items can be verified for mapping"

    from django.conf import settings
    project_urls = settings.ROOT_URLCONF

    urlpatterns = __import__(project_urls).urls.urlpatterns

    found = False
    matches_method = False
    for urlpattern in urlpatterns:
        regex = urlpattern.regex
        pattern = regex.pattern 
        actual_method = urlpattern.callback

        if topic.path == pattern:
            found = True
        if method == actual_method:
            matches_method = True

    assert found, "Expected url(%s) to be mapped but it wasn't"
    if assert_method_as_well:
        assert matches_method, "Expected url(%s) to match method(%s), but it didn't"

@Vows.assertion
def to_be_http_response(topic):
    expect(topic).to_be_instance_of(HttpResponse)

@Vows.assertion
def to_have_contents_of(topic, expected):
    expect(topic.content).to_be_like(expected)

@Vows.assertion
def to_contain(topic, selector):
    assert isinstance(topic, Template), "Only django_pyvows.Template items can be verified for mapping"
    assert topic._to_contain(selector), "Expected template(%s) to have an element(%s), but it don't have" % \
            (unicode(topic), selector)

@Vows.assertion
def not_to_contain(topic, selector):
    assert isinstance(topic, Template), "Only django_pyvows.Template items can be verified for mapping"
    assert not topic._to_contain(selector), "Expected template(%s) to not have an element(%s), but it have" % \
            (unicode(topic), selector)

@Vows.assertion
def to_have_field(topic, field_name, field_class=None, **kwargs):
    from django.db import models

    if isinstance(topic, models.Model):
        topic = topic.__class__

    if not field_class:
        field_class = models.Field

    field = topic._meta.get_field(field_name)
    assert isinstance(field, field_class), "The '%s.%s' is not an instance of '%s'" % (topic.__name__, field_name, field_class.__name__)
    if kwargs:
        for attr, value in kwargs.items():
            field_value = getattr(field, attr)
            assert field_value == value, "The field option '%s' should be equal to '%s', but it's equal to '%s'" % (attr, value, field_value)

@Vows.assertion
def to_be_cruddable(topic, defaults={}):
    import django.db.models.fields as fields
    instance = __create_or_update_instance(topic, None, defaults)

    assert instance, "An instance could not be created for model %s" % topic.model.__name__

    retrieved = topic.model.objects.get(id=instance.id)
    assert retrieved.id == instance.id, "An instance could not be retrieved for model %s with id %d" % (topic.model.__name__, instance.id)

    for key, value in defaults.iteritems():
        assert value == getattr(retrieved, key), "The default specified value of '%s' should have been set in the '%s' property of the instance but it was not" % (value, key)

    updated = __create_or_update_instance(topic, retrieved, defaults)

    for field, value in topic.model._meta._field_cache:
        if field.__class__ == fields.AutoField:
            continue

        if field.name in defaults:
            continue

        assert getattr(updated, field.name) != getattr(instance, field.name), "The instance should have been updated but the field %s is the same in both the original instance and the updated one (%s)." % (field.name, getattr(updated, field.name))

    instance.delete()
    object_count = topic.model.objects.count()
    assert object_count == 0, "Object should have been deleted, but it wasn't (count: %d)" % object_count

def __create_or_update_instance(topic, instance, defaults):
    import django.db.models.fields as fields
    arguments = {}
    for field, value in topic.model._meta._field_cache:
        if field.__class__ == fields.AutoField:
            continue

        if field.name in defaults:
            arguments[field.name] = defaults[field.name]
            continue

        if field.__class__ == fields.CharField:
            __add_char_value_for(field, instance, arguments)

    if instance:
        for key, value in arguments.iteritems():
            setattr(instance, key, value)

        instance.save()
        return instance

    return topic.model.objects.create(**arguments)

def __add_char_value_for(field, instance, arguments):
    value = "monty python"
    if instance:
        value = getattr(instance, field.name) + '2'
    if field.max_length:
        if instance:
            value = value[:len(value) - 2] + '2'
        value = (value * field.max_length)[:field.max_length]
    arguments[field.name] = value
