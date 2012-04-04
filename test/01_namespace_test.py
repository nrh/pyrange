#!/usr/bin/python
# -*- coding: utf-8 -*-

from wsgi_intercept.httplib2_intercept import install
install()
import bottle
import httplib2
import json
from nose.tools import *
import unittest
import wsgi_intercept

import pyrange.handler

addr = 'test'
port = 15232
http = httplib2.Http()
bottle.app.push(pyrange.handler.app)
url = 'http://%s:%d' % (addr, port)


def setup_stuff():
    '''set up test fixture'''

    wsgi_intercept.add_wsgi_intercept(addr, port, bottle.default_app)


def teardown_stuff():
    '''tear down test fixture'''

    wsgi_intercept.remove_wsgi_intercept(addr, port, bottle.default_app)


@with_setup(setup_stuff, teardown_stuff)
def test_put():
    namespace = {'name': 'testns', 'acls': []}
    payload = json.dumps(namespace)
    (r, c) = http.request(url + '/namespaces', 'PUT', body=payload)
    c = json.loads(c)
    assert_dict_contains_subset({u'message':u'created "testns"'}, c, c)
    assert_dict_contains_subset({'status': '201'}, r)


@with_setup(setup_stuff, teardown_stuff)
def test_get():
    (r, c) = http.request(url + '/namespaces', 'GET')
    c = json.loads(c)
    assert_dict_contains_subset({u'namespaces': ['testns']}, c)
    assert_dict_contains_subset({'status': '200'}, r)

