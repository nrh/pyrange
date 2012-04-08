#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, \
    DateTime, create_engine, select
import datetime
import os
import pdb

from config import conf
import logging
FORMAT ='%(asctime)s %(levelname)s %(filename)s:%(linenum)d %(funcName)s %message'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger(__name__)

meta = MetaData()
engine = create_engine(conf.db, echo=False)
meta.bind = engine
conn = engine.connect()

# {{{ table definitions
tables = {
    'namespaces': Table('namespaces', meta,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('name', String(64)),
        Column('created_by', String(64), nullable=False),
        Column('created_on', DateTime, default=datetime.datetime.now),
        Column('modified_by', String(64), nullable=False),
        Column('modified_on', DateTime, onupdate=datetime.datetime.now, default=datetime.datetime.now),
        ),
    'roles': Table('roles', meta,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('name', String(64)),
        Column('namespace_id', None, ForeignKey('namespaces.id')),
        Column('created_by', Integer, nullable=False),
        Column('created_on', DateTime, nullable=False,
               onupdate=datetime.datetime.now),
        Column('modified_by', Integer, nullable=False),
        Column('modified_on', DateTime, nullable=False,
               onupdate=datetime.datetime.now),
        ),
    'definitions': Table('definitions', meta,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('role_id', None, ForeignKey('roles.id')),
        Column('definition', String(128))
        ),
    'acls': Table('acls', meta,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('name', String(64), nullable=False),
        Column('mask', String(4), nullable=False),
        Column('created_by', Integer, nullable=False),
        Column('created_on', DateTime, nullable=False,
               onupdate=datetime.datetime.now),
        Column('modified_by', Integer, nullable=False),
        Column('modified_on', DateTime, nullable=False,
               onupdate=datetime.datetime.now),
        ),
    'members': Table('members', meta,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('name', String(128)),
        Column('role_id', None, ForeignKey('roles.id'))
        ),
    'log': Table( 'log', meta,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('namespace_id', Integer),
        Column('role_id', Integer),
        Column('acl_id', Integer),
        Column('message', String(128)),
        ),
    }

# }}}


def get_table(tname):
    t = Table(tname, meta, autoload=True)
    if t.exists():
        logger.debug('re-using %s' % (tname,))
    else:
        logger.info('creating %s' % (tname,))
        t.create()
    return t

def get_all_namespaces():
    s = select([namespaces.c.name])
    res = s.execute().fetchall()
    return [x.values().pop() for x in res]

namespaces = get_table('namespaces')

