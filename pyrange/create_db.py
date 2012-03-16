#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from store import store

meta = MetaData()

namespaces = Table('namespaces', meta,
        Column('id', Integer, primary_key=True),
        Column('name', String(64)),
        Column('created_by', Integer),
        Column('created_on', Integer),
        Column('modified_by', Integer),
        Column('modified_on', Integer)
        )

roles = Table('roles', meta,
        Column('id', Integer, primary_key=True),
        Column('name', String(64)),
        Column('namespace_id', None, ForeignKey('namespaces.id')),
        Column('created_by', Integer),
        Column('created_on', Integer),
        Column('modified_by', Integer),
        Column('modified_on', Integer)
        )

definitions = Table('definitions', meta,
        Column('id', Integer, primary_key=True),
        Column('role_id', None, ForeignKey('roles.id')),
        Column('definition', String(128))
        )

# need acl relationship table?
acls = Table('acls', meta,
        Column('id', Integer, primary_key=True),
        Column('name', String(64)),
        Column('mask', String(4)),
        Column('created_by', Integer),
        Column('created_on', Integer),
        Column('modified_by', Integer),
        Column('modified_on', Integer)
        )

members = Table('members', meta,
        Column('id', Integer, primary_key=True),
        Column('name', String(128)),
        Column('role_id', None, ForeignKey('roles.id'))
        )

log = Table('log', meta,
        Column('id', Integer, primary_key=True),
        Column('namespace_id', Integer),
        Column('role_id', Integer),
        Column('acl_id', Integer),
        Column('message', String(128))
        )


meta.create_all(store)

