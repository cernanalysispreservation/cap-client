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

from __future__ import absolute_import, print_function

import responses
from click import UsageError
from pytest import raises

from cap_client.errors import BadStatusCode


def test_create_method_when_both_ana_type_and_schema_provided_raises_UsageError(
    cap_api):
    with raises(UsageError):
        cap_api.create(data={'$schema': 'myschema'}, ana_type='test-type')


def test_create_method_when_no_ana_type_or_schema_provided_raises_UsageError(
    cap_api):
    with raises(UsageError):
        cap_api.create(data={})


@responses.activate
def test_create_method_when_type_not_valid_raises_BadStatusCode(cap_api):
    responses.add(responses.POST,
                  'https://analysispreservation-dev.cern.ch/api/deposits/',
                  json={
                      'status': 400,
                      'message': 'Schema doesnt exist.'
                  },
                  status=400)

    with raises(BadStatusCode):
        cap_api.create(
            data={"basic_info": {
                "abstract": "Example abstract"
            }},
            ana_type='test-type',
        )


@responses.activate
def test_create_method_when_no_permission_raises_BadStatusCode(cap_api):
    responses.add(responses.POST,
                  'https://analysispreservation-dev.cern.ch/api/deposits/',
                  json={
                      'status': 401,
                      'message': 'Permission Error'
                  },
                  status=401)

    with raises(BadStatusCode):
        cap_api.create(
            data={"basic_info": {
                "abstract": "Example abstract"
            }},
            ana_type='test-type',
        )


@responses.activate
def test_create_method_when_validation_error_raises_BadStatusCode(cap_api):
    responses.add(
        responses.POST,
        'https://analysispreservation-dev.cern.ch/api/deposits/',
        json={
            "status": 400,
            "message": "Validation error. Try again with valid data",
            "errors": [{
                "field": [],
                "message": "Additional properties are not allowed ('newfield' was unexpected)"
            }]
        },
        status=400)

    with raises(BadStatusCode):
        cap_api.create(
            data={
                "newfield": "title",
                "basic_info": {
                    "abstract": "Example Abstract"
                }
            },
            ana_type='test-type',
        )


@responses.activate
def test_create_method_when_success_returns_newly_created_deposit_via_basic_serializer(
    cap_api):
    responses.add(responses.POST,
                  'https://analysispreservation-dev.cern.ch/api/deposits/',
                  json={
                      'access': {
                          'deposit-admin': {
                              'roles': [],
                              'users': ['info@inveniosoftware.org']
                          },
                          'deposit-read': {
                              'roles': [],
                              'users': ['info@inveniosoftware.org']
                          },
                          'deposit-update': {
                              'roles': [],
                              'users': ['info@inveniosoftware.org']
                          }
                      },
                      'experiment': 'LHCb',
                      'schema': {
                          'name': 'lhcb',
                          'version': '0.0.1'
                      },
                      'id': 'some-pid',
                      'metadata': {
                          'basic_info': {
                              'analysis_number': 'HIN-16-007',
                          },
                          'general_title': 'Test Example'
                      }
                  },
                  status=201)
    serialized_response = {
        "metadata": {
            "basic_info": {
                'analysis_number': 'HIN-16-007'
            },
            "general_title": "Test Example"
        },
        "pid": "some-pid"
    }
    responses.add(
        responses.PUT,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json=serialized_response,
        status=200)

    resp = cap_api.create(
        data={
            "basic_info": {
                "people_info": [{
                    "name": "John Doe"
                }],
            },
            "general_title": "Test Example"
        },
        ana_type='lhcb',
    )

    assert responses.calls[0].request.headers[
        'Content-Type'] == 'application/json'
    assert responses.calls[1].request.headers[
        'Accept'] == 'application/basic+json'
    assert responses.calls[1].request.headers[
        'Content-Type'] == 'application/json'
    assert resp == serialized_response


@responses.activate
def test_update_method_when_validate_failed_raises_exception(cap_api):
    url = 'https://analysispreservation-dev.cern.ch/api/deposits/some-pid'
    responses.add(
        responses.PUT,
        url,
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
        cap_api.update(pid='some-pid',
                       data={
                           "title": "Bad Title",
                           "basic_info": {
                               "abstract": "Example Abstract"
                           }
                       })


@responses.activate
def test_update_method_when_no_permission(cap_api):
    url = 'https://analysispreservation-dev.cern.ch/api/deposits/some-pid'

    responses.add(responses.PUT,
                  url,
                  json={
                      'status': 403,
                      'message': 'Forbidden'
                  },
                  status=403)

    with raises(BadStatusCode):
        cap_api.update(pid='some-pid',
                       data={"basic_info": {
                           "abstract": "Example abstract"
                       }})


@responses.activate
def test_update_method_when_wrong_pid(cap_api):
    responses.add(
        responses.PUT,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={
            'status': 404,
            'message': 'PID does not exist'
        },
        status=404)

    with raises(BadStatusCode):
        cap_api.update(pid='some-pid',
                       data={"basic_info": {
                           "abstract": "Example abstract"
                       }})


@responses.activate
def test_update_method_when_success_returns_updated_data(cap_api, record_data):
    responses.add(
        responses.PUT,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json=record_data,
        status=200,
    )

    resp = cap_api.update(pid='some-pid',
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
