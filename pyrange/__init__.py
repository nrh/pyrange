# -*- coding: utf-8 -*-

from flask import Flask
app = Flask(__name__)

import pyrange.handler  # NOQA
import pyrange.store    # NOQA
