#!/usr/bin/python
# -*- coding: utf-8 -*-

import ply.lex as lex
import ply.yacc as yacc
import sys

# foo[1-10]
# foo[1-10],foo[13-14]

tokens = (
    'STRING',
    'LBRACE',
    'NUMBER',
    'DASH',
    'RBRACE',
    'UNION',
    'INTERSECT',
    'SUBTRACT',
    )
t_STRING    = r'[a-zA-Z0-9\.][a-zA-Z0-9\.]*'
t_LBRACE    = r'\['
t_DASH      = r'(-|\.\.)'
t_RBRACE    = r'\]'
t_INTERSECT = r',\&'
t_SUBTRACT  = r',\-'
t_UNION     = r','

precedence = (
        ('right', 'INTERSECT','SUBTRACT'),
        ('right', 'UNION')
        )

def t_NUMBER(t):
    r'''\d+'''

    t.value = int(t.value)
    return t


def t_newline(t):
    r'''\n+'''

    t.lexer.lineno += len(t.value)


def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)


def p_expression(p):
    '''expression : expression UNION expression
                  | expression INTERSECT expression
                  | expression SUBTRACT expression'''

    if p[2] == t_UNION:
        p[0] = p[1].union(p[3])
    elif p[2] == t_INTERSECT:
        p[0] = p[1].intersection(p[3])
    elif p[2] == t_SUBTRACT:
        p[0] = set([x for x in p[1] if x not in p[3]])


def p_expression_literal(p):
    '''expression : STRING outer'''

    p[0] = set([p[1] + str(x) for x in p[2]])


def p_expansion_outer(p):
    '''outer : LBRACE expando RBRACE'''

    p[0] = p[2]


def p_expansion_inner(p):
    '''expando : NUMBER DASH NUMBER'''

    p[0] = set(xrange(p[1], p[3] + 1))


def p_error(p):
    print 'syntax error! %s' % p



lexer = lex.lex(debug=1)
parser = yacc.yacc(debug=1)

def range_parser(exp):
    return parser.parse(exp)

