#!/usr/bin/env python3

import logging
import argparse
import ipaddress
import requests
import os
from itertools import chain
from pprint import pprint

from .aws import AWSCloud
from .azure import AzureCloud
from .google import GoogleCloud

logging.basicConfig(level=logging.INFO)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('-v','--verbose', default=0, action='count')
    p.add_argument('-p','--pretty', action='store_true')
    p.add_argument('ip', type=ipaddress.ip_address, nargs='+', help='IPv4 or IPv6 address')
    args = p.parse_args()

    session = requests.session()

    clouds = dict(
        AWS = AWSCloud(session=session),
        Azure = AzureCloud(session=session),
        Google = GoogleCloud(session=session),
    )

    for ip in args.ip:
        matched = False
        for name, cr in clouds.items():
            matches = cr.check(ip)
            for ii, match in enumerate(matches):
                if not matched:
                    matched = True
                if ii==0:
                    print("IP address {} belongs to cloud provider {}:".format(ip, name))
                if args.pretty:
                    pprint(match)
                else:
                    print('\t' + repr(match))
        if not matched:
            print("IP address {} not found in any public cloud range.".format(ip))
        print()

########################################

if __name__=='__main__':
    main()
