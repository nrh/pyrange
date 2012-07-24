#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gevent import monkey; monkey.patch_all()
from  bottle import run
import config
import api_handler

conf = config.Config()
api = api_handler.APIHandler()

def rangeapp(env, start_response):
    res = api.handle_request(env)
    start_response(res.headerlist)
    return res.body

def start():
    run(host=conf.addr, port=conf.port, server='gevent').serve_forever()


