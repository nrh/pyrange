# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
from pypeg2 import *  # NOQA

# foo[1-10].bar.com
# [1-10]foo.bar.com
# foo[1-10]bar.baz.com


Symbol.regex = re.compile(r'[\w\&\-]+')


class Operator(Symbol):
    grammar = Enum(K("&"), K("-"))


class Expando(List):
    grammar = '[', attr('begin', re.compile(r'\d+')), '-', \
        attr('end', re.compile(r'\d+')), ']'


class StringPart(str):
    grammar = re.compile(r'[\-_a-z0-9\.]+')


class Part(List):
    grammar = [StringPart, Expando]


class Hostname(List):
    grammar = some(Part)


class Pattern(str):
    grammar = re.compile(r'^\/.*\/$')


class Role(str):
    grammar = '@', name()


class RangePart(List):
    grammar = [Pattern, Hostname, Role]


class Range(List):
    grammar = RangePart, maybe_some(',', optional(Operator), RangePart)
