# -*- coding: utf-8 -*-
import argparse
import yaml

parser = argparse.ArgumentParser(description='start the pyrange server')

parser.add_argument('-c', dest='configfile', default=None,
                    type=str, help='config file')
parser.add_argument('--port', default=9191, type=int, help='port')
parser.add_argument('--addr', default='127.0.0.1', type=str,
                    help='address for bind()')
parser.add_argument('--db', default='sqlite:///:memory:', type=str,
                    help='sqlalchemy-friend database reference')
args = parser.parse_args()


class Config(object):

    def __init__(self, d):
        self.d = d

    def __getattr__(self, m):
        return self.d.get(m, None)

    def __str__(self):
        return repr(self.d)

if args.configfile:
    with open(args.configfile) as f:
        y = yaml.load(f)
        conf = Config(dict(y.items() + dict(args._get_kwargs()).items()))
        print conf
else:
    conf = args


