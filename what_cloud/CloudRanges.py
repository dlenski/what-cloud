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
        d = os.path.join(os.path.expanduser('~'), '.what-cloud-cache')
        os.makedirs(d, exist_ok=True)
        return os.path.join(d, fn)
    def load(fp=None):
        pass
    def save(self, fp=None):
        pass
    def check(self, ip):
        pass
