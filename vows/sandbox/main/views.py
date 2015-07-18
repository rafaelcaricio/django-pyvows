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
    elif SAY_HELLO_WITHOUT_NAME:
        name = 'guest'
    else:
        return HttpResponse("What's your name?")
    return HttpResponse("Hello, %s!" % name)


def post_it(request):
    return HttpResponse(request.POST['value'])


def post_file(request):
    return HttpResponse(request.FILES['the_file'].read().strip())
