# -*- coding: utf-8 -*-

import pyrange.peg
import pyrange.range
import pypeg2.xmlast
import pypeg2


def expand_range(expr):
    r = pypeg2.parse(expr, pyrange.peg.RangeExpr)
    return r


def xmldump(x):
    return pypeg2.xmlast.thing2xml(x, pretty=True)
