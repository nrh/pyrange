# -*- coding: utf-8 -*-
import ply.lex
import re
import sys

tokens = (
    'ROLE',         # @foo
    'UNION',        # exp,exp
    'DIFF',         # exp,-exp
    'INTER',        # exp,&exp
    'EOL',
    'EOF',
    'WSPACE',
    'TAGS',
    )

t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_ROLE(t):
    r'^@[a-z\.]+'

def t_UNION(t):
    r','

def t_DIFF(t):
    r',-'

def t_INTER(t):
    r',&'

def t_EOL(t):
    r'$'

def t_WSPACE(t):
    r'\r\n\t\ '

def t_TAGS(t):
    r''

