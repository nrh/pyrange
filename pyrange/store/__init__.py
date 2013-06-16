# -*- coding: utf-8 -*-

import importlib
from pyrange import app

# global...singletone?
_store = None


def get_store():
    global _store
    if not _store:
        modulename, classname = app.config['storage']['class'].rsplit('.', 1)
        module = importlib.import_module(modulename)
        klass = getattr(module, classname)
        _store = klass()
    return _store
