# -*- coding: utf-8 -*-
#
# This file is part of CERN Analysis Preservation Framework.
# Copyright (C) 2017 CERN.
#
# CERN Analysis Preservation Framework is free software; you can redistribute
# it and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# CERN Analysis Preservation Framework is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CERN Analysis Preservation Framework; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.
"""CAP client"""

import os
import re

from setuptools import find_packages, setup

readme = open('README.rst').read()
history = open('CHANGES.rst').read()

tests_require = [
    'check-manifest>=0.51',
    'coverage>=7.13.5',
    'mock>=5.2.0',
    'pydocstyle>=6.3.0',
    'pytest-cache>=1.0',
    'pytest-cov>=7.0.0',
    'flake8>=7.3.0',
    'pytest>=9.0.2',
    'responses>=0.26.0',
    'pytest-vcr>=1.0.2',
]

extras_require = {
    'docs': [
        'Sphinx>=7.2.0',
        'sphinx-rtd-theme>=2.0.0',
    ],
    'tests': tests_require,
}

extras_require['all'] = []
for key, reqs in extras_require.items():
    if ':' == key[0]:
        continue
    extras_require['all'].extend(reqs)

install_requires = [
    'click>=8.3.1',
    'click-help-colors>=0.9.4',
    'requests>=2.32.5',
    'colorama>=0.4.6',
    'future>=1.0.0',
]

packages = find_packages()

# Get the version string. Cannot be done with import!
with open(os.path.join('cap_client', 'version.py'), 'rt') as f:
    version = re.search('__version__\\s*=\\s*"(?P<version>.*)"\\n',
                        f.read()).group('version')

setup(
    name='cap_client',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    author='CAP',
    author_email='info@cap.io',
    url='https://github.com/cernanalysispreservation/cap-client',
    packages=packages,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'cap-client = cap_client.cli:cli',
        ],
    },
    install_requires=install_requires,
    extras_require=extras_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Development Status :: 3 - Alpha',
    ],
)
