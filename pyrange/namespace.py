#!/usr/bin/python
# -*- coding: utf-8 -*-

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


