#!/usr/bin/python
# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

from threading import Thread, current_thread, local
from time import sleep

from cherrypy import wsgiserver

from django.core.handlers.wsgi import WSGIHandler


def make_response_thread(thread, settings):
    if not hasattr(thread, 'settings'):
        thread.settings = settings

def run_app(host, port):
    server = wsgiserver.CherryPyWSGIServer(
        (host, port),
        WSGIHandler(),
        server_name='tornado-pyvows',
        numthreads = 1
    )

    my_thread = current_thread()
    my_thread.server = server

    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()

class DjangoServer(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self, settings):
        self.thr = Thread(target=run_app, args=(self.host, self.port))
        self.thr.daemon = True
        self.thr.start()

        while not len(self.thr.server.requests._threads):
            sleep(0.1)

        for _thread in self.thr.server.requests._threads:
            _thread.settings = hasattr(_thread, 'settings') and _thread.settings or local()
            for k, v in settings.iteritems():
                setattr(_thread.settings, k, v)



