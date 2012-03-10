from urlparse import parse_qsl

class RangeRequest:

    '''Parse and validate a range request'''

    def __init__(self, env, start_resp):
        self.env = env
        self.start_resp = start_resp

        # these are all pretty much guaranteed to be here by the wsgi handler
        self.method = env['REQUEST_METHOD']
        self.path = env['PATH_INFO']
        self.query_string = self.parse_querystring(env['QUERY_STRING'])

        # these may not be; passed in via nginx
        self.verified = False
        if env.has_key('VERIFIED'):
            if env['VERIFIED'] == 'SUCCESS':
                self.verified = True

        # probably want to support other auth types here
        if env.has_key('DN'):
            self.user = pyrange.acl.User(self.parse_dn(env['DN'], 'CN'))

        # for clients with limited access to http methods, support
        # ?method=POST, for example
        if self.param('method'):
            self.method = self.param('method').upper()

        # common ones
        self.limit = self.param('limit') or 1000
        self.offset = self.param('offset')
        self.fields = self.param('fields')
        self.pretty = self.param('pretty')

        # some clients barf on response codes
        self.suppress_response_codes = self.param('suppress_response_codes')

    def parse_querystring(self, string):
        # do some custom crap to support '&foo=bar,baz'
        dict = {}
        for (name, value) in parse_qsl(string):
            if name in dict:
                dict[name] = dict[name] + value.split(',')
            else:
                dict[name] = value.split(',')
        return dict

    def param(self, key):
        try:
            return self.query_string[key]
        except KeyError:

            return False

    def parse_dn(self, dn, field):
        '''
        parse one of these:
        /C=US/ST=Florida/L=Orlando/O=CLIENT NAME/CN=CLIENT NAME
        '''

        d = dict({})
        for x in dn.split('/'):
            (k, v) = x.split('=')
            d[k] = v

        return d[field]

