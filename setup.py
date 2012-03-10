#!/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='pyrange',
    version='1.0',
    description='wsgi server for host lists',
    author='Nicholas Harteau',
    author_email='nrh@spotify.com',
    url='https://github.com/nrh/pyrange',
    packages=['distutils', 'distutils.command'],
    requires=['gserver', 'gevent', 'pysqlite', 'json'],
    setup_requires=['nose>=1.0'],
    tests_require=['requests'],
    license='Apache 2.0',
    test_suite='nose.collector',
    )

