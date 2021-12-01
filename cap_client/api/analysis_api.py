# -*- coding: utf-8 -*-
#
# This file is part of CERN Analysis Preservation Framework.
# Copyright (C) 2020 CERN.
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
"""Analysis API class."""

import json

from click import UsageError
from future.moves.urllib.parse import urljoin, urlencode

from cap_client.errors import BadStatusCode

from .base import CapAPI


class AnalysisAPI(CapAPI):
    """Interface for CAP analysis methods."""

    def _param_encoder(self, all, query, search, type, sort, page, size):
        """Return the encoded string of parameters.

        :param all: show all (not only created by user)
        :type all: bool
        :param type: type of analysis
        :type type: string
        :param query: free text query in analyses
        :type query: string
        :param search: search in facets
        :type search: string
        :param sort: sort analysis
        :type sort: string
        :param page: show results on specified page
        :type page: integer
        :param size: number of results on a page
        :type size: integer
        :return: string of encoded parameters
        :rtype: string
        """
        params = {}
        if not all:
            params["by_me"] = True
        if type:
            params["type"] = type
        if query:
            params["q"] = query
        if sort:
            params["sort"] = sort
        if page:
            params["page"] = page
        if size:
            params["size"] = size
        if search:
            for search_param in search:
                _search = search_param.split('=')
                params[_search[0]] = _search[-1]
        return urlencode(params)

    def get_drafts(
            self,
            all=False,
            query='',
            search=None,
            type=None,
            sort=None,
            page=None,
            size=None):
        """Get list of user's draft analyses.

        :param all: show all (not only created by user)
        :type all: bool
        :param type: type of analysis
        :type type: string
        :param query: free text query in analyses
        :type query: string
        :param search: search in facets
        :type search: string
        :param sort: sort analysis
        :type sort: string
        :param page: show results on specified page
        :type page: integer
        :param size: number of results on a page
        :type size: integer
        :return: list of analyses
        :rtype: list
        """
        response = self._make_request(
            url='deposits/?{}'.format(self._param_encoder(all, query, search, type, sort, page, size)),
            headers={'Accept': 'application/basic+json'},
        )

        return response['hits']['hits']

    def get_draft_by_pid(self, pid):
        """Get draft analysis.

        :param pid: analysis PID
        :type pid: str
        :return: draft analysis
        :rtype: dict
        """
        response = self._make_request(
            url=urljoin('deposits/', pid),
            headers={'Accept': 'application/basic+json'},
        )

        return response

    def get_published(
            self,
            all=False,
            query='',
            search=None,
            type=None,
            sort=None,
            page=None,
            size=None):
        """Get list of user's published analyses.

        :param all: show all (not only created by user)
        :type all: bool
        :param type: type of analysis
        :type type: string
        :param query: free text query in analyses
        :type query: string
        :param search: search in facets
        :type search: string
        :param sort: sort analysis
        :type sort: string
        :param page: show results on specified page
        :type page: integer
        :param size: number of results on a page
        :type size: integer
        :return: list of analysis
        :rtype: list
        """
        response = self._make_request(
            url='records/?{}'.format(self._param_encoder(all, query, search, type, sort, page, size)),
            headers={'Accept': 'application/basic+json'},
        )

        return response['hits']['hits']

    def get_published_by_pid(self, pid):
        """Get published analysis.

        :param pid: analysis PID
        :type pid: str
        :return: published analysis
        :rtype: dict
        """
        response = self._make_request(
            url=urljoin('records/', pid),
            headers={'Accept': 'application/basic+json'},
        )

        return response

    def create(self, data, type_=None):
        """Create new analysis.

        :param data: analysis metadata (JSON serializable)
        :type data: dict
        :param type: analysis type
        :type type: str, optional
        :return: newly created draft analysis
        :rtype: dict
        """
        if not isinstance(data, dict):
            raise UsageError('Not a JSON object.')

        if data.get('$schema'):
            if type_:
                raise UsageError(
                    'Your JSON data already provides $schema - --type/-t parameter forbidden.'  # noqa
                )
        elif type_:
            data['$ana_type'] = type_
        else:
            raise UsageError('You need to provide the --type/-t parameter'
                             ' OR add $schema field in your JSON data.')

        res = self._make_request(
            url='deposits/',
            method='post',
            data=json.dumps(data),
            expected_status_code=201,
        )

        return self._make_request(
            url=urljoin('deposits/', res['id']),
            data=json.dumps(res['metadata']),
            expected_status_code=200,
            method='put',
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/basic+json'
            },
        )

    def delete(self, pid):
        """Delete draft analysis.

        :param pid: analysis PID
        :type pid: str
        """
        self._make_request(
            url=urljoin('deposits/', pid),
            method='delete',
            expected_status_code=204,
        )

    def update(self, pid, data):
        """Update analysis metadata.

        :param pid: analysis PID
        :type pid: str
        :param data: analysis metadata (JSON serializable)
        :type data: dict
        :return: updated analysis
        :rtype: dict
        """
        if not isinstance(data, dict):
            raise UsageError('Not a JSON object.')

        return self._make_request(
            url=urljoin('deposits/', pid),
            method='put',
            headers={
                'Accept': 'application/basic+json',
                'Content-Type': 'application/json'
            },
            data=json.dumps(data),
        )

    def patch(self, pid, data):
        """Patch analysis metadata with data in JSON Patch format.

        :param pid: analysis PID
        :type pid: str
        :param data: analysis metadata (JSON Patch compliant)
        :type data: dict
        :return: updated analysis
        :rtype: dict
        """
        if type(data) not in [list, dict]:
            raise UsageError('Not a JSON object or array.')

        res = self._make_request(
            url=urljoin('deposits/', pid),
            method='patch',
            headers={
                'Content-Type': 'application/json-patch+json',
                'Accept': 'application/basic+json'
            },
            data=json.dumps(data),
        )

        return res

    def publish(self, pid):
        """Publish draft analysis.

        :param pid: analysis PID
        :type pid: str
        :return: PID of published analysis
        :rtype: str
        """
        res = self._make_request(
            url='deposits/{}/actions/publish'.format(pid),
            method='post',
            expected_status_code=202,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/basic+json'
            },
        )

        return res.get('recid')

    def get_schema_types(self):
        """Get available analyses types."""
        res = self._make_request(url='me')

        return [exp['deposit_group'] for exp in res['deposit_groups']]

    def get_schema(self, type_, version=None, record_schema=False):
        """Get JSON schema for given analysis type.

        :param type_: analysis type
        :type type_: str
        :param version: schema version
        :type version: str, optional
        :param record_schema: get schema for published analysis
        (draft by default)
        :type record_schema: bool, optional
        :return: JSON schema
        :rtype: dict
        """
        if version:
            url = 'jsonschemas/{}/{}?resolve=True'.format(type_, version)
        else:  # return latest version of schema
            url = 'jsonschemas/{}?resolve=True'.format(type_)

        try:
            res = self._make_request(url=url)
        except BadStatusCode as e:
            if e.status_code == 404:
                e.message = 'Schema {}{} does not exist.'.format(
                    type_, '.v' + version if version else '')
                raise e

        schema = res['record_schema'] if record_schema else res[
            'deposit_schema']

        schema['properties'] = {
            k: v
            for k, v in schema.get('properties', {}).items()
            if not k.startswith('_')
        }

        return schema
