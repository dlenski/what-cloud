#!/usr/bin/env python3

import sys, os
try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

if not sys.version_info[0] == 3:
    sys.exit("Python 2.x is not supported; Python 3.x is required.")

########################################

version_py = os.path.join('what_cloud', 'version.py')

d = {}
with open(version_py, 'r') as fh:
    exec(fh.read(), d)
    version_pep = d['__version__']

########################################

setup(name="what-cloud",
      version=version_pep,
      description="Identify servers running in various clouds",
      long_description=open("description.rst").read(),
      author="Daniel Lenski",
      author_email="dlenski@gmail.com",
      license='GPL v3 or later',
      install_requires=[ open("requirements.txt").readlines() ],
      url="https://github.com/dlenski/what-cloud",
      packages = ['what_cloud'],
      entry_points={ 'console_scripts': [ 'what-cloud=what_cloud.__main__:main' ] },
      test_suite='nose.collector',
      )
