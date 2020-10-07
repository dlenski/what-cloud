import os
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
            r = self.session.get('https://www.microsoft.com/en-us/download/confirmation.aspx?id={}'.format(num))
            r.raise_for_status()
            m = re.search(r'https://download.microsoft.com/\S+/ServiceTags_\S+_\d+.json', r.text)
            assert m is not None
            jurl = m.group();
            self._logger.info('Downloading {} to {} ...'.format(jurl, fp.name))
            r = self.session.get(jurl, stream=True)
            r.raise_for_status()
            self._cache.append({'url': jurl, 'contents': json.load(r.raw)})
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
