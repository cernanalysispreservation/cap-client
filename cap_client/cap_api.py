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

import datetime
import json
import os
from urlparse import urljoin

import click
import requests
import urllib3

from cap_client.errors import StatusCodeException, UnknownAnalysisType
from utils import make_tarfile

# @TOFIX
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


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
                                    url=url)

    def _make_request(self,
                      url=None,
                      method='get',
                      expected_status_code=200,
                      headers={'Content-type': 'application/json'},
                      **kwargs):

        endpoint = self._construct_endpoint(url=url)

        params = {'access_token': self.access_token}
        method_obj = getattr(requests, method)
        response = method_obj(url=endpoint,
                              verify=False,
                              params=params,
                              headers=headers,
                              **kwargs)
        try:
            response_data = response.json()
        except ValueError:
            response_data = None

        if response.status_code == expected_status_code:
            return response_data
        else:
            raise StatusCodeException(
                endpoint=endpoint,
                expected_status_code=expected_status_code,
                status_code=response.status_code,
                data=response_data)

    def _get_available_types(self):
        """Get available analyses types from server."""
        ana_types = self._make_request(url='me')

        return [exp['deposit_group'] for exp in
                ana_types['deposit_groups']]

    def _get_permissions_data(self, rights, email, operation=None):
        """Get data for setting/removing permissions."""
        permissions = [{'action': 'deposit-{}'.format(r),
                        'op': operation} for r in rights]
        data = {
            "permissions": [
                {
                    "type": "user",
                    "identity": "{}".format(email),
                    "permissions": permissions
                }
            ]
        }

        return data

    def ping(self):
        """Health check CAP Server."""
        return self._make_request(url='ping')

    def me(self):
        """Retrieve user info."""
        response = self._make_request(url='me')

        return {x: response[x] for x in ('id',
                                         'collaborations',
                                         'email')}

    def get(self, pid=None, all=False):
        """Retrieve one or all analyses from a user."""
        headers = {} if not pid else {'Accept': 'application/basic+json'}

        if pid or all:
            url = urljoin('deposits/', pid)
        else:
            user_id = self.me().get('id', '')
            url = urljoin('deposits/', '?q=_deposit.created_by:{}'.format(
                user_id))

        response = self._make_request(url=url, headers=headers)

        return response if pid else response['hits']['hits']

    def get_metadata(self, pid, field=None):
        """Return metadata on analysis."""
        dct = self._make_request(url=urljoin('deposits/', pid),
                                 headers={
                                     'Accept': 'application/basic+json'
                                 })
        dct = dct["metadata"]
        fields = field.split('.') if field else []
        for x in fields:
            dct = dct[x or int(x)]
        return dct

    def get_permissions(self, pid):
        """Return deposit user permissions."""
        return self._make_request(url=urljoin('deposits/', pid),
                                  headers={
                                      'Accept': 'application/permissions+json'
                                  })

    def add_permissions(self, pid=None, email=None,
                        rights=None):
        """Assigns access right to users in a deposit."""
        data = self._get_permissions_data(rights, email, operation='add')
        url = urljoin('deposits/', pid + '/actions/permissions')
        return self._make_request(url=url,
                                  data=json.dumps(data),
                                  method='post',
                                  expected_status_code=201,
                                  headers={
                                      'Content-type': 'application/json',
                                      'Accept': 'application/permissions+json'
                                  })

    def remove_permissions(self, pid=None, email=None,
                           rights=None):
        """Removes access right to users in a deposit."""
        data = self._get_permissions_data(rights, email, operation='remove')
        url = urljoin('deposits/', pid + '/actions/permissions')
        return self._make_request(url=url,
                                  data=json.dumps(data),
                                  method='post',
                                  expected_status_code=201,
                                  headers={
                                      'Content-type': 'application/json',
                                      'Accept': 'application/permissions+json'
                                  })

    def remove_field(self, field_name, pid):
        """Remove analysis field."""
        json_data = [{
            "op": "remove",
            "path": '/{}'.format(field_name.replace('.', '/'))
        }]

        response = self._make_request(url=urljoin('deposits/', pid),
                                      data=json.dumps(json_data),
                                      method='patch',
                                      headers={
                                          'Content-Type': 'application/json-patch+json',  # noqa
                                          'Accept': 'application/basic+json'
                                      })
        return response['metadata']

    def remove_field(self, field_name, pid):
        """Remove analysis field."""

        json_data = [{
            "op": "remove",
            "path": '/{}'.format(field_name.replace('.', '/'))
        }]

        headers = {'Content-Type': 'application/json-patch+json',
                   'Accept': 'application/basic+json'}

        response = self._make_request(url=urljoin('deposits/', pid),
                                      data=json.dumps(json_data),
                                      method='patch',
                                      headers=headers)
        return response['data']['metadata']

    def set(self, field_name, field_val, pid, filepath=None, append=False):
        """Edit analysis field value."""
        try:
            val = json.loads(field_val)
        except ValueError:
            val = field_val

        json_data = [{
            "op": "add",
            "path": '/{}{}'.format(field_name.replace('.', '/'),
                                   '/-' if append else ''),
            "value": val,
        }]

        if filepath:
            self.upload(pid, filepath, field_val)

        response = self._make_request(url=urljoin('deposits/', pid),
                                      data=json.dumps(json_data),
                                      method='patch',
                                      headers={
                                          'Content-Type': 'application/json-patch+json',  # noqa
                                          'Accept': 'application/basic+json'
                                      })
        return response['metadata']

    def create(self, json_='', ana_type=None, version='0.0.1'):
        """Create an analysis."""
        types = self._get_available_types()

        if ana_type not in types:
            raise UnknownAnalysisType(types)

        try:
            data = json.loads(json_)
        except ValueError:
            with open(json_) as fp:
                data = json.load(fp)

        data['$ana_type'] = ana_type
        json_data = json.dumps(data)

        self._make_request(url='deposit/validator',
                           method='post',
                           data=json_data)

        return self._make_request(url='deposits/',
                                  method='post',
                                  data=json_data,
                                  expected_status_code=201,
                                  headers={
                                      'Content-Type': 'application/json',
                                      'Accept': 'application/basic+json'
                                  })

    def delete(self, pid=None):
        """Delete an analysis by given pid."""
        return self._make_request(url=urljoin('deposits/', pid),
                                  method='delete',
                                  expected_status_code=204)

    def update(self, pid=None, filename=''):
        """Update an analysis by given pid and JSON data from file."""
        try:
            data = json.loads(filename)
        except ValueError:
            with open(filename) as fp:
                data = json.load(fp)

        json_data = json.dumps(data)

        self._make_request(url='deposit/validator',
                           method='post',
                           data=json_data)

        return self._make_request(url=urljoin('deposits/', pid),
                                  data=json_data,
                                  method='put')

    def patch(self, pid=None, filename=''):
        """Patch an analysis by given pid and JSON-patch data from file."""
        try:
            data = json.loads(filename)
        except ValueError:
            with open(filename) as fp:
                data = json.load(fp)

        json_data = json.dumps(data)

        return self._make_request(url=urljoin('deposits/', pid),
                                  data=json_data,
                                  method='patch',
                                  headers={
                                      'Content-Type': 'application/json-patch+json'  # noqa
                                  })

    def get_files(self, pid):
        return self._make_request(url='deposits/{}/files'.format(pid))

    def upload(self, pid=None, filepath=None, yes=False, output_filename=None):
        """Upload file or directory to deposit by given pid."""
        try:
            deposit = self._make_request(url='deposits/{}'.format(pid))
        except Exception as e:
            return {"error": e}

        bucket_url = deposit.get("links", {}).get("bucket", None)
        bucket_id = bucket_url.split("/")[-1:][0]

        # Check if filepath is file or DIR
        if os.path.isdir(filepath):
            # If it's a DIR alert that it is going to be tarballed
            # and uploaded
            if yes or \
                    click.confirm('You are trying to upload a directory.\n'
                                  'Should we upload '
                                  'a tarball of the directory?'):
                if output_filename is None:
                    output_filename = "{pid}_{bucket_id}_{time}.tar.gz".format(
                        pid=pid,
                        bucket_id=bucket_id,
                        time=datetime.datetime.now().strftime(
                            '%b-%d-%I%M%p-%G')
                    )
                make_tarfile(output_filename, filepath)
                filepath = output_filename
        else:
            if output_filename is None:
                output_filename = os.path.basename(filepath)

        # data = {'filename': output_filename}
        return self._make_request(
            url="files/{bucket_id}/{filename}".format(
                bucket_id=bucket_id,
                filename=output_filename),
            data=open(filepath, 'rb'),
            method='put',
        )

    def types(self):
        """Get available analyses types."""
        return self._get_available_types()

    def publish(self, pid):
        return self._make_request(url='deposits/{}/actions/publish'.format(pid),
                                  expected_status_code=202,
                                  method='post',
                                  headers={'Content-Type': 'application/json',
                                           'Accept': 'application/basic+json'})
