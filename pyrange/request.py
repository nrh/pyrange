
from urlparse import parse_qsl
from webob import Request

class RangeRequest(Request):

    '''Parse and validate a range request'''

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
            return self.params[key]
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

