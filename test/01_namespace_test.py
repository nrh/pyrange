#!/usr/bin/python
# -*- coding: utf-8 -*-

from wsgi_intercept.httplib2_intercept import install
install()
import bottle
import httplib2
import json
from nose.tools import with_setup
import unittest
import wsgi_intercept

import pyrange.handler

addr = 'test'
port = 15232
http = httplib2.Http()
bottle.app.push(pyrange.handler.app)

def setup_stuff():
    '''set up test fixture'''
    wsgi_intercept.add_wsgi_intercept(addr, port, bottle.default_app)

def teardown_stuff():
    '''tear down test fixture'''
    wsgi_intercept.remove_wsgi_intercept(addr, port, bottle.default_app)


@with_setup(setup_stuff, teardown_stuff)
def test_put():
    namespace = {'name': 'testns', 'acls': []}
    url = 'http://%s:%d/namespaces' % (addr, port)
    payload = json.dumps(namespace)
    (r, c) = http.request(url, 'PUT', body=payload)
    print r


@with_setup(setup_stuff, teardown_stuff)
def test_get():
    url = 'http://%s:%d/namespaces' % (addr, port)
    (r, c) = http.request(url, 'GET')
    print r

