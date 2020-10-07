import os
import ipaddress
import json
import re
from copy import deepcopy

from .CloudRanges import CloudRanges

_subclouds = (
    ('Cloud', 'cloud', None),                   # Google cloud only. https://cloud.google.com/compute/docs/faq#find_ip_range
    ('Google', 'goog', {'service': 'Google'}),  # Everything Google? https://stackoverflow.com/a/63406235
)

class GoogleCloud(CloudRanges):
    def download(self, fp):
        self._cache = []
        for name, fn, extra in _subclouds:
            url = 'https://www.gstatic.com/ipranges/{}.json'.format(fn)
            self._logger.info('Downloading {} to {} ...'.format(url, fp.name))
            r = self.session.get(url, stream=True)
            r.raise_for_status()

            c = json.load(r.raw)
            if extra:
                for p in c['prefixes']:
                    p.update(extra)
            self._cache.append({'url': url, 'contents': c})
        json.dump(self._cache, fp)

    def load(self, fp=None):
        if not fp:
            fn = self._cached('google-ip-ranges.json')
            try:
                fp = open(fn)
            except FileNotFoundError:
                fp = open(fn, 'x+')
                self.download(fp)
                fp.flush()
                fp.seek(0)

        self._cache = json.load(fp)
        for st in self._cache:
            j = st['contents']
            for p in j['prefixes']:
                if 'ipv4Prefix' in p:
                    p['ipv4Prefix'] = ipaddress.ip_network(p['ipv4Prefix'])
                if 'ipv6Prefix' in p:
                    p['ipv6Prefix'] = ipaddress.ip_network(p['ipv6Prefix'])

    def check(self, ip):
        results = []
        for st in self._cache:
            j = st['contents']
            if type(ip) == ipaddress.IPv4Address:
                results.extend(p for p in j['prefixes'] if ip in p.get('ipv4Prefix',()))
            elif type(ip) == ipaddress.IPv6Address:
                results.extend(p for p in j['prefixes'] if ip in p.get('ipv6Prefix',()))
        return results
