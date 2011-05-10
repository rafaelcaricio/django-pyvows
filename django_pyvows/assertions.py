#!/usr/bin/python
# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

from lxml.cssselect import CSSSelector
from lxml.etree import fromstring

from django.template.loader import render_to_string

from pyvows import Vows

class Url(object):
    def __init__(self, context, path):
        self.context = context
        self.path = path

class Template(object):
    def __init__(self, template_name, context):
        self.template_name = template_name
        self.context = context
        self.doc = None

    def load(self):
        if not self.doc:
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
