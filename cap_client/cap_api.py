# -*- coding: utf-8 -*-
#
# This file is part of CERN Analysis Preservation Framework.
# Copyright (C) 2016, 2017 CERN.
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

"""CAP API Class."""

from urlparse import urljoin

import requests


class CapAPI(object):
    """CAP API client code."""

    def __init__(self, server_url, apipath='api', access_token=None):
        """Initialize ReanaAPI object."""
        self.server_url = server_url
        self.apipath = apipath
        self.access_token = access_token
        self.endpoint = '{server_url}/{apipath}/{url}'

    def construct_endpoint(self, url=None,):
        """Contruct api endpoint."""
        return self.endpoint.format(server_url=self.server_url,
                                    apipath=self.apipath,
                                    url=url,)

    def ping(self):
        """Health check CAP Server."""
        endpoint = self.construct_endpoint(url='ping')
        try:
            response = requests.get(endpoint, verify=False)

            if response.status_code == 200:
                return response.text
            else:
                raise Exception(
                    "Expected status code 200 but {endpoint} replied with "
                    "{status_code}".format(
                        status_code=response.status_code, endpoint=endpoint))

        except Exception:
            raise

    def get(self, pid=None):
        """Retrieve one or all analyses from a user."""
        endpoint = self.construct_endpoint(
            url=urljoin('deposits/', pid))
        try:
            params = {'access_token': self.access_token}
            response = requests.get(endpoint, verify=False, params=params)

            if response.status_code == 200:
                return response.text
            else:
                raise Exception(
                    "Expected status code 200 but {endpoint} replied with "
                    "{status_code}".format(
                        status_code=response.status_code, endpoint=endpoint))

        except Exception:
            raise
