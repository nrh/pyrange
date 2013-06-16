# -*- coding: utf-8 -*-
import inspect
import os
import pypeg2
import pypeg2.xmlast
import sys
import yaml
from nose.tools import timed, raises, assert_equal


sys.path.append('..')
import pyrange.peg

PARSERS = ['Operator', 'Expando', 'StringPart', 'Part', 'String', 'Pattern',
           'Role', 'RangePart', 'RangeExpr']


def test_range():
    @timed(.1)
    @raises(SyntaxError)
    def do_test_raises(p, data):
        return do_test(p, data)

    @timed(.1)
    def do_test(p, data):
        pclass = getattr(pyrange.peg, p)
        r = pypeg2.parse(data['input'], pclass)
        for key in data:
            if key == 'input' or key == 'raises' or key == 'testname':
                continue
            if key == 'is':
                assert_equal(data[key], r)
            else:
                assert_equal(data[key], getattr(r, key))
        print "\n", pypeg2.xmlast.thing2xml(r, pretty=True)
        #ok_(r, data.result)
        return

    path = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))

    for p in PARSERS:
        datafile = os.sep.join((path, 'pegdata', p.lower() + '.yaml'))
        with open(datafile) as f:
            tdata = yaml.load_all(f)
            tnum = 0
            for t in tdata:
                tname = t['testname'] if 'testname' in t else t['input']
                if 'raises' in t:
                    do_test_raises.description = "nok_%s_%s\t'%s'\t" \
                        % (p.lower(), tnum, tname)
                    tnum += 1
                    yield do_test_raises, p, t
                else:
                    do_test.description = "ok_%s_%s\t'%s'\t" \
                        % (p.lower(), tnum, tname)
                    tnum += 1
                    yield do_test, p, t
