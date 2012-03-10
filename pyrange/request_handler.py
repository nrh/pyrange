#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import re

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


def handle(method, path_re):
    '''decorator for mapping an (http_method,regex) tuple to a function'''
    def wrap(f):
        regex = re.compile(path_re)
        method_map[method][regex] = f
        return f

    return wrap


class RangeRequestHandler:

    '''Take a range request object, generate a useful response for WSGI'''

    def __init__(self, req):
        self.req = req
        self.response_headers = [('Content-type', 'application/json')]

    def default_handler(self, foo, match):
        return self.response_bad_request()

    def handle_request(self):
        request_handler = self.default_handler
        path_map = method_map[self.req.method]

        handler_match = None
        for key in path_map.iterkeys():
            match = key.match(self.req.path)
            if match:
                handler_match = match.groups()
                request_handler = path_map[key]

        # fake out self here.
        return request_handler(self,handler_match)

    # {{{ namespaces

    @handle('GET', '^\/namespaces/?$')
    def get_all_namespaces(self, match):
        '''request a list of namespaces'''

        return self.response_ok()

    @handle('PUT', '^\/namespaces/?$')
    def add_namespaces(self, match):
        '''add a new namespace'''

        pass

    @handle('GET', '^\/namespaces/[a-z0-9]+')
    def get_namespace(self, match):
        '''get a namespace'''

        pass

    @handle('PUT', '^\/namespaces/[a-z0-9]+')
    def update_namespace(self, match):
        '''get a namespace'''

        pass

    @handle('DELETE', '^\/namespaces/[a-z0-9]+')
    def delete_namespace(self, match):
        '''get a namespace'''

        pass

    # }}}
    # {{{ roles

    @handle('GET', '^\/[a-z0-9]+\/roles\/?$')
    def get_namespace_roles(self, match):
        '''request a list of roles from a namespace'''

        pass

    @handle('PUT', '^\/[a-z0-9]+\/roles\/?$')
    def add_namespace_roles(self, match):
        '''add or update roles in a namespace'''

        pass

    @handle('PUT', '^\/[a-z0-9]+\/roles\/[a-z0-9\.]+')
    def update_namespace_role(self, match):
        '''update a role'''

        pass

    @handle('DELETE', '^\/[a-z0-9]+\/roles\/[a-z0-9\.]+')
    def delete_namespace_role(self, match):
        '''delete a role'''

        pass

    # }}}
    # {{{ tags

    @handle('GET', '^\/tags\/?$')
    def get_tags(self, match):
        '''get list of tags'''

        pass

    @handle('PUT', '^\/tags\/?$')
    def add_tags(self, match):
        '''add or update tags'''

        pass

    @handle('GET', '^\/tags/[a-z0-9_\:]+')
    def get_tag(self, match):
        '''get a tag'''

        pass

    @handle('PUT', '^\/tags/[a-z0-9_\:]+')
    def update_tag(self, match):
        '''update a tag'''

        pass

    @handle('DELETE', '^\/tags/[a-z0-9_\:]+')
    def delete_tag(self, match):
        '''delete a tag'''

        pass

    # }}}
    # {{{ acls

    @handle('GET', '^\/acls\/?$')
    def get_acls(self, match):
        '''get list of acls'''

        pass

    @handle('PUT', '^\/acls\/?$')
    def add_acls(self, match):
        '''add or update acls'''

        pass

    @handle('GET', '^\/acls/[a-z0-9_\:]+')
    def get_acl(self, match):
        '''get a acl'''

        pass

    @handle('PUT', '^\/acls/[a-z0-9_\:]+')
    def update_acl(self, match):
        '''update a acl'''

        pass

    @handle('DELETE', '^\/acls/[a-z0-9_\:]+')
    def delete_acl(self, match):
        '''delete a acl'''

        pass

    # }}}
    # {{{ members

    @handle('GET', '^\/members\/?$')
    def get_members(self, match):
        '''get a list of members'''

        pass

    @handle('GET', '^\/members\/[a-z0-9_\.]+')
    def get_members(self, match):
        '''get a members'''

        pass

    # }}}
    # {{{ range

    @handle('GET', '^\\/range\\/?$')
    @handle('POST', '^\\/range\\/?$')
    def expand_range(self, match):
        '''expand a range expression'''

        pass
    # }}}

    def response(self, code, body):
        if self.req.suppress_response_codes:
            code = 200

        if self.req.pretty:
            jsopts = {'sort_keys': True, 'indent': 4}
        else:
            jsopts = {}

        message = '%d %s' % (code, resp_codes[code])

        if self.req.fields:
            body = self.filter_body(body)

        self.req.start_resp(message, self.response_headers)
        return json.dumps(body, **jsopts)

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
                              'Authorization required to access this resource',
                              body=body)

    def response_forbidden(self, body=dict({})):
        return self.response_error(403,
                              'Insufficient privileges to access this resource'
                              , body=body)

    def response_not_found(self, body=dict({})):
        return self.response_error(404, 'Resource not found', body=body)


    # }}}

