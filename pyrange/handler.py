# -*- coding: utf-8 -*-

from pyrange import app


@app.route('/')
def hello_world():
    return 'hi!'
