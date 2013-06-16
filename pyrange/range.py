# -*- coding: utf-8 -*-

from pypeg2 import List, parse
import pyrange


class Range:
    def __init__(self, expr=None):
        if expr:
            self.expr = expr
            self._ast = parse(self.expr, pyrange.peg.RangeExpr)
            self._data = self._rresolve(self._ast, 0)

    def _rresolve(self, ast, depth=0):
        '''
        recursively process AST into data
        '''

        if isinstance(ast, List):
            for x in ast:
                self._data.append(self._resolve_RangeExpr(x))
        elif isinstance(ast, pyrange.peg.RangePart):
            self._data.append(self._resolve_RangePart(x))
        elif isinstance(ast, pyrange.peg.Role):
            self._data.append(self._resolve_Role(x))
