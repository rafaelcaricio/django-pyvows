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
        self.context = context
        self.model = model

@Vows.assertion
def to_be_cruddable(topic):
    import django.db.models.fields as fields
    instance = __create_instance(topic)

    assert instance, "An instance could not be created for model %s" % topic.model.__name__

    retrieved = topic.model.objects.get(id=instance.id)
    assert retrieved.id == instance.id, "An instance could not be retrieved for model %s with id %d" % (topic.model.__name__, instance.id)

    updated = __update_instance(topic, retrieved)

    for field, value in topic.model._meta._field_cache:
        if field.__class__ == fields.AutoField:
            continue

        assert getattr(updated, field.name) != getattr(instance, field.name), "The instance should have been updated but the field %s is the same in both the original instance and the updated one (%s)." % (field.name, getattr(updated, field.name))

    topic.model.objects.delete(id=instance.id)
    object_count = topic.mode.objects.count()
    assert object_count == 0, "Object should have been deleted, but it wasn't (count: %d)" % object_count

def __create_instance(topic):
    import django.db.models.fields as fields
    arguments = {}
    for field, value in topic.model._meta._field_cache:
        if field.__class__ == fields.AutoField:
            continue

        if field.__class__ == fields.CharField:
            __add_char_value_for(field, None, arguments)

    return topic.model.objects.create(**arguments)

def __update_instance(topic, instance):
    import django.db.models.fields as fields
    arguments = {}
    for field, value in topic.model._meta._field_cache:
        if field.__class__ == fields.AutoField:
            continue

        if field.__class__ == fields.CharField:
            __add_char_value_for(field, instance, arguments)

    for key, value in arguments.iteritems():
        setattr(instance, key, value)

    instance.save()
    return instance

def __add_char_value_for(field, instance, arguments):
    value = "monty python"
    if instance:
        value = getattr(instance, field.name) + '2'
    if field.max_length:
        if instance:
            value = value[:len(value) - 2] + '2'
        value = (value * field.max_length)[:field.max_length]
    arguments[field.name] = value
