#!/usr/bin/python
# -*- coding: utf-8 -*-

import pdb
import sys
import json
from traceback import format_exc

from bottle import Bottle, Response, HTTPError
from bottle import response, request

from core import AccessList, Member, Namespace, Role

app = Bottle()
import bottle

# {{{ namespaces

@app.get('/namespaces')
def get_all_namespaces():
    '''request a list of namespaces'''

    if not hasattr(response, '_body'):
        response._body = {}

    response._body.update({'namespaces':['testns']})
    return response._body


@app.put('/namespaces')
def add_namespace():
    '''add a new namespace'''

    if not hasattr(response, '_body'):
        response._body = {}

    try:
        ns = Namespace(json.load(request.body))
        response._body = ns.commit()
    except:
        # if something lower-level tries to pass up an HTTPError, assume they know what they're doing and let it through
        if sys.exc_type == 'HTTPError':
            raise
        else:
            raise HTTPError(code=400, output="couldn't understand your request", traceback=format_exc(10))

    return response._body


@app.get('/namespaces/<ns>')
def get_namespace(ns=None):
    '''get a namespace'''

    pass


@app.put('/namespaces/<ns>')
def update_namespace(ns=None):
    '''add/update a namespace'''

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
#
#    def response(self, code, body):
#        if param_is_true(self.req.params['suppress_response_codes']):
#            code = 200
#
#        if param_is_true(self.req.params['pretty']):
#            jsopts = {'sort_keys': True, 'indent': 4}
#        else:
#            jsopts = {}
#
#        message = '%d %s' % (code, resp_codes[code])
#        self.res.status = message
#
#        if self.req.fields:
#            body = self.filter_body(body)
#
#        self.req.start_resp(self.res.status, self.res.headerlist)
#        self.res.body = json.dumps(body, **jsopts)
#        return self.res
#
#    def filter_body(self, body):
#        d = dict({})
#        for k in self.req.fields:
#            try:
#                d[k] = body[k]
#            except KeyError:
#                d[k] = None
#        return d
#
#    # {{{ success response types
#    # body is always a dict
#
#    def response_ok(self, body=dict({})):
#        return self.response(200, body)
#
#    def response_created(self, body=dict({})):
#        return self.response(201, body)
#
#    def response_deleted(self, body=dict({})):
#        return self.response(200, body)
#
#    # }}}
# {{{ error response types


@app.error(400)
@app.error(401)
@app.error(403)
@app.error(404)
@app.error(405)
@app.error(418)
@app.error(500)
def respond_error(err):
    if not hasattr(response, '_body'):
        response._body = {}

    if request.query.suppress_response_codes == u'1':
        response.status = '200 OK'
        response._body.update({'errc': err.status})

    response.content_type = 'application/json'
    response._body.update({'error': err.output})
    if err.traceback:
        response._body.update({'traceback': err.traceback})

    return json.dumps(response._body)

# }}}

