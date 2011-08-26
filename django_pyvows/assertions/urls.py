#!/usr/bin/python
# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

from pyvows import Vows, expect
from django.http import HttpResponse


class Url(object):
    def __init__(self, context, path):
        self.context = context
        self.path = path

@Vows.assertion
def to_be_mapped(topic):
    verify_url_is_mapped_to_method(topic)

@Vows.assertion
def to_match_view(topic, view):
    verify_url_is_mapped_to_method(topic, view, True)

@Vows.assertion
def to_be_http_response(topic):
    expect(topic).to_be_instance_of(HttpResponse)

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
