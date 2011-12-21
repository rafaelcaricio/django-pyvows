#!/usr/bin/python
# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

import os
import re
from threading import local, current_thread

from pyvows import Vows
from django.http import HttpRequest

from django_pyvows import http_helpers
from django_pyvows.assertions import Url, Model, Template
from django_pyvows.server import DjangoServer
from django_pyvows.settings_manager import settings_tracker

DEFAULT_PORT = 3331
DEFAULT_HOST = '127.0.0.1'

class DjangoContext(Vows.Context):

    @classmethod
    def start_environment(cls, settings_path):
        if not settings_path:
            raise RuntimeError('The settings_path argument is required.')
        os.environ['DJANGO_SETTINGS_MODULE'] = settings_path
        settings_tracker.install()

    def __init__(self, parent):
        super(DjangoContext, self).__init__(parent)
        self.ignore('get_settings', 'template', 'request', 'model', 'url', 'find_in_parent',
                'start_environment', 'port', 'host', 'get_url', 'get', 'post')

    @property
    def settings(self):
        thread = current_thread()
        if not hasattr(thread, 'settings'):
            thread.settings = local()
        return thread.settings

    def setup(self):
        DjangoContext.start_environment(self.get_settings())

    def get_settings(self):
        return os.environ.get('DJANGO_SETTINGS_MODULE', 'settings')

    def url(self, path):
        return Url(self, path)

    def template(self, template_name, context):
        return Template(template_name, context)

    def request(self, **kw):
        return HttpRequest(**kw)

    def model(self, model_class):
        return Model(self, model_class)

    def get(self, path):
        return http_helpers.get(self.get_url(path))

    def post(self, path, params):
        return http_helpers.post(self.get_url(path), params)

    def find_in_parent(self, attr_name):
        ctx = self.parent
        while ctx:
            if hasattr(ctx, attr_name):
                return getattr(ctx, attr_name)
            ctx = ctx.parent
        raise ValueError('Host could not be found in the context or any of its parents')

    def get_url(self, path):
        try:
            return self.find_in_parent('get_url')(path)
        except ValueError:
            return path


class DjangoHTTPContext(DjangoContext):

    def start_server(self, host=None, port=None):
        if not port: port = DEFAULT_PORT
        if not host: host = DEFAULT_HOST

        self.address = (host, port)
        self.server = DjangoServer(host, port)
        self.server.start(self.settings)

    def __init__(self, parent):
        super(DjangoHTTPContext, self).__init__(parent)
        self.ignore('start_server', 'settings')

    @property
    def host(self):
        if hasattr(self, 'address'):
            return self.address[0]
        return self.find_in_parent('host')

    @property
    def port(self):
        if hasattr(self, 'address'):
            return self.address[1]
        return self.find_in_parent('port')

    def get_url(self, path):
        if re.match('^https?:\/\/', path):
            return path
        return 'http://%s:%d%s' % (self.host, self.port, path)

