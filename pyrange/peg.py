from __future__ import unicode_literals, print_function
from pypeg2 import *  # NOQA

# foo[1-10].bar.com
# [1-10]foo.bar.com
# foo[1-10]bar.baz.com

exprsep = ','


class Expando(List):
    grammar = '[', attr('begin', re.compile(r'\d+')), '-', \
        attr('end', re.compile(r'\d+')), ']'


class StringPart(str):
    grammar = re.compile(r'[\-_a-z0-9\.]+')


class Part(List):
    grammar = [StringPart, Expando]


class Hostname(List):
    grammar = some(Part)


class Operator(Keyword):
    '''
    @ => role lookup
    & => intersection
    - => disjoint
    '''
    grammar = Enum(K('@'), K('&'), K('-'))


class Pattern(str):
    grammar = '/', re.compile(r'[^\/]'), '/'


class RangePart(List):
    grammar = [Pattern, Hostname]


class Range(Namespace):
    grammar = some(csl(RangePart))
