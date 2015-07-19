# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

from django.test import SimpleTestCase
from pyvows import Vows


class _Dummy(SimpleTestCase):
    def nop():
        pass

dummy_testcase = _Dummy('nop')


@Vows.assertion
def redirects_to(*args, **kwargs):
    return dummy_testcase.assertRedirects(*args, **kwargs)


@Vows.assertion
def contains(*args, **kwargs):
    return dummy_testcase.assertContains(*args, **kwargs)


@Vows.assertion
def with_form_error(*args, **kwargs):
    return dummy_testcase.assertFormError(*args, **kwargs)
