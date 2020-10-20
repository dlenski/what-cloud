import logging
import requests
from ipaddress import ip_address

from what_cloud import all_clouds

matched_ips = [ip_address(i) for i in [
    '208.86.91.234', '2a05:d07a:a000::1234', # AWS
    '20.37.64.123', '2603:1000:4:402::179',  # Azure
    '8.8.8.8', '2600:1901::1234',            # Google
    '131.0.72.1', '2405:8100::1234',         # CloudFlare
    '185.31.16.1', '2a04:4e40::1234',        # Fastly
]]

unmatched_ips = [ip_address(i) for i in [
    '1.1.1.1',
    '9.9.9.9',
]]

class test_known_ips:
    def setUp(self):
        session = requests.session()
        self.clouds = {n:c(session=session) for n,c in all_clouds.items()}

    def check_hits(self, expected_hits, ip):
        hits = 0
        for name, cr in self.clouds.items():
            logging.debug('checking if {} belongs to cloud provider {}'.format(ip, name))
            hits += bool(cr.check(ip))
        if hits != expected_hits:
            raise AssertionError("got {} hits for {}, instead of expected {}".format(hits, ip, expected_hits))

    def test_matched_ips(self):
        for ip in matched_ips:
            yield self.check_hits, 1, ip

    def test_unmatched_ips(self):
        for ip in unmatched_ips:
            yield self.check_hits, 0, ip
