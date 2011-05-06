#!/usr/bin/python
# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com


from django.core.management.base import BaseCommand


class RunVowsCommand(BaseCommand):
    help = u'Run all vows for this project.'

    def handle(self, *args, **kwargs):
        pass
