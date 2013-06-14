# -*- coding: utf-8 -*-
import inspect
import os
import sys
import yaml


sys.path.append('..')
import pyrange.peg
from pyrange.parser import xmldump

PARSERS = ['Expando', 'StringPart', 'Part', 'Hostname', 'Operator', 'Pattern',
           'RangePart', 'Range']


def test_range():
    def do_test(p, data):
        pclass = getattr(pyrange.peg, p)
        r = pyrange.peg.parse(data['input'], pclass)
        print xmldump(r)
        #ok_(r, data.result)
        return

    path = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))

    for p in PARSERS:
        datafile = os.sep.join((path, 'data', p.lower() + '.yaml'))
        with open(datafile) as f:
            tdata = yaml.load_all(f)
            tnum = 0
            for t in tdata:
                if 'name' in t:
                    do_test.description = "test_%s_%s\t'%s'\t" \
                        % (p.lower(), tnum, t['name'])
                else:
                    do_test.description = "test_%s_%s\t'%s'\t" \
                        % (p.lower(), tnum, t['input'])

                tnum += 1
                yield do_test, p, t
