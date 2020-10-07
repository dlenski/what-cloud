import os
import ipaddress
import json

from .CloudRanges import CloudRanges

# https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html#aws-ip-syntax
class AWSCloud(CloudRanges):
    def download(self, fp):
        url = 'https://ip-ranges.amazonaws.com/ip-ranges.json'
        self._logger.info('Downloading {} to {} ...'.format(url, fp.name))
        fp.write(self.session.get(url).text)

    def load(self, fp=None):
        if not fp:
            fn = self._cached('aws-ip-ranges.json')
            try:
                fp = open(fn)
            except FileNotFoundError:
                fp = open(fn, 'x+')
                self.download(fp)
                fp.flush()
                fp.seek(0)

        self._cache = j = json.load(fp)
        for p in j.get('prefixes', ()):
            p['ip_prefix'] = ipaddress.ip_network(p['ip_prefix'])
        for p in j.get('ipv6_prefixes', ()):
            p['ipv6_prefix'] = ipaddress.ip_network(p['ipv6_prefix'])

    def check(self, ip):
        if type(ip) == ipaddress.IPv4Address:
            return [p for p in self._cache.get('prefixes') if ip in p['ip_prefix']]
        elif type(ip) == ipaddress.IPv6Address:
            return [p for p in self._cache.get('ipv6_prefixes') if ip in p['ipv6_prefix']]
