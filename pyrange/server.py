#!/usr/bin/python
# -*- coding: utf-8 -*-

from gevent import monkey; monkey.patch_all()
from bottle import debug
from bottle import run

from handler import app
from config import conf

def start():
    debug(True)
    run(app, host=conf.addr, port=conf.port, server='gevent', reloader=True)


