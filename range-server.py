#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pyrange.handler import app
app.config.from_object('pyrange.config')

if os.getenv('PYRANGE_CONFIG'):
    app.config.from_envvar('PYRANGE_CONFIG')

app.run(debug=True)
