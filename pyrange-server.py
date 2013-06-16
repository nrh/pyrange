#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import logging.config
import configparser
from pprint import pformat
from pyrange.handler import app

parser = argparse.ArgumentParser()
parser.add_argument('-c',
                    metavar='<file>',
                    type=argparse.FileType('r'),
                    help='configuration file to load')
parser.add_argument('--log-config',
                    metavar='<file>',
                    dest='log_config',
                    help='logging configuration file')
args = parser.parse_args()

# must be Raw due to logging's use of interpolators
cf = configparser.RawConfigParser()
cf.read_file(args.c)

if args.log_config:
    logging.config.fileConfig(args.log_config)
else:
    # provide some sane logging defaults
    try:
        level = cf.get('logging', 'level')
    except (configparser.NoSectionError, configparser.NoOptionError):
        level = 'DEBUG'
    try:
        format = cf.get('logging', 'format')
    except (configparser.NoSectionError, configparser.NoOptionError):
        format = '''%(asctime)s - %(name)s - %(levelname)s - %(message)s'''

    level = getattr(logging, level.upper())
    logging.basicConfig(level=level, format=format)

logger = logging.getLogger(__name__)

# for flask, it wants uppercase in the main config dictionary
for key in dict(cf.items('flask')):
    if key == 'debug':
        app.config['DEBUG'] = cf.getboolean('flask', 'debug')
    else:
        app.config[key.upper()] = cf.get('flask', key)

# for other sections, we cram them in as a sub-dict keyed on
# the section name
for section in cf.sections():
    if section == 'flask':
        continue
    app.config.update({section: dict(cf.items(section))})

logger.debug(pformat(dict(app.config)))
app.run()  # whee!
