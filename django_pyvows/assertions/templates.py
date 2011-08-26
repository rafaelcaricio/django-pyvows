#!/usr/bin/python
# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

from lxml.etree import fromstring
from lxml.cssselect import CSSSelector

from pyvows import Vows, expect
from django.template.loader import render_to_string


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

