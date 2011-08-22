#!/usr/bin/python
# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

from django.conf import settings
from django.http import HttpResponse


def home(request):
    return HttpResponse('hello world')

def say_hello(request):
    SAY_HELLO_WITHOUT_NAME = getattr(settings, "SAY_HELLO_WITHOUT_NAME", False)

    if 'name' in request.GET:
        name = request.GET['name']

    elif not SAY_HELLO_WITHOUT_NAME:
        return HttpResponse("What's your name?")

    elif SAY_HELLO_WITHOUT_NAME:
        name = 'guess'

    return HttpResponse("Hello, %s!" % name)

def get_setting(request, attr):
    return HttpResponse(str(getattr(settings, attr)))

