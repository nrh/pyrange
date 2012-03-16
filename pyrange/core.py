#!/usr/bin/python
# -*- coding: utf-8 -*-

from store import store

class Namespace(object):
    '''
    pyrange.Namespace
    attributes:
        name
        acls
        roles
        created_by
        created_at
    '''

# namespace schema
# id            int primary key
# name          str(64)
# created_by    int
# created_on    timestamp
# modified_by   int
# modified_on   timestamp

    def __init__(self, name):
        self._meta = {'name': name}
        store.

    def commit(self):

    def name(self):
        return self._meta['name']

    def acls(self):
        return self._acls

    def created_by(self):
        return self._created_by

    def roles(self):
        return store.get('namespace',name)


# -*- coding: utf-8 -*-

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


# -*- coding: utf-8 -*-

class AccessList(object):
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


class User(object):
    '''
    '''

class Group(object):
    '''
    '''

