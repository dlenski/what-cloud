import os
import ipaddress
import json

from .CloudRanges import CloudRanges

# https://docs.fastly.com/en/guides/accessing-fastlys-ip-ranges
class Fastly(CloudRanges):
    def download(self, fp):
        self._cache = []
        url = 'https://api.fastly.com/public-ip-list'
        self._logger.info('Downloading {} to {} ...'.format(url, fp.name))
        fp.write(self.session.get(url).text)

    def load(self, fp=None):
        if not fp:
            fn = self._cached('fastly-ip-ranges.json')
            try:
                fp = open(fn)
            except FileNotFoundError:
                fp = open(fn, 'x+')
                self.download(fp)
                fp.flush()
                fp.seek(0)

        self._cache = j = json.load(fp)
        j['addresses'] = list(map(ipaddress.IPv4Network, j['addresses']))
        j['ipv6_addresses'] = list(map(ipaddress.IPv6Network, j['ipv6_addresses']))

    def check(self, ip):
        if type(ip) == ipaddress.IPv4Address:
            return [p for p in self._cache['addresses'] if ip in p]
        elif type(ip) == ipaddress.IPv6Address:
            return [p for p in self._cache['ipv6_addresses'] if ip in p]
