#!/usr/bin/python
# -*- coding: utf-8 -*-


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
