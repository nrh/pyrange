#!/usr/bin/python
# -*- coding: utf-8 -*-

from gevent.wsgi import WSGIServer
from pyrange.request import RangeRequest
from pyrange.request_handler import RangeRequestHandler

class Server:

    '''Start a wsgi server, pass requests to RangeRequest for handling'''

    def __init__(self, addr, port, **kwargs):
        self.addr = addr
        self.port = port

    def rangeapp(self, env, start_resp):
        req = RangeRequest(env, start_resp)
        return RangeRequestHandler(req).handle_request()

    def start(self):
        WSGIServer((self.addr, self.port), self.rangeapp).serve_forever()

