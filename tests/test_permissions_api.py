# -*- coding: utf-8 -*-
#
# This file is part of CERN Analysis Preservation Framework.
# Copyright (C) 2020, 2020 CERN.
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
"""Tests for Permissions API."""

from __future__ import absolute_import, print_function

import json

import responses
from pytest import raises

from cap_client.api.permissions_api import PermissionsAPI
from cap_client.errors import BadStatusCode


@responses.activate
def test_get_permissions():
    responses.add(
        responses.GET,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={
            'permissions': {
                'deposit-admin': {
                    'roles': [1],
                    'users': ['cms@inveniosoftware.org']
                },
                'deposit-read': {
                    'roles': [],
                    'users': ['cms@inveniosoftware.org']
                },
                'deposit-update': {
                    'roles': [],
                    'users': ['cms@inveniosoftware.org']
                }
            }
        },
        status=200)

    resp = PermissionsAPI().get('some-pid')

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/permissions+json'
    assert resp == {
        'deposit-admin': {
            'roles': [1],
            'users': ['cms@inveniosoftware.org']
        },
        'deposit-read': {
            'roles': [],
            'users': ['cms@inveniosoftware.org']
        },
        'deposit-update': {
            'roles': [],
            'users': ['cms@inveniosoftware.org']
        }
    }


@responses.activate
def test_add_permissions():
    responses.add(
        responses.POST,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid/actions/permissions',
        json={
            'permissions': {
                'deposit-admin': {
                    'roles': [],
                    'users': ['cms@inveniosoftware.org']
                },
                'deposit-read': {
                    'roles': [],
                    'users': [
                        'cms@inveniosoftware.org', 'cms2@inveniosoftware.org'
                    ]
                },
                'deposit-update': {
                    'roles': [],
                    'users': [
                        'cms@inveniosoftware.org', 'cms2@inveniosoftware.org'
                    ]
                }
            }
        },
        status=201)

    resp = PermissionsAPI().add(
        pid='some-pid',
        email='cms2@inveniosoftware.org',
        rights=['read', 'update'],
    )

    request = responses.calls[0].request
    assert request.headers['Accept'] == 'application/permissions+json'
    assert json.loads(request.body) == [{
        "email": "cms2@inveniosoftware.org",
        "type": "user",
        "op": "add",
        "action": "deposit-read"
    }, {
        "email": "cms2@inveniosoftware.org",
        "type": "user",
        "op": "add",
        "action": "deposit-update"
    }]

    assert resp == {
        'deposit-admin': {
            'roles': [],
            'users': ['cms@inveniosoftware.org']
        },
        'deposit-read': {
            'roles': [],
            'users': ['cms@inveniosoftware.org', 'cms2@inveniosoftware.org']
        },
        'deposit-update': {
            'roles': [],
            'users': ['cms@inveniosoftware.org', 'cms2@inveniosoftware.org']
        }
    }


@responses.activate
def test_add_permissions_no_access():
    responses.add(
        responses.POST,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid/actions/permissions',
        json={
            'status': 403,
            'message': 'Error'
        },
        status=403)

    with raises(BadStatusCode):
        PermissionsAPI().add(
            pid='some-pid',
            email='cms@inveniosoftware.org',
            rights=['read'],
        )


@responses.activate
def test_remove_permissions():
    responses.add(
        responses.POST,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid/actions/permissions',
        json={
            'permissions': {
                'deposit-admin': {
                    'roles': [],
                    'users': []
                },
                'deposit-read': {
                    'roles': [],
                    'users': ['cms@inveniosoftware.org']
                },
                'deposit-update': {
                    'roles': [],
                    'users': ['cms@inveniosoftware.org']
                }
            }
        },
        status=201,
    )

    resp = PermissionsAPI().remove(pid='some-pid',
                                   email='cms@inveniosoftware.org',
                                   rights=['read', 'update'])

    request = responses.calls[0].request
    assert request.headers['Accept'] == 'application/permissions+json'
    assert json.loads(request.body) == [{
        "email": "cms@inveniosoftware.org",
        "type": "user",
        "op": "remove",
        "action": "deposit-read"
    }, {
        "email": "cms@inveniosoftware.org",
        "type": "user",
        "op": "remove",
        "action": "deposit-update"
    }]
    assert resp == {
        'deposit-admin': {
            'roles': [],
            'users': []
        },
        'deposit-read': {
            'roles': [],
            'users': ['cms@inveniosoftware.org']
        },
        'deposit-update': {
            'roles': [],
            'users': ['cms@inveniosoftware.org']
        }
    }
