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
"""Base CAP API class."""

import os

import requests
import urllib3
from click import UsageError
from future.moves.urllib.parse import urljoin

from cap_client.errors import BadStatusCode

# @TOFIX
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

status_code_to_msg = {
    500: 'The server encountered an unexpected error. Try again soon.'
    'In case the error persists, please contact the server administrators.',
    401: 'You are not authorized to access the server (invalid access token?)',
    403: 'You don\'t have sufficient permissions.'
}


class CapAPI(object):
    """Base CAP interface class.

    Build your own API class on top of it, to handle requests to CAP server.
    """

    def __init__(self):
        """Initialize."""
        server_url = os.environ.get('CAP_SERVER_URL',
                                    'https://analysispreservation.cern.ch')
        apipath = os.environ.get('CAP_SERVER_API_PATH', 'api/')
        self.api = urljoin(server_url, apipath)
        try:
            self.access_token = os.environ['CAP_ACCESS_TOKEN']
        except KeyError:
            raise UsageError(
                'No personal access token provided.\n'
                'Try: export CAP_ACCESS_TOKEN=[TOKEN]\n\n'
                'If you do not have your token yet, login to the website and'
                'generate one from your account settings page.')

    def _make_request(self,
                      url,
                      method='get',
                      expected_status_code=200,
                      headers={'Content-type': 'application/json'},
                      stream=False,
                      **kwargs):
        """Make request to the CAP server.

        :param url: endpoint url eg. 'deposits/{pid}'
        :type url: str
        :param method: request method
        :type method: str, optional
        :param expected_status_code: status code expected on success
        :type expected_status_code: int, optional
        :param headers: request headers
        :type headers: dict, optional
        :param stream: request streamed response
        :type stream: bool, optional

        :raises BadStatusCode: when response status code
        different than expected

        :return: response data
        """
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
                data, msg = response.json(), None
            except ValueError:
                data = msg = response.text

            # use predefined messages
            msg = status_code_to_msg.get(response.status_code, msg)

            raise BadStatusCode(
                message=msg,
                expected_status_code=expected_status_code,
                status_code=response.status_code,
                endpoint=endpoint,
                data=data,
            )

        if stream:
            return response
        else:
            try:
                return response.json()
            except ValueError:
                return response.text
