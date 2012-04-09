#!/usr/bin/python
# -*- coding: utf-8 -*-

from nose.tools import *
import logging
import pdb
import unittest
import yaml

from pyrange.range_parser import range_parser as rp

FORMAT = \
    '%(asctime)s %(levelname)s %(filename)s:%(linenum)d %(funcName)s %message'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger(__name__)

def test_range():
    with open('test/10_range_parser_test.data') as f:
        foo = yaml.load_all(f)
        i = 0
        for test in foo:
            logger.debug('test=%s' % test)
            result = foo.next()
            if not result:
                assert_items_equal(result, rp(test), test)
            else:
                assert_is_none(rp(test), test)



