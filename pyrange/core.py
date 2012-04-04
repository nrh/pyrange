# -*- coding: utf-8 -*-

from bottle import HTTPError
from traceback import format_exc
import pdb
import store
from sqlalchemy.sql import text

# {{{ Namespace

class Base(object):
    def __init__(self):
        pass

class Namespace(Base):
    '''
    pyrange.Namespace

    id INTEGER NOT NULL,
    name VARCHAR(64),
    created_by INTEGER NOT NULL,
    created_on DATETIME NOT NULL,
    modified_by INTEGER NOT NULL,
    modified_on DATETIME NOT NULL,
    PRIMARY KEY (id)

    '''

    def __init__(self, name=None, data=None):
        self.name = name
        self.data = data

    def commit(self):
        if not self.exists():
            return self.create()
        else:
            return self.update()

    def create(self):
        '''sudo make me a namespace'''
        pdb.set_trace()
        t = store.conn.begin()
        insert = text("INSERT INTO namespaces VALUES ('',?,?,'',?,'')").compile()
        try:
            r1 = t.execute(insert, (self.name, 'nrh', 'nrh'))
            t.commit()
        except:
            t.rollback()
            raise HTTPError(code=500, output="transaction failure", traceback=format_exc(10))

        return {'ok':'created'}

    def exists(self):
        return False

    def update(self):
        pass

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
        return store.get('namespace',name)

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
        return store.get('namespace',name)

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
