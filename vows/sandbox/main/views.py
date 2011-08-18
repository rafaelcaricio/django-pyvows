#!/usr/bin/python
# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

from django.http import HttpResponse

def home(request):
    return HttpResponse('hello world')

def say_hello(request):
    if not 'name' in request.GET:
        return HttpResponse("What's your name?")
    return HttpResponse("Hello, %s!" % request.GET['name'])
