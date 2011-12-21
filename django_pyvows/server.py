#!/usr/bin/python
# -*- coding: utf-8 -*-

# django-pyvows extensions
# https://github.com/rafaelcaricio/django-pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com


import sys
import urllib2
from threading import Thread, local, current_thread
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

from django.core.handlers.wsgi import WSGIHandler


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
            headers_set[:] = [status, response_headers]
            return write

        application_iter = app(environ, start_response)
        try:
            for data in application_iter:
                write(data)
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


class DjangoServer(HTTPServer, object):

    def __init__(self, host, port):
        HTTPServer.__init__(self, (host, int(port)), WSGIRequestHandler)
        self.app = WSGIHandler()

    def start(self, settings):
        self.server_activate()
        self.thr = Thread(target=self.make_response_thread, args=(getattr(settings, '__dict__', settings),))
        self.thr.daemon = True
        self.thr.start()

    def make_response_thread(self, settings):
        thread = current_thread()
        if not hasattr(thread, 'settings'):
            thread.settings = local()
            for key, value in settings.items():
                setattr(thread.settings, key, value)
        while True:
            self.handle_request()


