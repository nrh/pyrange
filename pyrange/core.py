#!/usr/bin/python
# -*- coding: utf-8 -*-

from bottle import HTTPError
from traceback import format_exc
import pdb
import store
from sqlalchemy.sql import text

import time
import logging
FORMAT ='%(asctime)s %(levelname)s %(filename)s:%(linenum)d %(funcName)s %message'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger(__name__)

__all__ = ["Namespace"]

class Base(object):

    def __init__(self):
        pass

# {{{ Namespace

class Namespace(Base):
    '''our main man, the namespace'''

    def __init__(self, name, request_data=None):  # name=None, data=None):
        logger.debug("init %s" % name)
        self.name = name
        self._request_data = request_data
        self._data = None

    def exists(self):
        logger.debug("exists %s" % self.name)
        select = store.namespaces.select(store.namespaces.c.name == self.name)
        res = select.execute()
        if res.rowcount == -1:
            return False
        elif res.rowcount == 1:
            return True

        raise HTTPError(code=500, output='internal consistency error')

    def create(self):
        '''sudo make me a namespace'''
        logger.debug("create %s" % self.name)
        t = store.conn.begin()
        insert = store.namespaces.insert({
            'name': self.name,
            'created_by': 'nrh',
            'modified_by': 'nrh',
            })
        try:
            res = insert.execute()
            t.commit()
        except:
            t.rollback()
            raise HTTPError(code=500, output='transaction failure',
                            traceback=format_exc(10))

        return self

    def update(self):
        ''' merge dicts and commit back to the database'''
        logger.debug("update %s" % self.name)
        pass

    def data(self):
        '''return a dict of namespace data, suitable for returning in an http response'''
        logger.debug("data %s" % self.name)
        if not self._data:
            select = store.namespaces.select(store.namespaces.c.name == self.name)
            res = select.execute()
            row = res.fetchone()
            self._data = dict([(k,row[k]) for k in res.keys()])

        return self._data

# }}}
# {{{ Role


class Role(object):

    '''
    pyrange.Role
    attributes:
        name
        acls
        tags
        members
        created_by
        created_at
    '''

    def __init__(self, name):
        self._meta = {'name': name}

    def name(self):
        return self._meta['name']

    def acls(self):
        return self._acls

    def created_by(self):
        return self._created_by

    def roles(self):
        return store.get('namespace', name)


# }}}
# {{{ Member


class Member(Base):

    def __init__(self):
        pass


# }}}
# {{{ AccessList


class AccessList(Base):

    '''
    pyrange.AccessList
    attributes:
        name
        users
        groups
        created_by
        created_at
        last_modified_by
        last_modified_at
    '''

    def __init__(self, name):
        self._meta = {'name': name}

    def name(self):
        return self._meta['name']

    def acls(self):
        return self._acls

    def created_by(self):
        return self._created_by

    def roles(self):
        return store.get('namespace', name)


# }}}
# {{{ User


class User(Base):

    '''
    '''


# }}}
# {{{ Group


class Group(Base):

    '''
    '''


# }}}
