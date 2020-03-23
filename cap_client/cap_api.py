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

import requests
import urllib3
from click import BadParameter, UsageError, confirm
from future.moves.urllib.parse import urljoin

from .errors import BadStatusCode, DepositCreationError
from .utils import make_tarfile

# @TOFIX
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class CapAPI(object):
    """CAP API client code."""
    def __init__(self, server_url, apipath, access_token):
        """Initialize CapAPI object."""
        self.server_url = server_url
        self.api = urljoin(server_url, apipath)
        self.access_token = access_token

    def _make_request(self,
                      url=None,
                      method='get',
                      expected_status_code=200,
                      headers={'Content-type': 'application/json'},
                      stream=False,
                      **kwargs):

        endpoint = urljoin(self.api, url)
        method_obj = getattr(requests, method)
        headers.update(
            {'Authorization': 'OAuth2 {}'.format(self.access_token)})

        response = method_obj(url=endpoint,
                              verify=False,
                              headers=headers,
                              stream=stream,
                              **kwargs)

        if response.status_code != expected_status_code:
            try:
                data = response.json()
                msg = data.get('message')
            except ValueError:
                data = msg = response.text

                if response.status_code == 500:
                    msg = 'The server encountered an unexpected error. Try again soon.\nIn case the error persists, please contact the server administrators.'  # noqa

            raise BadStatusCode(msg, endpoint, expected_status_code,
                                response.status_code, data)

        if stream:
            return response
        else:
            try:
                return response.json()
            except ValueError:
                return response.text

    def _get_available_types(self):
        """Get available analyses types from server."""
        ana_types = self._make_request(url='me')

        return [exp['deposit_group'] for exp in ana_types['deposit_groups']]

    def _get_permissions_data(self, rights, email, operation=None):
        """Get data for setting/removing permissions."""
        return [{
            "email": email,
            "type": "user",
            "op": operation,
            "action": "deposit-{}".format(right)
        } for right in rights]

    def me(self):
        """Retrieve user info."""
        response = self._make_request(url='me')
        return {x: response[x] for x in ('id', 'email')}

    def types(self):
        """Get available analyses types."""
        return self._get_available_types()

    ##############
    # CRUD
    ##############
    def get_drafts(self, all=False):
        """Retrieve user drafts."""
        url = 'deposits/' if all else 'deposits/?q=&by_me=True'

        response = self._make_request(
            url=url, headers={'Accept': 'application/basic+json'})

        return response['hits']['hits']

    def get_draft_by_pid(self, pid):
        """Retrieve draft by pid."""
        url = urljoin('deposits/', pid)

        response = self._make_request(
            url=url, headers={'Accept': 'application/basic+json'})

        return response

    def get_shared(self, all=False):
        """Retrieve user published analysis."""
        url = 'records/' if all else 'records/?q=&by_me=True'

        response = self._make_request(
            url=url, headers={'Accept': 'application/basic+json'})

        return response['hits']['hits']

    def get_shared_by_pid(self, pid):
        """Retrieve one or all shared analyses from a user."""
        response = self._make_request(
            url=urljoin('records/', pid),
            headers={'Accept': 'application/basic+json'})

        return response

    def get_schema(self, ana_type=None, version=None, record=False):
        """Retrieve schema according to type of analysis."""
        url = 'jsonschemas/{}/{}?resolve=True'.format(ana_type, version) \
            if version \
            else 'jsonschemas/{}?resolve=True'.format(ana_type)

        resp = self._make_request(url=url)

        schema = resp['record_schema'] if record \
            else resp['deposit_schema']

        properties = {
            k: v
            for k, v in schema.get('properties', {}).items()
            if not k.startswith('_')
        }

        schema['properties'] = properties
        return schema

    def create(self, data, ana_type=None):
        """Create analysis."""
        if not isinstance(data, dict):
            raise UsageError('Not a JSON object.')

        if data.get('$schema'):
            if ana_type:
                raise UsageError(
                    'Your JSON data already provides $schema - --type/-t parameter forbidden.'  # noqa
                )
        elif ana_type:
            data['$ana_type'] = ana_type
        else:
            raise UsageError('You need to provide the --type/-t parameter'
                             ' OR add $schema field in your JSON data.')

        response = self._make_request(
            url='deposits/',
            method='post',
            data=json.dumps(data),
            expected_status_code=201,
        )

        return self._make_request(
            url=urljoin('deposits/', response['id']),
            data=json.dumps(response.get('metadata', {})),
            expected_status_code=200,
            method='put',
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/basic+json'
            },
        )

    def delete(self, pid=None):
        """Delete an analysis by given pid."""
        self._make_request(url=urljoin('deposits/', pid),
                           method='delete',
                           expected_status_code=204)

    def update(self, pid, data):
        """Update an analysis by given pid and JSON data from file."""
        if not isinstance(data, dict):
            raise UsageError('Not a JSON object.')

        return self._make_request(url=urljoin('deposits/', pid),
                                  data=json.dumps(data),
                                  method='put',
                                  headers={
                                      'Accept': 'application/basic+json',
                                      'Content-Type': 'application/json'
                                  })

    def patch(self, pid=None, filename=''):
        """Patch an analysis by given pid and JSON-patch data from file."""
        try:
            data = json.loads(filename)
        except ValueError:
            with open(filename) as fp:
                data = json.load(fp)

        res = self._make_request(
            url=urljoin('deposits/', pid),
            data=json.dumps(data),
            method='patch',
            headers={
                'Content-Type': 'application/json-patch+json'  # noqa
            })

        return res

    ##############
    # METADATA
    ##############
    def get_field(self, pid, field=None):
        """Return metadata on analysis."""
        metadata = self._make_request(
            url=urljoin('deposits/', pid),
            headers={'Accept': 'application/basic+json'})['metadata']

        fields = field.split('.') if field else []
        for x in fields:
            try:
                metadata = metadata[int(x) if x.isdigit() else x]
            except IndexError:
                raise UsageError(
                    'The index you are trying to access does not exist.')
            except (TypeError, KeyError):
                raise UsageError(
                    'The field {} does not exist. Try a different field.'.
                    format(x))

        return metadata

    def set_field(self, pid, field_name, field_val, filepath=None):
        """Edit analysis field value."""
        json_data = [{
            "op": "replace",
            "path": '/' + field_name.replace('.', '/'),
            "value": field_val,
        }]

        if filepath:
            self.upload_file(pid, filepath, field_val)

        response = self._make_request(
            url=urljoin('deposits/', pid),
            data=json.dumps(json_data),
            method='patch',
            headers={
                'Content-Type': 'application/json-patch+json',
                'Accept': 'application/basic+json'
            })

        return response['metadata']

    def remove_field(self, pid, field_name):
        """Remove analysis field."""
        json_data = [{
            "op": "remove",
            "path": '/{}'.format(field_name.replace('.', '/'))
        }]

        response = self._make_request(
            url=urljoin('deposits/', pid),
            data=json.dumps(json_data),
            method='patch',
            headers={
                'Content-Type': 'application/json-patch+json',  # noqa
                'Accept': 'application/basic+json'
            })
        return response['metadata']

    ##############
    # PERMISSIONS
    ##############
    def get_permissions(self, pid):
        """Return deposit user permissions."""
        return self._make_request(
            url=urljoin('deposits/', pid),
            headers={'Accept': 'application/permissions+json'})

    def add_permissions(self, pid=None, email=None, rights=None):
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

    def remove_permissions(self, pid=None, email=None, rights=None):
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

    ##############
    # FILES
    ##############

    def _get_bucket_id(self, pid):
        deposit = self._make_request(url='deposits/{}'.format(pid))
        return deposit['links']['bucket'].split("/")[-1:][0]

    def get_files(self, pid):
        return self._make_request(url='deposits/{}/files'.format(pid))

    def download_file(self, pid, filename, output_filename=None):
        bucket_id = self._get_bucket_id(pid)
        output = output_filename or filename

        response = self._make_request(
            url="files/{bucket_id}/{filename}".format(bucket_id=bucket_id,
                                                      filename=filename),
            method='get',
            stream=True)

        with open(output, 'wb') as f:
            f.write(response.content)

        return response

    def remove_file(self, pid, filename):
        bucket_id = self._get_bucket_id(pid)

        return self._make_request(url="files/{bucket_id}/{filename}".format(
            bucket_id=bucket_id, filename=filename),
                                  expected_status_code=204,
                                  method='delete')

    def upload_file(self,
                    pid=None,
                    filepath=None,
                    yes=False,
                    output_filename=None):
        """Upload file or directory to deposit by given pid."""
        bucket_id = self._get_bucket_id(pid)

        if os.path.isdir(filepath):
            # If it's a DIR alert that it is going to be tarballed
            # and uploaded
            if yes or \
                    confirm('You are trying to upload a directory.\n'
                            'Should we upload a tarball of the directory?'):
                if output_filename is None:
                    output_filename = "{pid}_{bucket_id}_{time}.tar.gz".format(
                        pid=pid,
                        bucket_id=bucket_id,
                        time=datetime.datetime.now().strftime(
                            '%b-%d-%I%M%p-%G'))
                make_tarfile(output_filename, filepath)
                filepath = output_filename
        else:
            if output_filename is None:
                output_filename = os.path.basename(filepath)

        return self._make_request(
            url="files/{bucket_id}/{filename}".format(
                bucket_id=bucket_id, filename=output_filename),
            data=open(filepath, 'rb'),
            method='put',
        )

    def publish(self, pid):
        return self._make_request(
            url='deposits/{}/actions/publish'.format(pid),  # noqa
            expected_status_code=202,
            method='post',
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/basic+json'
            })

    def clone(self, pid):
        return self._make_request(url='deposits/{}/actions/clone'.format(pid),
                                  expected_status_code=201,
                                  method='post',
                                  headers={
                                      'Content-Type': 'application/json',
                                      'Accept': 'application/basic+json'
                                  })

    ##############
    # REPOSITORIES
    ##############

    def upload_repository(self, pid, url, event_type=None):
        return self._make_request(url='deposits/{}/actions/upload'.format(pid),
                                  expected_status_code=201,
                                  method='post',
                                  data=json.dumps({
                                      'pid': pid,
                                      'url': url,
                                      'webhook': True if event_type else False,
                                      'event_type': event_type
                                  }),
                                  headers={
                                      'Content-Type': 'application/json',
                                      'Accept': 'application/repositories+json'
                                  })

    def get_repositories(self, pid, with_snapshots=False):
        response = self._make_request(
            url='deposits/{}'.format(pid),
            expected_status_code=200,
            method='get',
            headers={'Accept': 'application/repositories+json'})

        if not with_snapshots:
            for hook in response['webhooks']:
                hook.pop('snapshots')

        return response
