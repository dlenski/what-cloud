import logging
import os

import requests


class CloudRanges:
    def __init__(self, session=requests):
        self._cache = None
        self.session = session
        self.load()
    @property
    def _logger(self):
        return logging.getLogger(#((__module__ + '.') if __module__ else '') +
            self.__class__.__name__)
    def _cached(self, fn=None):
        return os.path.join(os.path.dirname(__file__), 'cache', fn)
    def load(fp=None):
        pass
    def save(fp=None):
        pass
    def check(self, ip):
        return None
