[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Build Status](https://api.travis-ci.org/dlenski/what-cloud.png)](https://travis-ci.org/dlenski/what-cloud)
[![PyPI](https://img.shields.io/pypi/v/what-cloud.svg)](https://pypi.python.org/pypi/what-cloud)

# what-cloud

Identifies servers running in various public clouds. Currently it can recognize…

* AWS
* Azure
* Google

## Install

Requires Python 3, `pip`, and [`requests`](https://docs.python-requests.org):

```sh
$ pip3 install https://github.com/dlenski/what-cloud/archive/master.zip
...
$ what_cloud --help
usage: __main__.py [-h] [-v] [-p] ip [ip ...]

positional arguments:
  ip             IPv4 or IPv6 address

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose
  -p, --pretty
```

## Examples

```
$ what_cloud 208.86.91.234
IP address 208.86.91.234 belongs to cloud provider AWS:
	{'ip_prefix': IPv4Network('208.86.90.0/23'), 'region': 'eu-west-1', 'service': 'AMAZON', 'network_border_group': 'eu-west-1'}
	{'ip_prefix': IPv4Network('208.86.90.0/23'), 'region': 'eu-west-1', 'service': 'EC2', 'network_border_group': 'eu-west-1'}
```

```
$ what_cloud 20.37.64.123 51.4.144.99
IP address 20.37.64.123 belongs to cloud provider Azure:
	{'changeNumber': 111, 'cloud': 'Public', 'values': [{'name': 'PowerBI', 'id': 'PowerBI', 'properties': {'changeNumber': 3, 'region': '', 'regionId': 0, 'platform': 'Azure', 'systemService': 'PowerBI', 'addressPrefixes': [IPv4Network('20.37.64.122/31')], 'networkFeatures': ['NSG', 'UDR', 'FW']}}]}
	{'changeNumber': 111, 'cloud': 'Public', 'values': [{'name': 'AzureCloud.uaecentral', 'id': 'AzureCloud.uaecentral', 'properties': {'changeNumber': 8, 'region': 'uaecentral', 'regionId': 61, 'platform': 'Azure', 'systemService': '', 'addressPrefixes': [IPv4Network('20.37.64.0/19')], 'networkFeatures': ['API', 'NSG']}}]}
	{'changeNumber': 111, 'cloud': 'Public', 'values': [{'name': 'AzureCloud', 'id': 'AzureCloud', 'properties': {'changeNumber': 48, 'region': '', 'regionId': 0, 'platform': 'Azure', 'systemService': '', 'addressPrefixes': [IPv4Network('20.37.64.0/19')], 'networkFeatures': ['API', 'NSG']}}]}

IP address 51.4.144.99 belongs to cloud provider Azure:
	{'changeNumber': 112, 'cloud': 'AzureGermany', 'values': [{'name': 'ServiceFabric', 'id': 'ServiceFabric', 'properties': {'changeNumber': 1, 'region': '', 'regionId': 0, 'platform': 'Azure', 'systemService': 'ServiceFabric', 'addressPrefixes': [IPv4Network('51.4.144.99/32')], 'networkFeatures': ['API', 'NSG', 'UDR', 'FW']}}]}
	{'changeNumber': 112, 'cloud': 'AzureGermany', 'values': [{'name': 'ServiceFabric.GermanyCentral', 'id': 'ServiceFabric.GermanyCentral', 'properties': {'changeNumber': 1, 'region': 'germanycentral', 'regionId': 5, 'platform': 'Azure', 'systemService': 'ServiceFabric', 'addressPrefixes': [IPv4Network('51.4.144.99/32')], 'networkFeatures': None}}]}
	{'changeNumber': 112, 'cloud': 'AzureGermany', 'values': [{'name': 'AzureCloud.germanycentral', 'id': 'AzureCloud.germanycentral', 'properties': {'changeNumber': 8, 'region': 'germanycentral', 'regionId': 5, 'platform': 'Azure', 'systemService': '', 'addressPrefixes': [IPv4Network('51.4.128.0/17')], 'networkFeatures': ['API', 'NSG']}}]}
	{'changeNumber': 112, 'cloud': 'AzureGermany', 'values': [{'name': 'AzureCloud', 'id': 'AzureCloud', 'properties': {'changeNumber': 9, 'region': '', 'regionId': 0, 'platform': 'Azure', 'systemService': '', 'addressPrefixes': [IPv4Network('51.4.128.0/17')], 'networkFeatures': ['API', 'NSG']}}]}
```

```
$ what_cloud 2600:1901::1234 8.8.8.8
IP address 2600:1901::1234 belongs to cloud provider Google:
	{'ipv6Prefix': IPv6Network('2600:1901::/48'), 'service': 'Google Cloud', 'scope': 'global'}
	{'ipv6Prefix': IPv6Network('2600:1900::/28'), 'service': 'Google'}

IP address 8.8.8.8 belongs to cloud provider Google:
	{'ipv4Prefix': IPv4Network('8.8.8.0/24'), 'service': 'Google'}
```

## TODO

* More clouds
* Standardize output across clouds?
* Condense output for IPs that belong to multiple ranges?

## License

GPLv3 or later
