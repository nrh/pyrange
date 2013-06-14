# -*- coding: utf-8 -*- 

import pyrange.peg
import pypeg2.xmlast

def expand_range(expr):
    return pyrange.peg.parse(expr, pyrange.peg.Range)

def xmldump(x):
    return pypeg2.xmlast.thing2xml(x, pretty=True)
