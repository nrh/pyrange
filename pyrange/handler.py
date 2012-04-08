#!/usr/bin/python
# -*- coding: utf-8 -*-

import pdb
import sys
import json
from traceback import format_exc

from bottle import Bottle, Response, HTTPError, HTTPResponse
from bottle import response, request

import core
import store

app = Bottle()
import bottle

import datetime
import logging
FORMAT = \
    '%(asctime)s %(levelname)s %(filename)s:%(linenum)d %(funcName)s %message'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger(__name__)

# {{{ namespaces


@app.get('/namespaces')
def get_all_namespaces():
    '''request a list of namespaces'''
    logger.debug('GET /namespaces')
    body = {}
    nlist = store.get_all_namespaces()
    body.update({'namespaces': nlist })
    return body


@app.put('/namespaces')
def add_namespace():
    '''add a new namespace'''

    logger.debug('PUT /namespaces')
    body = {}

    try:
        r = json.load(request.body)
        ns = core.Namespace(r['name'], r)
        if ns.exists():
            ns.update()
            response.status = '200 OK Updated /namespaces/%s' % (ns.name, )
        else:
            ns.create()
            response.status = '201 OK Created /namespaces/%s' % (ns.name, )

        return body
    except Exception, e:

        logger.error(format_exc(10))
        if isinstance(e, HTTPError):
            raise
        else:
            raise HTTPError(code=400, output="couldn't understand your request"
                            , traceback=format_exc(10))


@app.get('/namespaces/<nsname>')
def get_namespace(nsname=None):
    '''get a namespace'''

    logger.debug('GET /namespace/%s' % (nsname, ))
    body = {}

    try:
        ns = core.Namespace(nsname)
        data = ns.data()
        # need to turn the datetime objects into strings for serialization.
        [data.update({k: int(data[k].strftime('%s'))}) for k in data.keys()
         if isinstance(data[k], datetime.datetime)]
        return {nsname: data}
    except Exception, e:

        logger.error(format_exc(10))
        if isinstance(e, HTTPError):
            raise
        else:
            raise HTTPError(code=400, output="couldn't understand your request"
                            , traceback=format_exc(10))


@app.put('/namespaces/<ns>')
def update_namespace(ns=None):
    '''add/update a namespace'''

    logger.debug('PUT /namespace/%s' % (ns, ))

    pass


@app.delete('/namespaces/<ns>')
def delete_namespace(ns=None):
    '''remove a namespace'''

    pass

# }}}
# {{{ roles


@app.get('/<ns>/roles')
def get_namespace_roles(ns=None):
    '''request a list of roles from a namespace'''

    pass


@app.put('/<ns>/roles')
def add_namespace_roles(ns=None):
    '''add or update roles in a namespace'''

    pass


@app.put('/<ns>/roles/<role>')
def update_namespace_role(ns=None, role=None):
    '''update a role'''

    pass


@app.delete('/<ns>/roles/<role>')
def delete_namespace_role(ns=None, role=None):
    '''delete a role'''

    pass

# }}}
# {{{ tags
#
#    @route('GET', '^\/tags\/?$')
#    def get_tags(self, match):
#        '''get list of tags'''
#
#        pass
#
#    @route('PUT', '^\/tags\/?$')
#    def add_tags(self, match):
#        '''add or update tags'''
#
#        pass
#
#    @route('GET', '^\/tags/[a-z0-9_\:]+')
#    def get_tag(self, match):
#        '''get a tag'''
#
#        pass
#
#    @route('PUT', '^\/tags/[a-z0-9_\:]+')
#    def update_tag(self, match):
#        '''update a tag'''
#
#        pass
#
#    @route('DELETE', '^\/tags/[a-z0-9_\:]+')
#    def delete_tag(self, match):
#        '''delete a tag'''
#
#        pass
#
#    # }}}
#    # {{{ acls
#
#    @route('GET', '^\/acls\/?$')
#    def get_acls(self, match):
#        '''get list of acls'''
#
#        pass
#
#    @route('PUT', '^\/acls\/?$')
#    def add_acls(self, match):
#        '''add or update acls'''
#
#        pass
#
#    @route('GET', '^\/acls/[a-z0-9_\:]+')
#    def get_acl(self, match):
#        '''get a acl'''
#
#        pass
#
#    @route('PUT', '^\/acls/[a-z0-9_\:]+')
#    def update_acl(self, match):
#        '''update a acl'''
#
#        pass
#
#    @route('DELETE', '^\/acls/[a-z0-9_\:]+')
#    def delete_acl(self, match):
#        '''delete a acl'''
#
#        pass
#
#    # }}}
#    # {{{ members
#
#    @route('GET', '^\/members\/?$')
#    def get_members(self, match):
#        '''get a list of members'''
#
#        pass
#
#    @route('GET', '^\/members\/[a-z0-9_\.]+')
#    def get_members(self, match):
#        '''get a members'''
#
#        pass
#
#    # }}}
#    # {{{ range
#
#    @route('GET', '^\\/range\\/?$')
#    @route('POST', '^\\/range\\/?$')
#    def expand_range(self, match):
#        '''expand a range expression'''
#
#        pass
#    # }}}
# {{{ misc helpers


def pretty_print(resp):
    '''takes a parsed-from-json response and pretty-prints it'''

    str = ''
    for key in resp:
        str += '''
>>> %s
''' % (key, )
        str += resp[key]
        str += '''
<<< %s
''' % (key, )

    return str


# }}}
# {{{ error response types


@app.error(400)
@app.error(401)
@app.error(403)
@app.error(404)
@app.error(405)
@app.error(418)
@app.error(500)
def respond_error(err):
    '''copy the err info into our HTTPResponse object'''

    body = {}
    response.content_type = 'application/json'

    if request.query.suppress_response_codes == u'1':
        response.status = '200 OK'
        body.update({'errc': err.status})
    else:
        response.status = err.status

    if err.traceback:
        body.update({'traceback': err.traceback})

    body.update({'error': err.output})
    return json.dumps(body)

# }}}

