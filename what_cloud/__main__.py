#!/usr/bin/env python3

import logging
import argparse
import ipaddress
import requests
import os
import socket
from itertools import chain
from pprint import pprint

from . import all_clouds

logging.basicConfig(level=logging.INFO)

def ipaddress_or_hostname(val):
    try:
        return ipaddress.ip_address(val)
    except ValueError:
        pass

    ips = []
    for af in (socket.AF_INET, socket.AF_INET6):
        try:
            ips += [ipaddress.ip_address(gai[4][0]) for gai in socket.getaddrinfo(val, None, family=af, proto=socket.IPPROTO_TCP)]
        except socket.gaierror:
            pass
    if ips:
        return val, ips

    raise argparse.ArgumentTypeError(f"could not resolve IPv4 or IPv6 address for {val!r}")

def main():
    p = argparse.ArgumentParser()
    p.add_argument('-v','--verbose', default=0, action='count')
    p.add_argument('-p','--pretty', action='store_true')
    p.add_argument('ip_or_hostname', type=ipaddress_or_hostname, nargs='+', help='IPv4 or IPv6 address, or domain name')
    args = p.parse_args()

    session = requests.session()
    clouds = {n:c(session=session) for n,c in all_clouds.items()}

    for ip_or_hostname in args.ip_or_hostname:
        if isinstance(ip_or_hostname, ipaddress._BaseAddress):
            hostname, ips = None, (ip_or_hostname,)
        else:
            hostname, ips = ip_or_hostname
            print(f"Hostname {hostname} has {len(ips)} IP address(es):")

        for ip in ips:
            matched = False
            for name, cr in clouds.items():
                matches = cr.check(ip)
                for ii, match in enumerate(matches):
                    if not matched:
                        matched = True
                    if ii==0:
                        print(f"IP address {ip} belongs to cloud provider {name}:")
                    if args.pretty:
                        pprint(match)
                    else:
                        print('\t' + repr(match))
            if not matched:
                print(f"IP address {ip} not found in any public cloud range.")
            print()

########################################

if __name__=='__main__':
    main()
