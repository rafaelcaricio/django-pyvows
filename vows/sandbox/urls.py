#!/usr/bin/python
# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'sandbox.main.views.home', name='home'),
    url(r'^say/$', 'sandbox.main.views.say_hello', name='say_hello'),
    url(r'^post_it/$', 'sandbox.main.views.post_it', name='post_it'),
    url(r'^settings/(?P<attr>[\w_]+)/?$', 'sandbox.main.views.get_setting', name='get_setting'),

    # url(r'^sandbox/', include('sandbox.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
