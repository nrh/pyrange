#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json
import random
import unittest
from nose.tools import with_setup

randport = random.randrange(1025, 65534)


class NamespaceTest(unittest.TestCase):
    def setup_stuff(self):
        '''set up test fixture'''


    def teardown_stuff(self):
        '''tear down test fixture'''


    @with_setup(setup_stuff, teardown_stuff)
    def test_put(self):
        namespace = {'name': 'testns', 'acls': []}
        url = 'http://localhost:%d/namespace/' % randport
        payload = json.dumps(namespace)
        r = requests.put(url, data=payload)


    @with_setup(setup_stuff, teardown_stuff)
    def test_get(self):
        r = requests.get('http://localhost:%d/namespace/')
        print r
        pass



