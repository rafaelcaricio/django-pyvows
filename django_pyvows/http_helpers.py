# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com


class HttpClientSupport(object):
    def __init__(self):
        self._client = None
        self.ignore('get', 'post')

    @property
    def client(self):
        if self._client is None:
            from django.test.client import Client  # Needs to be lazy loaded due settings config
            self._client = Client()
        return self._client

    def get(self, *args, **kwargs):
        return self.client.get(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.client.post(*args, **kwargs)
