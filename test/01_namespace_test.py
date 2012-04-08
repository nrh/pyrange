#!/usr/bin/python
# -*- coding: utf-8 -*-

from wsgi_intercept.httplib2_intercept import install
install()
import bottle
import httplib2
import json
import pdb
from nose.tools import *
from pyrange.handler import pretty_print
import unittest
import wsgi_intercept

import pyrange.handler
import logging
FORMAT = \
    '%(asctime)s %(levelname)s %(filename)s:%(linenum)d %(funcName)s %message'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger('pyrange.tests')

addr = 'test'
port = 15232
http = httplib2.Http()
bottle.app.push(pyrange.handler.app)
url = 'http://%s:%d' % (addr, port)

bottle.debug(True)


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
    logger.info('r=%s' % r)
    logger.info('c=%s' % c)
    c = json.loads(c)
    if c.has_key('traceback'):
        logger.error(c['traceback'])
    assert_dict_contains_subset({'status': '201'}, r)


@with_setup(setup_stuff, teardown_stuff)
def test_get():
    (r, c) = http.request(url + '/namespaces', 'GET')
    logger.info('r=%s' % r)
    logger.info('c=%s' % c)
    c = json.loads(c)
    if c.has_key('traceback'):
        logger.error(c['traceback'])
    assert_dict_contains_subset({u'namespaces': ['testns']}, c)
    assert_dict_contains_subset({'status': '200'}, r)


@with_setup(setup_stuff, teardown_stuff)
def test_get_ns():
    (r, c) = http.request(url + '/namespaces/testns', 'GET')
    logger.info('r=%s' % r)
    logger.info('c=%s' % c)
    c = json.loads(c)
    if c.has_key('traceback'):
        logger.error(c['traceback'])
    testns = c['testns']
    assert_dict_contains_subset({'created_by': 'nrh'}, testns)
    assert_dict_contains_subset({'status': '200'}, r)


