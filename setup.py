#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
from distutils.core import setup

setup(
    name='pyrange',
    version='1.0',
    description='wsgi server for host lists',
    author='Nicholas Harteau',
    author_email='nrh@spotify.com',
    url='https://github.com/nrh/pyrange',
    packages=['pyrange'],
    requires=['gserver', 'gevent', 'pysqlite', 'bottle', 'WebOb', 'requests'],
    setup_requires=['nose>=1.0'],
    license='Apache 2.0',
    test_suite='nose.collector',
    )

