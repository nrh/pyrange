#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime
from store import store, meta
import datetime

namespaces = Table('namespaces', meta,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('name', String(64)),
        Column('created_by', Integer, nullable=False),
        Column('created_on', DateTime, nullable=False, onupdate=datetime.datetime.now),
        Column('modified_by', Integer, nullable=False),
        Column('modified_on', DateTime, nullable=False, onupdate=datetime.datetime.now)
        )

roles = Table('roles', meta,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('name', String(64)),
        Column('namespace_id', None, ForeignKey('namespaces.id')),
        Column('created_by', Integer, nullable=False),
        Column('created_on', DateTime, nullable=False, onupdate=datetime.datetime.now),
        Column('modified_by', Integer, nullable=False),
        Column('modified_on', DateTime, nullable=False, onupdate=datetime.datetime.now)
        )

definitions = Table('definitions', meta,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('role_id', None, ForeignKey('roles.id')),
        Column('definition', String(128))
        )

# need acl relationship table?
acls = Table('acls', meta,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('name', String(64), nullable=False),
        Column('mask', String(4), nullable=False),
        Column('created_by', Integer, nullable=False),
        Column('created_on', DateTime, nullable=False, onupdate=datetime.datetime.now),
        Column('modified_by', Integer, nullable=False),
        Column('modified_on', DateTime, nullable=False, onupdate=datetime.datetime.now)
        )

members = Table('members', meta,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('name', String(128)),
        Column('role_id', None, ForeignKey('roles.id'))
        )

log = Table('log', meta,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('namespace_id', Integer),
        Column('role_id', Integer),
        Column('acl_id', Integer),
        Column('message', String(128))
        )


meta.create_all()

