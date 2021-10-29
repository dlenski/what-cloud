import ipaddress
import json

from .CloudRanges import CloudRanges, IP_NETWORK_REGEX

# https://postmaster.comcast.net/dynamic-IP-ranges.html
class Comcast(CloudRanges):
    def download(self, fp):
        # contains duplicates, and 2601::/20 is mysteriously missing
        url = 'https://postmaster.comcast.net/dynamic-IP-ranges.html'
        self._cache = {'v4': set(), 'v6': {'2601::/20'}}
        self._logger.info('Downloading {} to {} ...'.format(url, fp.name))
        for net in IP_NETWORK_REGEX.findall(self.session.get(url).text):
            self._cache['v6' if ':' in net else 'v4'].add(net)
        json.dump(self._cache, fp, default=list)

    def load(self, fp=None):
        if not fp:
            fn = self._cached('comcast-ip-ranges.json')
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
