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
"""Tests for Repositories API."""

from __future__ import absolute_import, print_function

import json

import responses
from pytest import raises

from cap_client.api.repositories_api import RepositoriesAPI
from cap_client.errors import BadStatusCode


@responses.activate
def test_get_repositories_from_server_without_snapshots():
    responses.add(
        responses.GET,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={
            'webhooks': [{
                "branch": "master",
                "event_type": "release",
                "host": "github.com",
                "name": "test-repo",
                "owner": "user",
                "snapshots": [{
                    "created": "2020-03-11T13:45:16.199496+00:00",
                    "payload": {
                        "branch": None,
                        "commit": None,
                        "event_type": "release",
                        "link": "https://github.com/Lilykos/test-repo/releases/tag/0.2",
                        "author": {
                            "id": 2445433,
                            "name": "Lilykos"
                        },
                        "release": {
                            "name": "test",
                            "tag": "0.2"
                        }
                    }
                }]
            }]
        },
        status=200,
    )

    resp = RepositoriesAPI().get('some-pid')

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/repositories+json'
    assert resp == [{
        "branch": "master",
        "event_type": "release",
        "host": "github.com",
        "name": "test-repo",
        "owner": "user",
    }]


@responses.activate
def test_get_repositories_from_server_with_snapshots():
    responses.add(
        responses.GET,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={
            'webhooks': [{
                "branch": "master",
                "event_type": "release",
                "host": "github.com",
                "name": "test-repo",
                "owner": "user",
                "snapshots": [{
                    "created": "2020-03-11T13:45:16.199496+00:00",
                    "payload": {
                        "branch": None,
                        "commit": None,
                        "event_type": "release",
                        "link": "https://github.com/Lilykos/test-repo/releases/tag/0.2",
                        "author": {
                            "id": 2445433,
                            "name": "Lilykos"
                        },
                        "release": {
                            "name": "test",
                            "tag": "0.2"
                        }
                    }
                }]
            }]
        },
        status=200,
    )

    resp = RepositoriesAPI().get('some-pid', True)

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/repositories+json'
    assert resp == [{
        "branch": "master",
        "event_type": "release",
        "host": "github.com",
        "name": "test-repo",
        "owner": "user",
        "snapshots": [{
            "created": "2020-03-11T13:45:16.199496+00:00",
            "payload": {
                "branch": None,
                "commit": None,
                "event_type": "release",
                "link": "https://github.com/Lilykos/test-repo/releases/tag/0.2",
                "author": {
                    "id": 2445433,
                    "name": "Lilykos"
                },
                "release": {
                    "name": "test",
                    "tag": "0.2"
                }
            }
        }]
    }]


@responses.activate
def test_get_repo_400_from_server():
    responses.add(
        responses.GET,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={
            'status': 400,
            'message': 'Error'
        },
        status=400)

    with raises(BadStatusCode):
        RepositoriesAPI().get('some-pid')

@responses.activate
def test_upload_repo_no_webhook():
    responses.add(
        responses.POST,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid/actions/upload',
        json={'webhooks': []},
        status=201)

    resp = RepositoriesAPI().upload('some-pid', 'https://github.com/myrepo')

    request = responses.calls[0].request
    assert request.headers['Accept'] == 'application/repositories+json'
    assert request.headers['Content-Type'] == 'application/json'
    assert json.loads(request.body) == {
        'url': 'https://github.com/myrepo',
        'webhook': False,
        'event_type': None
    }
    assert resp is None


@responses.activate
def test_upload_repo_push_webhook():
    responses.add(
        responses.POST,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid/actions/upload',
        json=[{
            "branch": "master",
            "event_type": "push",
            "host": "github.com",
            "name": "some_repo",
            "owner": "SomeUser",
            "snapshots": []
        }],
        status=201)

    resp = RepositoriesAPI().upload(
        pid='some-pid',
        url='https://github.com/myrepo',
        event_type='push',
    )

    request = responses.calls[0].request
    assert request.headers['Accept'] == 'application/repositories+json'
    assert request.headers['Content-Type'] == 'application/json'
    assert json.loads(request.body) == {
        'url': 'https://github.com/myrepo',
        'webhook': True,
        'event_type': 'push'
    }
    assert resp is None


@responses.activate
def test_upload_repo_when_400_from_server():
    responses.add(
        responses.POST,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid/actions/upload',
        json={
            'status': 400,
            'message': 'Error'
        },
        status=400,
    )

    with raises(BadStatusCode):
        RepositoriesAPI().upload('some-pid', 'endpoint')
