#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re
import webob

import store
import auth
import request

baseurl = '/v1'
method_map = {
    'GET': {},
    'HEAD': {},
    'PUT': {},
    'POST': {},
    'DELETE': {},
    }

resp_codes = {
    200: 'OK',
    201: 'Created',
    400: 'Bad Request',
    401: 'Unauthorized',
    403: 'Forbidden',
    404: 'Not Found',
    }


def route(method, path_re):
    '''decorator for mapping an (http_method,regex) tuple to a function'''

    def decorate(f):
        regex = re.compile(path_re)
        method_map[method][regex] = f
        return f

    return decorate


class APIHandler(object):

    '''Handle a range API request, generate a usseful response for WSGI'''

    def __init__(self):
        self.response_headers = [('Content-type', 'application/json')]
        self.store = store.Store()

    def handle_request(self, env):
        '''Handle an API request, returning a webob.Response

        In all cases including errors, this method should return a valid
        webob.Response.

        @type env: dict
        @param env: the WSGI environment for the request
        @rtype: webob.Response
        @return: response object suitable for presentation in the API
        '''

        request_handler = self.default_handler

        # authenticate
        env = auth.authenticate(env)
        if isinstance(env, webob.Response):
            return env

        self.req = request.RangeRequest(env)
        path_map = method_map[self.req.method]

        handler_match = None
        for key in path_map.iterkeys():
            match = key.match(self.req.path)
            if match:
                handler_match = match.groups()
                request_handler = path_map[key]

        # fake out self here.
        return request_handler(self, handler_match)

    def default_handler(self, foo, match):  # foo is another copy of self due to fakery above
        return self.response_bad_request()

    # {{{ namespaces

    @route('GET', r'^\/namespaces/?$')
    def get_all_namespaces(self, match):
        '''request a list of namespaces'''

        return self.response_ok(body=self.store.get_all_namespaces())

    @route('PUT', r'^\/namespaces/?$')
    def add_namespaces(self, match):
        '''add a new namespace'''

        # am I authenticated?

        pass

    @route('GET', r'^\/namespaces/[a-z0-9]+')
    def get_namespace(self, match):
        '''get a namespace'''

        pass

    @route('PUT', r'^\/namespaces/[a-z0-9]+')
    def update_namespace(self, match):
        '''get a namespace'''

        pass

    @route('DELETE', r'^\/namespaces/[a-z0-9]+')
    def delete_namespace(self, match):
        '''get a namespace'''

        pass

    # }}}
    # {{{ roles

    @route('GET', '^\/[a-z0-9]+\/roles\/?$')
    def get_namespace_roles(self, match):
        '''request a list of roles from a namespace'''

        pass

    @route('PUT', '^\/[a-z0-9]+\/roles\/?$')
    def add_namespace_roles(self, match):
        '''add or update roles in a namespace'''

        pass

    @route('PUT', '^\/[a-z0-9]+\/roles\/[a-z0-9\.]+')
    def update_namespace_role(self, match):
        '''update a role'''

        pass

    @route('DELETE', '^\/[a-z0-9]+\/roles\/[a-z0-9\.]+')
    def delete_namespace_role(self, match):
        '''delete a role'''

        pass

    # }}}
    # {{{ tags

    @route('GET', '^\/tags\/?$')
    def get_tags(self, match):
        '''get list of tags'''

        pass

    @route('PUT', '^\/tags\/?$')
    def add_tags(self, match):
        '''add or update tags'''

        pass

    @route('GET', '^\/tags/[a-z0-9_\:]+')
    def get_tag(self, match):
        '''get a tag'''

        pass

    @route('PUT', '^\/tags/[a-z0-9_\:]+')
    def update_tag(self, match):
        '''update a tag'''

        pass

    @route('DELETE', '^\/tags/[a-z0-9_\:]+')
    def delete_tag(self, match):
        '''delete a tag'''

        pass

    # }}}
    # {{{ acls

    @route('GET', '^\/acls\/?$')
    def get_acls(self, match):
        '''get list of acls'''

        pass

    @route('PUT', '^\/acls\/?$')
    def add_acls(self, match):
        '''add or update acls'''

        pass

    @route('GET', '^\/acls/[a-z0-9_\:]+')
    def get_acl(self, match):
        '''get a acl'''

        pass

    @route('PUT', '^\/acls/[a-z0-9_\:]+')
    def update_acl(self, match):
        '''update a acl'''

        pass

    @route('DELETE', '^\/acls/[a-z0-9_\:]+')
    def delete_acl(self, match):
        '''delete a acl'''

        pass

    # }}}
    # {{{ members

    @route('GET', '^\/members\/?$')
    def get_members(self, match):
        '''get a list of members'''

        pass

    @route('GET', '^\/members\/[a-z0-9_\.]+')
    def get_members(self, match):
        '''get a members'''

        pass

    # }}}
    # {{{ range

    @route('GET', '^\\/range\\/?$')
    @route('POST', '^\\/range\\/?$')
    def expand_range(self, match):
        '''expand a range expression'''

        pass
    # }}}

    def response(self, code, body):
        if param_is_true(self.req.params['suppress_response_codes']):
            code = 200

        if param_is_true(self.req.params['pretty']):
            jsopts = {'sort_keys': True, 'indent': 4}
        else:
            jsopts = {}

        message = '%d %s' % (code, resp_codes[code])
        self.res.status = message

        if self.req.fields:
            body = self.filter_body(body)

        self.req.start_resp(self.res.status, self.res.headerlist)
        self.res.body = json.dumps(body, **jsopts)
        return self.res

    def filter_body(self, body):
        d = dict({})
        for k in self.req.fields:
            try:
                d[k] = body[k]
            except KeyError:
                d[k] = None
        return d

    # {{{ success response types
    # body is always a dict

    def response_ok(self, body=dict({})):
        return self.response(200, body)

    def response_created(self, body=dict({})):
        return self.response(201, body)

    def response_deleted(self, body=dict({})):
        return self.response(200, body)

    # }}}
    # {{{ error response types

    def response_error(self, errc, errmsg, more_info=None, body=dict({})):
        body['error'] = errmsg
        if more_info:
            body['more_info'] = more_info
        return self.response(errc, body)

    def response_bad_request(self, body=dict({})):
        return self.response_error(400, "I couldn't understand your request",
                                   body=body)

    def response_unauthorized(self, body=dict({})):
        return self.response_error(401,
                                   'Authorization required to access this resource'
                                   , body=body)

    def response_forbidden(self, body=dict({})):
        return self.response_error(403,
                                   'Insufficient privileges to access this resource'
                                   , body=body)

    def response_not_found(self, body=dict({})):
        return self.response_error(404, 'Resource not found', body=body)


    # }}}

