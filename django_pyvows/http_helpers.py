#!/usr/bin/python
# -*- coding: utf-8 -*-


class RetrocompatibleResponse(object):
    def __init__(self, response):
        self.response = response

    @property
    def status(self):
        return self.response.status_code

    def __iter__(self):
        yield self
        yield self.response.content


def get(url):
    from django.test.client import Client
    client = Client()
    resp = client.get(url)
    return RetrocompatibleResponse(resp), resp.content


def post(url, data):
    from django.test.client import Client
    client = Client()
    return RetrocompatibleResponse(client.post(url, data))
