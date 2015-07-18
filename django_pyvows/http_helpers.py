#!/usr/bin/python
# -*- coding: utf-8 -*-


def get(*args, **kwargs):
    from django.test.client import Client
    client = Client()
    return client.get(*args, **kwargs)


def post(*args, **kwargs):
    from django.test.client import Client
    client = Client()
    return client.post(*args, **kwargs)
