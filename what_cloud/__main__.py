#!/usr/bin/env python3

import logging
import argparse
import ipaddress
import requests
import os
from itertools import chain

from .aws import AWSCloud
from .azure import AzureCloud

logging.basicConfig(level=logging.INFO)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('-v','--verbose', default=0, action='count')
    p.add_argument('ip', type=ipaddress.ip_address, nargs='+', help='IPv4 or IPv6 address')
    args = p.parse_args()

    session = requests.session()

    clouds = dict(
        AWS = AWSCloud(session=session),
        AZure = AzureCloud(session=session),
    )

    for ip in args.ip:
        matched = False
        for name, cr in clouds.items():
            matches = cr.check(ip)
            for ii, match in enumerate(matches):
                if not matched:
                    matched = True
                if ii==0:
                    print("IP address {} belongs to {} cloud:".format(ip, name))
                print('\t' + repr(match))
        if not matched:
            print("IP address {} not found in any public cloud range.".format(ip))

########################################

if __name__=='__main__':
    main()
