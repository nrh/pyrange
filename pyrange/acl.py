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

