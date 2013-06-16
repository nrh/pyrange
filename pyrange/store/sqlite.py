# -*- coding: utf-8 -*-

import sqlite3
from pyrange import app
import logging

logger = logging.getLogger(__name__)

__version__ = '0.1'


class Sqlite3Store:
    def __init__(self):
        # we should probably do some configuration
        logger.debug("connecting to %s" % app.config['storage']['db'])
        self.con = sqlite3.connect(app.config['storage']['db'])

    def status(self):
        return "%s %s" % (self.__class__.__name__, __version__)

    def add_role(self):
        pass

    def update_role(self):
        pass

    def delete_role(self):
        pass
