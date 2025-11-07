import ipaddress
import json
import re
from copy import deepcopy

from .CloudRanges import CloudRanges

_subclouds = (
    ('Public', 56519),
    ('US Government', 57063),
    ('China', 57062),
    ('Germany', 57064),
)

# https://github.com/MicrosoftDocs/azure-docs/blob/master/articles/virtual-network/service-tags-overview.md#user-content-discover-service-tags-by-using-downloadable-json-files
class AzureCloud(CloudRanges):
    def download(self, fp):
        self._cache = []
        for name, num in _subclouds:
            r = self.session.get(
                f'https://www.microsoft.com/en-us/download/details.aspx?id={num}', allow_redirects=True,
                headers={'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"})
            r.raise_for_status()
            m = re.search(r'https://download.microsoft.com/\S+/ServiceTags_\S+_\d+.json', r.text)
            assert m is not None, \
                f"Didn't find expected URL (https://download.microsoft.com/*/ServiceTags_ABC_NNN.json) in contents of {r.url}"
            jurl = m.group()
            self._logger.info(f'Downloading {jurl} to {fp.name} ...')
            r = self.session.get(jurl)
            r.raise_for_status()
            self._cache.append({'url': jurl, 'contents': r.json()})
        json.dump(self._cache, fp)

    def load(self, fp=None):
        if not fp:
            fn = self._cached('azure-ip-ranges.json')
            try:
                fp = open(fn)
            except FileNotFoundError:
                fp = open(fn, 'x+')
                self.download(fp)
                fp.flush()
                fp.seek(0)

        self._cache = json.load(fp)
        for st in self._cache:
            for v in st['contents']['values']:
                v['properties']['addressPrefixes'] = list(map(ipaddress.ip_network, v['properties']['addressPrefixes']))

    def check(self, ip):
        results = []
        for st in self._cache:
            for v in st['contents']['values']:
                mp = next((p for p in v['properties']['addressPrefixes'] if ip in p), None)
                if mp:
                    st2 = deepcopy(st)
                    v2 = deepcopy(v)
                    v2['properties']['addressPrefixes'] = [mp]
                    st2['contents']['values'] = [v2]
                    results.append(st2['contents'])
        return results
