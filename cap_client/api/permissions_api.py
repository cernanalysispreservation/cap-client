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
"""Permissions API class."""

import json

from future.moves.urllib.parse import urljoin

from .base import CapAPI


class PermissionsAPI(CapAPI):
    """Interface for CAP permissions methods."""

    def get(self, pid):
        """List permissions for analysis.

        :param pid: analysis PID
        :type pid: str
        :return: list of users/egroups with access to analysis
        :rtype: dict
        """
        res = self._make_request(
            url=urljoin('deposits/', pid),
            headers={'Accept': 'application/permissions+json'})

        return res.get('permissions')

    def add(self, pid, email, rights, is_egroup=False):
        """Give user permissions to analysis.

        :param pid: analysis PID
        :type pid: str
        :param email: user|egroup email
        :type email: str
        :param rights: list of rights (read|update|admin)
        :type rights: list(str)
        :param is_egroup: permissions for egroup or user
        :type is_egroup: bool
        :return: updated permissions
        :rtype: dict
        """
        data = self._construct_permission(email,
                                          "add",
                                          rights,
                                          is_egroup=is_egroup)
        res = self._make_request(
            url='deposits/{}/actions/permissions'.format(pid),
            method='post',
            expected_status_code=201,
            headers={
                'Content-type': 'application/json',
                'Accept': 'application/permissions+json'
            },
            data=json.dumps(data),
        )

        return res.get('permissions')

    def remove(self, pid, email, rights, is_egroup=False):
        """Revoke user permissions to analysis.

        :param pid: analysis PID
        :type pid: str
        :param email: user|egroup email
        :type email: str
        :param rights: list of rights (read|update|admin)
        :type rights: list(str)
        :param is_egroup: permissions for egroup or user
        :type is_egroup: bool
        :return: updated permissions
        :rtype: dict
        """
        data = self._construct_permission(email,
                                          "remove",
                                          rights,
                                          is_egroup=is_egroup)
        res = self._make_request(
            url='deposits/{}/actions/permissions'.format(pid),
            method='post',
            expected_status_code=201,
            headers={
                'Content-type': 'application/json',
                'Accept': 'application/permissions+json'
            },
            data=json.dumps(data),
        )

        return res.get('permissions')

    def _construct_permission(self, email, operation, rights, is_egroup=False):
        return [{
            "email": email,
            "type": "egroup" if is_egroup else "user",
            "op": operation,
            "action": "deposit-{}".format(right)
        } for right in rights]
