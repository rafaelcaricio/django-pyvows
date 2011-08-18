#!/usr/bin/python
# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

import os
import sys
import urllib2
from threading import Thread
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

from pyvows import Vows
from django.http import HttpRequest
from django.core.handlers.wsgi import WSGIHandler

from django_pyvows.assertions import Url, Model, Template
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

    def log_request(self, *args, **kwargs):
        pass

    def log_error(self, *args):
        pass

    def log_message(self, *args):
        pass

class DjangoServer(HTTPServer, object):

    def __init__(self, host, port):
        HTTPServer.__init__(self, (host, int(port)), WSGIRequestHandler)
        self.app = WSGIHandler()


class DjangoContext(Vows.Context):

    @classmethod
    def start_environment(cls, settings_path):
        if not settings_path:
            raise RuntimeError('The settings_path argument is required.')
        os.environ['DJANGO_SETTINGS_MODULE'] = settings_path

    def __init__(self, parent):
        super(DjangoContext, self).__init__(parent)
        self.port = 8080
        self.host = '127.0.0.1'
        self.ignore('get_settings', 'template', 'request', 'model', 'url', 'start_environment', 'get', 'post')

    def setup(self):
        DjangoContext.start_environment(self.get_settings())

    def get_settings(self):
        if 'DJANGO_SETTINGS_MODULE' in os.environ:
            return os.environ['DJANGO_SETTINGS_MODULE']
        else:
            return 'settings'

    def url(self, path):
        return Url(self, path)

    def template(self, template_name, context):
        return Template(template_name, context)

    def request(self, **kw):
        return HttpRequest(**kw)

    def model(self, model_class):
        return Model(self, model_class)

    def get(self, path):
        return urllib2.urlopen(self.get_url(path))

    def post(self, path, params):
        return urllib2.urlopen(self.get_url(path), data=params)

    def get_url(self, path):
        ctx = self.parent
        while ctx:
            if hasattr(ctx, 'get_url'):
                return ctx.get_url(path)
            ctx = ctx.parent
        return ""

class DjangoHTTPContext(DjangoContext):

    def start_server(self):
        self.server = DjangoServer(self.host, self.port)
        self.server.server_activate()
        def make_response():
            while True:
                self.server.handle_request()
        self.thr = Thread(target=make_response)
        self.thr.daemon = True
        self.thr.start()

    def __init__(self, parent):
        super(DjangoHTTPContext, self).__init__(parent)
        self.port = 8080
        self.host = '127.0.0.1'
        self.ignore('start_server', 'port', 'host', 'get_url')

    def get_url(self, path):
        return 'http://%s:%d%s' % (self.host, self.port, path)
