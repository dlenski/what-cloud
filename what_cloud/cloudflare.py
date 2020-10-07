import os
import ipaddress
import json

from .CloudRanges import CloudRanges

# https://www.cloudflare.com/ips/
class CloudFlare(CloudRanges):
    def download(self, fp):
        self._cache = {}
        for v in ('v4', 'v6'):
            url = 'https://www.cloudflare.com/ips-{}'.format(v)
            self._logger.info('Downloading {} to {} ...'.format(url, fp.name))
            self._cache[v] = self.session.get(url).text.splitlines()
        json.dump(self._cache, fp)

    def load(self, fp=None):
        if not fp:
            fn = self._cached('cloudflare-ip-ranges.json')
            try:
                fp = open(fn)
            except FileNotFoundError:
                fp = open(fn, 'x+')
                self.download(fp)
                fp.flush()
                fp.seek(0)

        self._cache = j = json.load(fp)
        j['v4'] = list(map(ipaddress.IPv4Network, j['v4']))
        j['v6'] = list(map(ipaddress.IPv6Network, j['v6']))

    def check(self, ip):
        if type(ip) == ipaddress.IPv4Address:
            return [p for p in self._cache['v4'] if ip in p]
        elif type(ip) == ipaddress.IPv6Address:
            return [p for p in self._cache['v6'] if ip in p]
