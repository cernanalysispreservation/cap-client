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
"""Tests for Metadata API."""

from __future__ import absolute_import, print_function

import json

import responses
from pytest import raises

from cap_client.api.metadata_api import MetadataAPI
from cap_client.errors import BadStatusCode


@responses.activate
def test_set_field_when_replacing_non_array_field():
    responses.add(
        responses.PATCH,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        content_type='application/basic+json',
        json={'metadata': {
            'object_field': {
                'new_field': 'new_value'
            }
        }},
        status=200)

    MetadataAPI().set(
        pid='some-pid',
        field='object_field.new_field',
        value='new_value',
    )

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/basic+json'
    assert json.loads(responses.calls[0].request.body) == [{
        'op': 'replace',
        'path': '/object_field/new_field',
        'value': 'new_value'
    }]


@responses.activate
def test_set_field_when_replacing_array_field():
    responses.add(
        responses.PATCH,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        content_type='application/basic+json',
        json={'metadata': {
            'array_field': ['new_value']
        }},
        status=200)

    MetadataAPI().set(
        pid='some-pid',
        field='array_field.0',
        value='new_value',
    )

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/basic+json'
    assert json.loads(responses.calls[0].request.body) == [{
        'op': 'replace',
        'path': '/array_field/0',
        'value': 'new_value'
    }]


@responses.activate
def test_set_field_when_non_existing_index():
    responses.add(
        responses.PATCH,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        content_type='application/basic+json',
        json={
            'status': 400,
            'message': 'Could not patch JSON.'
        },
        status=400)

    with raises(BadStatusCode):
        MetadataAPI().set(
            pid='some-pid',
            field='array_field.100',
            value='new_value',
        )

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/basic+json'
    assert json.loads(responses.calls[0].request.body) == [{
        'op': 'replace',
        'path': '/array_field/100',
        'value': 'new_value'
    }]


#@responses.activate
#def test_set_field_when_replace_on_empty_array(cap_api):
#    responses.add(
#        responses.PATCH,
#        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
#        body='IndexError: list assignment index out of range',
#        status=500)
#
#    with raises(BadStatusCode):
#        cap_api.set_field('some-pid', 'empty_array_field.0', 'new_value')
#
#    assert responses.calls[0].request.headers[
#        'Accept'] == 'application/basic+json'
#    assert json.loads(responses.calls[0].request.body) == [{
#        'op': 'replace',
#        'path': '/empty_array_field/0',
#        'value': 'new_value'
#    }]

#@responses.activate
#def test_set_field_when_appending_field_to_array(cap_api):
#    responses.add(
#        responses.PATCH,
#        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
#        content_type='application/basic+json',
#        json={'metadata': {
#            'array_field': ['appended_value']
#        }},
#        status=200)
#
#    cap_api.set_field('some-pid', 'array_field', 'appended_value', append=True)
#
#    assert responses.calls[0].request.headers[
#        'Accept'] == 'application/basic+json'
#    assert json.loads(responses.calls[0].request.body) == [{
#        'op': 'add',
#        'path': '/array_field/-',
#        'value': 'appended_value'
#    }]
#
#
#@responses.activate
#def test_set_field_when_appending_to_non_array_field(cap_api):
#    responses.add(
#        responses.PATCH,
#        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
#        status=500)  # TOFIX
#
#    with raises(BadStatusCode):
#        cap_api.set_field('some-pid',
#                          'non_array_field',
#                          'appended_value',
#                          append=True)
#
#    assert responses.calls[0].request.headers[
#        'Accept'] == 'application/basic+json'
#    assert json.loads(responses.calls[0].request.body) == [{
#        'op': 'add',
#        'path': '/non_array_field/-',
#        'value': 'appended_value'
#    }]
#
#
#@responses.activate
#def test_set_field_when_appending_to_non_existing_field(cap_api):
#    responses.add(
#        responses.PATCH,
#        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
#        content_type='application/basic+json',
#        json={
#            'status': 400,
#            'message': 'Could not patch JSON.'
#        },
#        status=400)
#
#    with raises(BadStatusCode):
#        cap_api.set_field('some-pid',
#                          'non_existing_field',
#                          'appended_value',
#                          append=True)
#
#    assert responses.calls[0].request.headers[
#        'Accept'] == 'application/basic+json'
#    assert json.loads(responses.calls[0].request.body) == [{
#        'op': 'add',
#        'path': '/non_existing_field/-',
#        'value': 'appended_value'
#    }]
#
#
#@responses.activate
#def test_set_field_when_appending_with_specific_index(cap_api):
#    with raises(BadParameter):
#        cap_api.set_field('some-pid',
#                          'array_field.7',
#                          'appended_value',
#                          append=True)
#
#
#@responses.activate
#def test_set_field_when_appending_to_object(cap_api):
#    responses.add(
#        responses.PATCH,
#        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
#        content_type='application/basic+json',
#        json={
#            'metadata': {
#                'object_field': {
#                    "-": "appended_value"  # TOFIX
#                }
#            }
#        },
#        status=200)
#
#    cap_api.set_field('some-pid',
#                      'object_field',
#                      'appended_value',
#                      append=True)
#
#    assert responses.calls[0].request.headers[
#        'Accept'] == 'application/basic+json'
#    assert json.loads(responses.calls[0].request.body) == [{
#        'op': 'add',
#        'path': '/object_field/-',
#        'value': 'appended_value'
#    }]


@responses.activate
def test_remove_field_when_object_field():
    responses.add(
        responses.PATCH,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        content_type='application/basic+json',
        json={'metadata': {
            'object_field': {}
        }},
        status=200)

    MetadataAPI().remove(pid='some-pid', field='object_field.field_to_remove')

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/basic+json'
    assert json.loads(responses.calls[0].request.body) == [{
        'op': 'remove',
        'path': '/object_field/field_to_remove',
    }]


@responses.activate
def test_remove_field_when_non_existing_field():
    responses.add(
        responses.PATCH,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        content_type='application/basic+json',
        json={
            'status': 400,
            'message': 'Could not patch JSON.'
        },
        status=400)

    with raises(BadStatusCode):
        MetadataAPI().remove(pid='some-pid',
                             field='non_existing_field_to_remove')

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/basic+json'
    assert json.loads(responses.calls[0].request.body) == [{
        'op': 'remove',
        'path': '/non_existing_field_to_remove',
    }]


@responses.activate
def test_remove_field_when_array_element():
    responses.add(
        responses.PATCH,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        content_type='application/basic+json',
        json={'metadata': {
            'array_field': ['first_value']
        }},
        status=200)

    MetadataAPI().remove(pid='some-pid', field='array_field.1')

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/basic+json'
    assert json.loads(responses.calls[0].request.body) == [{
        'op': 'remove',
        'path': '/array_field/1',
    }]


@responses.activate
def test_remove_field_when_non_existing_index_for_array_field():
    responses.add(
        responses.PATCH,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        content_type='application/basic+json',
        json={'metadata': {
            'array_field': ['first_value']
        }},
        status=400)

    with raises(BadStatusCode):
        MetadataAPI().remove(pid='some-pid', field='array_field.1000')

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/basic+json'
    assert json.loads(responses.calls[0].request.body) == [{
        'op': 'remove',
        'path': '/array_field/1000',
    }]
