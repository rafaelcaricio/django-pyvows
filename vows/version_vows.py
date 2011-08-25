#!/usr/bin/python
# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

from types import TupleType

from pyvows import Vows, expect


@Vows.batch
class VersionVows(Vows.Context):

    def topic(self):
        from django_pyvows.version import __version__
        return __version__

    def should_be_an_tuple(self, topic):
        expect(topic).to_be_instance_of(TupleType)
