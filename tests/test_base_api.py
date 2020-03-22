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
"""Tests for base CAPAPI."""

from __future__ import absolute_import, print_function

import json

import responses
from pytest import raises

from cap_client.api.base import CapAPI
from cap_client.errors import BadStatusCode


@responses.activate
def test_make_request_when_json_response():
    responses.add(
        responses.POST,
        'https://analysispreservation-dev.cern.ch/api/endpoint',
        json={'message': 'success'},
        stream=False,
        status=201,
    )

    resp = CapAPI()._make_request(url='endpoint',
                                  method='post',
                                  expected_status_code=201,
                                  headers={
                                      'Content-Type': 'application/json',
                                      'Accept': 'application/serializer+json'
                                  },
                                  data=json.dumps({}))

    request = responses.calls[0].request
    assert request.headers['Accept'] == 'application/serializer+json'
    assert request.headers['Content-Type'] == 'application/json'
    assert json.loads(request.body) == {}

    assert resp == {'message': 'success'}


@responses.activate
def test_make_request_when_request_successful_with_stream():
    responses.add(responses.GET,
                  'https://analysispreservation-dev.cern.ch/api/endpoint',
                  body=b'test-data',
                  status=200,
                  stream=True)

    resp = CapAPI()._make_request(url='endpoint', stream=True)

    assert resp.content == b'test-data'


@responses.activate
def test_make_request_when_no_text_resp():
    responses.add(responses.GET,
                  'https://analysispreservation-dev.cern.ch/api/endpoint',
                  body='success',
                  status=201)

    resp = CapAPI()._make_request(url='endpoint',
                                  expected_status_code=201,
                                  method='get')
    assert resp == 'success'


@responses.activate
def test_make_request_when_response_status_code_different_than_expected_and_json_response(
):
    responses.add(responses.GET,
                  'https://analysispreservation-dev.cern.ch/api/endpoint',
                  json={
                      'status': 400,
                      'message': 'Error'
                  },
                  status=400)

    with raises(BadStatusCode) as e:
        CapAPI()._make_request(url='endpoint', expected_status_code=201)

        assert e.message == 'Error'
        assert e.data == {'status': 400, 'message': 'Error'}
        assert e.expected_status_code == 201
        assert e.status_code == 200
        assert e.endpoint == 'https://analysispreservation-dev.cern.ch/api/endpoint'
