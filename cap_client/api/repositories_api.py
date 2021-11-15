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
"""Repositories API class."""

import json

from future.moves.urllib.parse import urljoin

from .base import CapAPI


class RepositoriesAPI(CapAPI):
    """Interface for CAP repositories/webhooks methods."""

    def get(self, pid, with_snapshots=False):
        """Get list of repositories attached to analysis with given PID.

        :param pid: analysis PID
        :type pid: str
        :param with_snapshots: include snapshots informations
        :type with_snapshots: bool
        :return: list of repositories
        :rtype: list
        """
        response = self._make_request(
            url=urljoin('deposits/', pid),
            headers={'Accept': 'application/repositories+json'},
        )

        if not with_snapshots:
            for hook in response['webhooks']:
                hook.pop('snapshots')

        return response['webhooks']

    def upload(self, pid, url, event_type=None):
        """Get list of repositories attached to analysis with given PID.

        :param pid: analysis PID
        :type pid: str
        :param event_type: create webhook on this event
        :type event_type: str, optional
        :return: None
        """
        self._make_request(url='deposits/{}/actions/upload'.format(pid),
                           expected_status_code=201,
                           method='post',
                           headers={
                               'Content-Type': 'application/json',
                               'Accept': 'application/repositories+json'},
                           data=json.dumps({
                               'url': url,
                               'webhook': True if event_type else False,
                               'event_type': event_type
                           }))
