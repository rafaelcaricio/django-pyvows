#!/usr/bin/python
# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

import os

from pyvows import Vows
from django_pyvows.assertions import Url
from django.http import HttpRequest

class DjangoContext(Vows.Context):

    def __init__(self, parent):
        super(DjangoContext, self).__init__(parent)
        if not hasattr(self, '_get_settings'):
            raise RuntimeError('The context %s needs a _get_settings method that returns the DJANGO_SETTINGS_MODULE environment variable value.' % self.__class__.__name__)
        os.environ['DJANGO_SETTINGS_MODULE'] = self._get_settings()

        #Gotta set settings environment variable first
        from django.test.utils import setup_test_environment #, teardown_test_environment

        setup_test_environment()

    def _url(self, path):
        return Url(self, path)

    def _request(self, **kw):
        return HttpRequest(**kw)

class DjangoSubContext(Vows.Context):

    def _url(self, path):
        return self.parent._url(path)

    def _request(self, **kw):
        return self.parent._request(**kw)

