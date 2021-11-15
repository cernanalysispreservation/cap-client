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
"""Metadata API class."""

import json

from click import UsageError
from future.moves.urllib.parse import urljoin

from .base import CapAPI


class MetadataAPI(CapAPI):
    """Interface for CAP metadata methods."""

    def get(self, pid, field=None):
        """Get metadata for analysis with given PID.

        :param pid: analysis PID
        :type pid: str
        :param field: get specific field, eg. obj.nested_arr.0
        :type field: str, optional
        :return: metadata field's object|value
        :rtype: JSON serializable object
        """
        metadata = self._make_request(
            url=urljoin('deposits/', pid),
            headers={'Accept': 'application/basic+json'},
        )['metadata']

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

    def set(self, pid, value, field=None):
        """Update analysis metadata.

        :param pid: analysis PID
        :type pid: str
        :param value: value to set
        :type value: JSON serializable object
        :param field: set specific field, eg. obj.nested_arr.0
        :type field: str, optional
        :return: updated analysis metadata
        :rtype: dict
        """
        if field:  # use JSON patch to patch fields
            res = self._make_request(
                url=urljoin('deposits/', pid),
                method='patch',
                headers={
                    'Content-Type': 'application/json-patch+json',
                    'Accept': 'application/basic+json'
                },
                data=json.dumps([{
                    "op": "replace",
                    "path": '/' + field.replace('.', '/'),
                    "value": value,
                }]))
        else:  # use PUT request to update the whole object
            if not isinstance(value, dict):
                raise UsageError('Not a JSON object.')

            res = self._make_request(
                url=urljoin('deposits/', pid),
                method='put',
                headers={
                    'Content-Type': 'application/json',
                    'Accept': 'application/basic+json'
                },
                data=json.dumps(value),
            )

        return res

    def remove(self, pid, field):
        """Remove metadata field for analysis with given PID.

        :param pid: analysis PID
        :type pid: str
        :param field: field name, eg. obj.nested_arr.0
        :type field: str, optional
        :return: updated analysis metadata
        :rtype: dict
        """
        response = self._make_request(
            url=urljoin('deposits/', pid),
            method='patch',
            data=json.dumps([
                {
                    "op": "remove",
                    "path": '/' + field.replace('.', '/')
                },
            ]),
            headers={
                'Content-Type': 'application/json-patch+json',  # noqa
                'Accept': 'application/basic+json'
            })

        return response['metadata']
