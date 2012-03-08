#!/usr/bin/python
# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

from pyvows import Vows, expect


class Model(object):
    def __init__(self, context, model):
        from django.db import models

        self.context = context
        if isinstance(model, models.Model):
            model = model.__class__
        self.model = model

    def __call__(self, *args, **kwargs):
        return self.model(*args, **kwargs)

    @property
    def admin(self):
        from django.contrib import admin
        if self.model not in admin.site._registry:
            raise admin.sites.NotRegistered('The model %s is not registered' % self.model.__name__)
        return admin.site._registry[self.model]

@Vows.assertion
def to_be_in_admin(topic):
    from django.contrib import admin
    try:
        assert topic.admin
    except admin.sites.NotRegistered:
        assert False, "The model %s isn't registered in admin." % topic.model.__name__

@Vows.assertion
def to_have_field(topic, field_name, field_class=None, **kwargs):
    from django.db import models

    if isinstance(topic, Model):
        topic = topic.model

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
