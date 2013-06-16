# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
from pypeg2 import Symbol, Enum, List, K
from pypeg2 import attr, re, some, maybe_some, optional

Symbol.regex = re.compile(r'[\w\&\-]+')


class Operator(Symbol):
    grammar = Enum(K("&"), K("-"))


class Expando(List):
    grammar = '[', attr('begin', re.compile(r'\d+')), ['-', ':'], \
        attr('end', re.compile(r'\d+')), ']'


class StringPart(str):
    grammar = re.compile(r'[\-_a-z0-9\.]+')


class Part(List):
    grammar = [StringPart, Expando]


class String(List):
    grammar = some(Part)


class Pattern(str):
    grammar = re.compile(r'^\/.*\/$')


class Role(str):
    grammar = '@', attr('name', StringPart)


class RangePart(List):
    grammar = [Pattern, String, Role]


class RangeExpr(List):
    grammar = RangePart, maybe_some(',', optional(Operator), RangePart)
