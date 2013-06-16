# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from pypeg2 import Symbol, Enum, List, K
from pypeg2 import attr, re, some, maybe_some, optional

Symbol.regex = re.compile(r'[\w\&\-]+')


class Operator(Symbol):
    grammar = Enum(K("&"), K("-"))

    def _build(self, rr):
        rr._ops.append(self[0])
        rr._nextop = self[0]
        return


class Expando(List):
    grammar = '[', attr('begin', re.compile(r'\d+')), ['-', ':'], \
        attr('end', re.compile(r'\d+')), ']'

    def _build(self, rr):
        for e in self:
            rr._expandos.append(e)
        return


class StringPart(str):
    grammar = attr('part', re.compile(r'[\-_a-z0-9\.]+'))

    def _build(self, rr):
        rr._strings.append(self[0])
        return


class Part(List):
    grammar = [StringPart, Expando]

    def _build(self, rr):
        for o in self:
            o._build(rr)
        return


class String(List):
    grammar = some(Part)

    def _build(self, rr):
        for o in self:
            o._build(rr)
        return


class Pattern(str):
    grammar = re.compile(r'^\/.*\/$')

    def _build(self, rr):
        rr._patterns.append(self[0])
        return


class Role(str):
    grammar = '@', attr('name', StringPart)

    def _build(self, rr):
        rr._roles.append(self.name)
        return


class RangePart(List):
    grammar = [Pattern, String, Role]

    def _build(self, rr):
        # no data here, just iterate
        for o in self:
            o._build(rr)
        return


class RangeExpr(List):
    grammar = RangePart, maybe_some(',', optional(Operator), RangePart)

    def _build(self, rr):
        # no data here, just iterate
        for o in self:
            o._build(rr)
        return
