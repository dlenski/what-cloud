import ipaddress
import json

from .CloudRanges import CloudRanges

# https://docs.cloud.oracle.com/en-us/iaas/Content/General/Concepts/addressranges.htm
class OracleCloud(CloudRanges):
    def download(self, fp):
        self._cache = []
        url = 'https://docs.cloud.oracle.com/en-us/iaas/tools/public_ip_ranges.json'
        self._logger.info(f'Downloading {url} to {fp.name} ...')
        r = self.session.get(url)
        r.raise_for_status()
        j = r.json()

        # Transform from regions { region, cidrs { cidr, tags[] } }
        # to just cidrs { cidr, region, tags[] }
        for region in j['regions']:
            cidrs = region.pop('cidrs')
            for cidr in cidrs:
                cidr.update(region)
                self._cache.append(cidr)
        json.dump(self._cache, fp)

    def load(self, fp=None):
        if not fp:
            fn = self._cached('oracle-ip-ranges.json')
            try:
                fp = open(fn)
            except FileNotFoundError:
                fp = open(fn, 'x+')
                self.download(fp)
                fp.flush()
                fp.seek(0)

        self._cache = j = json.load(fp)
        for cidr in self._cache:
            cidr['cidr'] = ipaddress.ip_network(cidr['cidr'])

    def check(self, ip):
        return [cidr for cidr in self._cache if ip in cidr['cidr']]
