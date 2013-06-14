# -*- coding: utf-8 -*-
import inspect
import os
import sys
import yaml
from nose.tools import timed, raises


sys.path.append('..')
import pyrange.peg
from pyrange.parser import xmldump

PARSERS = ['Expando', 'StringPart', 'Part', 'Hostname', 'Pattern', 'Role',
           'Operator', 'RangePart', 'Range']


def test_range():
    @timed(.1)
    @raises(SyntaxError)
    def do_test_raises(p, data):
        return do_test(p, data)

    @timed(.1)
    def do_test(p, data):
        pclass = getattr(pyrange.peg, p)
        r = pyrange.peg.parse(data['input'], pclass)
        print "\n", xmldump(r)
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
                tname = t['name'] if 'name' in t else t['input']
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
