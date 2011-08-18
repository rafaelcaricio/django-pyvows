#!/usr/bin/python
# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

import os

from pyvows import Vows

from django_pyvows.assertions import Url, Model, Template
from django.http import HttpRequest

class DjangoContext(Vows.Context):

    @classmethod
    def _start_environment(cls, settings_path):
        if not settings_path:
            raise RuntimeError('The settings_path argument is required.')
        os.environ['DJANGO_SETTINGS_MODULE'] = settings_path

    def __init__(self, parent):
        super(DjangoContext, self).__init__(parent)
        if not parent:
            DjangoContext._start_environment(self._get_settings())

    def _get_settings(self):
        if 'DJANGO_SETTINGS_MODULE' in os.environ:
            return os.environ['DJANGO_SETTINGS_MODULE']
        else:
            return 'settings'

    def _url(self, path):
        return Url(self, path)

    def _template(self, template_name, context):
        return Template(template_name, context)

    def _request(self, **kw):
        return HttpRequest(**kw)

    def _model(self, model_class):
        return Model(self, model_class)


import sys
import urllib2
from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
from threading import Thread

from django.core.handlers.wsgi import WSGIHandler

from django_pyvows import version

class WSGIRequestHandler(BaseHTTPRequestHandler):
    """A request handler that implements WSGI dispatching."""

    @property
    def server_version(self):
        return 'pyVowsServer'

    def make_environ(self):
        if '?' in self.path:
            path_info, query = self.path.split('?', 1)
        else:
            path_info = self.path
            query = ''

        environ = {
            'wsgi.version':         (1, 0),
            'wsgi.url_scheme':      'http',
            'wsgi.input':           self.rfile,
            'wsgi.errors':          sys.stderr,
            'wsgi.multithread':     False,
            'wsgi.multiprocess':    False,
            'wsgi.run_once':        False,
            'SERVER_SOFTWARE':      self.server_version,
            'REQUEST_METHOD':       self.command,
            'SCRIPT_NAME':          '',
            'PATH_INFO':            urllib2.unquote(path_info),
            'QUERY_STRING':         query,
            'CONTENT_TYPE':         self.headers.get('Content-Type', ''),
            'CONTENT_LENGTH':       self.headers.get('Content-Length', ''),
            'REMOTE_ADDR':          self.client_address[0],
            'REMOTE_PORT':          self.client_address[1],
            'SERVER_NAME':          self.server.server_address[0],
            'SERVER_PORT':          str(self.server.server_address[1]),
            'SERVER_PROTOCOL':      self.request_version
        }

        for key, value in self.headers.items():
            key = 'HTTP_' + key.upper().replace('-', '_')
            if key not in ('HTTP_CONTENT_TYPE', 'HTTP_CONTENT_LENGTH'):
                environ[key] = value

        return environ

    def run_wsgi(self):
        app = self.server.app
        environ = self.make_environ()
        headers_set = []
        headers_sent = []

        def write(data):
            assert headers_set, 'write() before start_response'
            if not headers_sent:
                status, response_headers = headers_sent[:] = headers_set
                code, msg = status.split(None, 1)
                self.send_response(int(code), msg)
                header_keys = set()
                for key, value in response_headers:
                    self.send_header(key, value)
                    key = key.lower()
                    header_keys.add(key)
                if 'content-length' not in header_keys:
                    self.close_connection = True
                    self.send_header('Connection', 'close')
                if 'server' not in header_keys:
                    self.send_header('Server', self.version_string())
                if 'date' not in header_keys:
                    self.send_header('Date', self.date_time_string())
                self.end_headers()

            assert type(data) is str, 'applications must write bytes'
            self.wfile.write(data)
            self.wfile.flush()

        def start_response(status, response_headers, exc_info=None):
            if exc_info:
                try:
                    if headers_sent:
                        raise exc_info[0], exc_info[1], exc_info[2]
                finally:
                    exc_info = None
            elif headers_set:
                raise AssertionError('Headers already set')
            headers_set[:] = [status, response_headers]
            return write

        application_iter = app(environ, start_response)
        try:
            for data in application_iter:
                write(data)
            # make sure the headers are sent
            if not headers_sent:
                write('')
        finally:
            if hasattr(application_iter, 'close'):
                application_iter.close()
            application_iter = None

    def handle_one_request(self):
        self.raw_requestline = self.rfile.readline()
        if self.parse_request():
            return self.run_wsgi()

    def log_request(self, code='-', size='-'):
        pass

    def log_error(self, *args):
        pass

    def log_message(self, format, *args):
        pass

class PyVowsDjangoServer(HTTPServer, object):

    def __init__(self, host, port, app):
        HTTPServer.__init__(self, (host, int(port)), WSGIRequestHandler)
        self.app = app

class DjangoHttpContext(DjangoContext):

    def _start_server(self):
        self.server = PyVowsDjangoServer(self._get_http_host(), self._get_http_port(), WSGIHandler())
        self.server.server_activate()

    def _get_http_port(self):
        return 8080

    def _get_http_host(self):
        return '127.0.0.1'

    def _get_url(self, path):
        return 'http://%s:%d%s' % (self._get_http_host(), self._get_http_port(), path)

    def _get(self, path):
        def make_response():
            self.server.handle_request()
        Thread(target=make_response).start()
        return urllib2.urlopen(self._get_url(path))

    def _post(self, url, params):
        pass
