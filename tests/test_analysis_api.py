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
"""Tests for Analysis API."""

from __future__ import absolute_import, print_function

import responses
from click import UsageError
from pytest import raises

from cap_client.api.analysis_api import AnalysisAPI
from cap_client.errors import BadStatusCode



@responses.activate
def test_update_method_when_validate_failed_raises_exception():
    responses.add(
        responses.PUT,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={
            "status": 400,
            "message": "Validation error. Try again with valid data",
            "errors": [{
                "field": [],
                "message": "Additional properties are not allowed ('title' was unexpected)"
            }]
        },
        status=400)

    with raises(BadStatusCode):
        AnalysisAPI().update(pid='some-pid',
                             data={
                                 "title": "Bad Title",
                                 "basic_info": {
                                     "abstract": "Example Abstract"
                                 }
                             })


@responses.activate
def test_update_method_when_no_permission():
    responses.add(
        responses.PUT,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={
            'status': 403,
            'message': 'Forbidden'
        },
        status=403)

    with raises(BadStatusCode):
        AnalysisAPI().update(
            pid='some-pid',
            data={"basic_info": {
                "abstract": "Example abstract"
            }})


@responses.activate
def test_update_method_when_wrong_pid():
    responses.add(
        responses.PUT,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={
            'status': 404,
            'message': 'PID does not exist'
        },
        status=404)

    with raises(BadStatusCode):
        AnalysisAPI().update(
            pid='some-pid',
            data={"basic_info": {
                "abstract": "Example abstract"
            }})


@responses.activate
def test_update_method_when_success_returns_updated_data(record_data):
    responses.add(
        responses.PUT,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json=record_data,
        status=200,
    )

    resp = AnalysisAPI().update(pid='some-pid',
                                data={
                                    "metadata": {
                                        "general_title": "General relativity",
                                        "basic_info": {
                                            "analysis_number": "HIN-16-007",
                                            "people_info": [{
                                                "name": "John Doe"
                                            }, {
                                                "name": "Albert Einstein"
                                            }],
                                        }
                                    }
                                })

    assert resp == record_data


@responses.activate
def test_patch_method_when_no_permission():
    responses.add(
        responses.PATCH,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={
            'status': 403,
            'message': 'Forbidden'
        },
        status=403,
    )

    with raises(BadStatusCode):
        AnalysisAPI().patch(
            pid='some-pid',
            data=[{
                "op": "add",
                "path": "/test",
                "value": "test"
            }],
        )


@responses.activate
def test_patch_method_when_wrong_pid():
    responses.add(
        responses.PATCH,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={
            'status': 404,
            'message': 'PID does not exist'
        },
        status=404,
    )

    with raises(BadStatusCode):
        AnalysisAPI().patch(
            pid='some-pid',
            data=[{
                "op": "add",
                "path": "/test",
                "value": "test"
            }],
        )


@responses.activate
def test_patch_method_when_success_returns_updated_data(record_data):
    responses.add(
        responses.PATCH,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json=record_data,
        status=200,
    )

    resp = AnalysisAPI().patch(pid='some-pid',
                               data=[{
                                   "op": "add",
                                   "path": "/basic_info/analysis_number",
                                   "value": "HIN-16-007"
                               }])

    assert responses.calls[0].request.headers[
        'Content-Type'] == 'application/json-patch+json'
    assert responses.calls[0].request.headers[
        'Accept'] == 'application/basic+json'
    assert resp == record_data


@responses.activate
def test_patch_method_when_failed_raises_exception():
    responses.add(
        responses.PATCH,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={
            'status': 400,
            'message': 'Could not patch JSON.'
        },
        status=400)

    with raises(BadStatusCode):
        AnalysisAPI().patch(
            pid='some-pid',
            data=[{
                "op": "add",
                "path": "/test",
                "value": "test"
            }],
        )


@responses.activate
def test_get_drafts_method_with_given_pid(record_data):
    responses.add(
        responses.GET,
        'https://analysispreservation-dev.cern.ch/api/deposits/some_pid',
        json=record_data,
        headers={'Content-Type': 'application/repositories+json'},
        status=200)

    resp = AnalysisAPI().get_draft_by_pid('some_pid')

    assert resp == record_data
