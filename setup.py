#!/usr/bin/python
# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

import os
from setuptools import setup
from imp import load_source

version = load_source('version', os.path.join("django_pyvows", "version.py"))

setup(
    name = 'django-pyvows',
    version = '.'.join([str(item) for item in version.__version__]),
    description = "django-pyvows are pyvows extensions to django web framework.",
    long_description = """
django-pyvows are pyvows extensions to django web framework.
""",
    keywords = 'testing vows test tdd django web',
    author = u'Rafael Caricio',
    author_email = 'rafael@caricio.com',
    #Contributors
    #contributor = 'Bernardo Heynemann',
    #contributor_email = 'heynemann@gmail.com',
    url = 'https://github.com/rafaelcaricio/django-pyvows',
    license = 'MIT',
    classifiers = ['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Natural Language :: English',
                   'Operating System :: MacOS',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 2.6',
                   'Topic :: Software Development :: Testing'
    ],
    packages = ['django_pyvows', 'django_pyvows.assertions'],
    package_dir = {"django_pyvows": "django_pyvows"},

    install_requires=[
        "pyvows",
        "django"
    ],

)
