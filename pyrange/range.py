# -*- coding: utf-8 -*-

import pypeg2
import pyrange
import pyrange.peg
import logging


def resolve(e):
    rr = RangeResult(expr=e)
    logging.debug(e)
    rr.build()
    return rr


def expand_range(expr):
    r = pypeg2.parse(expr, pyrange.peg.RangeExpr)
    return r


def xmldump(x):
    return pypeg2.xmlast.thing2xml(x, pretty=True)


class RangeResult:
    def __init__(self, expr=None):
        if expr:
            self.expr = expr
            self._ast = pypeg2.parse(self.expr, pyrange.peg.RangeExpr)
            self._nextop = None
            self._expandos = []
            self._ops = []
            self._patterns = []
            self._roles = []
            self._strings = []

    def build(self):
        for o in self._ast:
            o._build(rr=self)
