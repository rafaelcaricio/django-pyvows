#!/usr/bin/python
# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

import os
import re
import urllib2

from pyvows import Vows
from django.http import HttpRequest

from django_pyvows.assertions import Url, Model, Template
from django_pyvows.server import DjangoServer


class DjangoContext(Vows.Context):

    @classmethod
    def start_environment(cls, settings_path):
        if not settings_path:
            raise RuntimeError('The settings_path argument is required.')
        os.environ['DJANGO_SETTINGS_MODULE'] = settings_path

    def __init__(self, parent):
        super(DjangoContext, self).__init__(parent)
        if parent:
            self.port = parent.port
            self.host = parent.host
        else:
            self.port = 3331
            self.host = '127.0.0.1'
        self.ignore('get_settings', 'template', 'request', 'model', 'url',
                'start_environment', 'port', 'host', 'get_url', 'get', 'post')

    def setup(self):
        DjangoContext.start_environment(self.get_settings())

    def get_settings(self):
        if 'DJANGO_SETTINGS_MODULE' in os.environ:
            return os.environ['DJANGO_SETTINGS_MODULE']
        else:
            return 'settings'

    def url(self, path):
        return Url(self, path)

    def template(self, template_name, context):
        return Template(template_name, context)

    def request(self, **kw):
        return HttpRequest(**kw)

    def model(self, model_class):
        return Model(self, model_class)

    def get(self, path):
        return urllib2.urlopen(self.get_url(path))

    def post(self, path, params):
        return urllib2.urlopen(self.get_url(path), data=params)

    def get_url(self, path):
        ctx = self.parent
        while ctx:
            if hasattr(ctx, 'get_url'):
                return ctx.get_url(path)
            ctx = ctx.parent
        return ""

class DjangoHTTPContext(DjangoContext):

    def start_server(self):
        self.server = DjangoServer(self.host, self.port)
        self.server.start()

    def __init__(self, parent):
        super(DjangoHTTPContext, self).__init__(parent)
        self.ignore('start_server', 'settings')

    def get_url(self, path):
        if re.match('^https?:\/\/', path):
            return path
        return 'http://%s:%d%s' % (self.host, self.port, path)

