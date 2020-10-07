import logging
import requests
from ipaddress import ip_address

from what_cloud import all_clouds

session = requests.session()
clouds = {n:c(session=session) for n,c in all_clouds.items()}

matched_ips = [ip_address(i) for i in [
    '208.86.91.234', '2a05:d07a:a000::1234', # AWS
    '20.37.64.123', '2603:1000:4:402::179',  # Azure
    '8.8.8.8', '2600:1901::1234',            # Google
    '131.0.72.1', '2405:8100::1234',         # CloudFlare
]]
unmatched_ips = [ip_address(i) for i in [
    '1.1.1.1',
    '9.9.9.9',
]]

def _count_hits(ip):
    hits = 0
    for name, cr in clouds.items():
        logging.debug('checking if {} belongs to cloud provider {}'.format(ip, name))
        hits += bool(cr.check(ip))
    return hits

def test_matched_ips():
    unexpected = [(i, h) for i, h in ((i, _count_hits(i)) for i in matched_ips) if h != 1]
    if unexpected:
        raise AssertionError("\n".join("got {} hits for {}, instead of expected 1".format(hits, ip) for ip, hits in unexpected))

def test_unmatched_ips():
    unexpected = [(i, h) for i, h in ((i, _count_hits(i)) for i in unmatched_ips) if h != 0]
    if unexpected:
        raise AssertionError("\n".join("got {} hits for {}, instead of expected 0".format(hits, ip) for ip, hits in unexpected))
