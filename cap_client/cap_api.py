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

import json
import requests

from errors import StatusCodeException


class CapAPI(object):
    """CAP API client code."""

    def __init__(self, server_url, apipath, access_token):
        """Initialize CapAPI object."""
        self.server_url = server_url
        self.apipath = apipath
        self.access_token = access_token
        self.endpoint = '{server_url}/{apipath}/{url}'

    def _construct_endpoint(self, url=None):
        """Construct api endpoint."""
        return self.endpoint.format(server_url=self.server_url,
                                    apipath=self.apipath,
                                    url=url, )

    def _make_request(self,
                      url=None,
                      method='get',
                      expected_code=200,
                      **kwargs):
        endpoint = self._construct_endpoint(url=url)

        params = {'access_token': self.access_token}
        headers = {'Content-type': 'application/json'}
        method_obj = getattr(requests, method)
        response = method_obj(endpoint,
                              verify=False,
                              params=params,
                              headers=headers,
                              **kwargs)
        if response.status_code == expected_code:
            try:
                data = response.json()
            except ValueError:
                data = None
            return {'status': response.status_code,
                    'data': data}
        else:
            raise StatusCodeException(expected_code=expected_code,
                                      status_code=response.status_code,
                                      endpoint=endpoint,
                                      data=response.json())

    def _get_available_types(self):
        """Get available analyses types from server."""
        ana_types = self._make_request(url='me').get('data', {})
        try:
            return [exp['deposit_group'] for exp in
                    ana_types['deposit_groups']]
        except KeyError as e:
            raise e

    def ping(self):
        """Health check CAP Server."""
        return self._make_request(url='ping')

    def get(self, pid=None):
        """Retrieve one or all analyses from a user."""
        return self._make_request(url=urljoin('deposits/', pid))

    def create(self, data=None, type=None, version='0.0.1'):
        """Create an analysis."""
        types = self._get_available_types()
        if type not in types:
            return "Choose one of the available analyses types:\n{}".format(
                '\n'.join(types)
            )

        with open(data) as fp:
            data = json.load(fp)
            data['$ana_type'] = type

        try:
            self._make_request(url='deposit/validator',
                               method='post',
                               data=json.dumps(data)
                               )
        except StatusCodeException as e:
            return e.data['errors']

        response = self._make_request(url='deposits/',
                                      method='post',
                                      data=json.dumps(data),
                                      expected_code=201)

        return json.dumps(response, indent=4)

    def delete(self, pid=None):
        """"Delete an analysis by given pid."""
        return self._make_request(url=urljoin('deposits/', pid),
                                  method='delete',
                                  expected_code=204)

    def update(self, pid=None, data=None):
        """"Update an analysis by given pid and data."""
        with open(data) as fp:
            data = json.load(fp)

        return self._make_request(url=urljoin('deposits/', pid),
                                  data=json.dumps(data),
                                  method='put',
                                  expected_code=200)

    def types(self):
        """"Get available analyses types."""
        return self._get_available_types()
