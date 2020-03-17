# -*- coding: utf-8 -*-
#
# This file is part of CERN Analysis Preservation Framework.
# Copyright (C) 2016, 2017 CERN.
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

import json
import sys

import responses
from click import BadParameter
from mock import mock_open, patch
from pytest import raises

from cap_client.errors import (BadStatusCode, MissingJsonFile,
                               UnknownAnalysisType)

if sys.version_info.major == 3:
    builtin_module_name = 'builtins'
else:
    builtin_module_name = '__builtin__'


@responses.activate
def test_make_request_when_request_successful(cap_api, record_data):
    url = 'https://analysispreservation-dev.cern.ch/api/endpoint'
    responses.add(responses.GET, url, json=record_data, status=200)

    resp = cap_api._make_request(url='endpoint')
    assert resp == record_data


@responses.activate
def test_make_request_when_request_successful_with_stream(cap_api):
    url = 'https://analysispreservation-dev.cern.ch/api/endpoint'
    stream_data = b'test-data'

    responses.add(responses.GET, url, body=stream_data, status=200)

    resp = cap_api._make_request(url='endpoint', stream=True)
    assert resp.content == stream_data


@responses.activate
def test_make_request_when_sending_record_data(cap_api, record_data):
    url = 'https://analysispreservation-dev.cern.ch/api/endpoint'
    responses.add(responses.POST, url, json=record_data, status=200)

    resp = cap_api._make_request(url='endpoint',
                                 method='post',
                                 data=record_data)
    assert resp == record_data


@responses.activate
def test_make_request_when_no_json_in_resp(cap_api):
    url = 'https://analysispreservation-dev.cern.ch/api/endpoint'
    responses.add(responses.DELETE, url, json=None, status=204)

    resp = cap_api._make_request(url='endpoint',
                                 expected_status_code=204,
                                 method='delete')

    # when no json in resp no error raised, just no data returned
    assert resp is None


@responses.activate
def test_make_request_when_request_fails(cap_api):
    url = 'https://analysispreservation-dev.cern.ch/api/endpoint'
    responses.add(responses.GET,
                  url,
                  json={
                      'status': 400,
                      'message': 'Error'
                  },
                  status=400)

    with raises(BadStatusCode):
        cap_api._make_request(url='endpoint')


@patch('requests.get')
def test_get_available_types_when_no_available_types(mock_requests, cap_api,
                                                     user_data):
    user_data['deposit_groups'] = []
    mock_requests.return_value.status_code = 200
    mock_requests.return_value.json.return_value = user_data

    types = cap_api._get_available_types()

    assert types == []


@responses.activate
def test_get_drafts_method_with_given_pid(cap_api, record_data):
    responses.add(
        responses.GET,
        'https://analysispreservation-dev.cern.ch/api/deposits/some_pid',
        json=record_data,
        headers={'Content-Type': 'application/repositories+json'},
        status=200)

    resp = cap_api.get_draft_by_pid('some_pid')

    assert resp == record_data


@patch('requests.get')
def test_get_field_when_field_unspecified(mock_requests, cap_api, record_data):
    mock_requests.return_value.status_code = 200
    mock_requests.return_value.json.return_value = record_data

    resp = cap_api.get_field('some_pid')

    assert resp == record_data['metadata']


@patch('requests.get')
def test_get_field_when_field_specified(mock_requests, cap_api, record_data):
    mock_requests.return_value.status_code = 200
    mock_requests.return_value.json.return_value = record_data

    resp = cap_api.get_field('some_pid', 'general_title')

    assert resp == record_data['metadata']['general_title']


@patch('requests.get')
def test_get_field_when_field_is_incorrect(mock_requests, cap_api,
                                           record_data):
    mock_requests.return_value.status_code = 200
    mock_requests.return_value.json.return_value = record_data

    with raises(KeyError):
        cap_api.get_field('some_pid', 'title')


# @patch('requests.get')
# def test_ping_method(mock_requests, cap_api):
#     mock_requests.return_value.status_code = 200
#     mock_requests.return_value.json.return_value = 'Pong'

#     resp = cap_api.ping()

#     assert resp == 'Pong'


@patch('requests.delete')
def test_delete_method_with_given_pid(mock_requests, cap_api, record_data):
    mock_requests.return_value.status_code = 204
    mock_requests.return_value.json.return_value = None

    resp = cap_api.delete('some_pid')

    assert resp is None


@patch('requests.get')
def test_types(mock_requests, cap_api, mocked_cap_api):
    mock_requests.return_value.status_code = 200
    mock_requests.return_value.json.return_value = [
        'atlas-workflows', 'alice-analysis'
    ]

    resp = cap_api.types()

    assert resp == ['atlas-workflows', 'alice-analysis']


# Public methods
@patch('requests.get')
def test_get_available_types_returns_all_available_types(
        mock_requests, cap_api, user_data):
    mock_requests.return_value.status_code = 200
    mock_requests.return_value.json.return_value = user_data

    types = cap_api._get_available_types()

    assert 'atlas-workflows' in types
    assert 'alice-analysis' in types


def test_create_method_when_no_type_given_returns_list_of_options(
        mocked_cap_api):  # noqa
    with raises(UnknownAnalysisType):
        mocked_cap_api.create(ana_type=None)


def test_create_method_when_type_given_not_in_available_options(
        mocked_cap_api):  # noqa
    with raises(UnknownAnalysisType):
        mocked_cap_api.create(ana_type='non-atlas-workflows')


def test_create_method_when_no_file_with_data_given(mocked_cap_api):
    with raises(MissingJsonFile):
        mocked_cap_api.create(ana_type='atlas-workflows')


@patch('{}.open'.format(builtin_module_name),
       new_callable=mock_open,
       read_data='{,}]')
def test_create_method_when_no_json_in_given_file(mock_open, mocked_cap_api):
    with raises(ValueError):
        mocked_cap_api.create(json_='file', ana_type='atlas-workflows')


def test_create_method_when_validate_failed_raises_exception(
        mocked_cap_api, record_data):
    json_data = json.dumps(record_data)
    with patch('{}.open'.format(builtin_module_name),
               new_callable=mock_open,
               read_data=json_data):
        mocked_cap_api._make_request.side_effect = [BadStatusCode(), None]
        with raises(BadStatusCode):
            mocked_cap_api.create(json_='file', ana_type='atlas-workflows')


@patch('{}.open'.format(builtin_module_name), new_callable=mock_open)
def test_update_method_when_json_file_not_found(mock_open, cap_api):
    mock_open.side_effect = IOError

    with raises(MissingJsonFile):
        cap_api.update(pid='some_pid', json_='file')


@patch('{}.open'.format(builtin_module_name),
       new_callable=mock_open,
       read_data='{,}]')
def test_update_method_when_no_json_in_given_file(mock_open, cap_api):
    with raises(MissingJsonFile):
        cap_api.update(pid='some-pid', json_='file')


@responses.activate
def test_update_method_when_validate_failed_raises_exception(cap_api):
    url = 'https://analysispreservation-dev.cern.ch/api/deposits/some-pid'
    mock_json_data = {
        "title": "Bad Title",
        "basic_info": {
            "abstract": "Example Abstract"
        }
    }
    mock_response = {
        "status": 400,
        "message": "Validation error. Try again with valid data",
        "errors": [{
            "field": [],
            "message": "Additional properties are not allowed ('title' was unexpected)"
        }]
    }
    responses.add(responses.PUT, url, json=mock_response, status=400)
    with raises(BadStatusCode):
        cap_api.update(pid='some-pid', json_=json.dumps(mock_json_data))


@responses.activate
def test_update_method_when_no_permission(cap_api):
    url = 'https://analysispreservation-dev.cern.ch/api/deposits/some-pid'
    mock_json_data = {"basic_info": {"abstract": "Example abstract"}}

    responses.add(responses.PUT,
                  url,
                  json={
                      'status': 403,
                      'message': 'Forbidden'
                  },
                  status=403)

    with raises(BadStatusCode):
        cap_api.update(pid='some-pid', json_=json.dumps(mock_json_data))


@responses.activate
def test_update_method_when_wrong_pid(cap_api):
    url = 'https://analysispreservation-dev.cern.ch/api/deposits/some-pid'
    mock_json_data = {"basic_info": {"abstract": "Example abstract"}}

    responses.add(responses.PUT,
                  url,
                  json={
                      'status': 404,
                      'message': 'PID does not exist'
                  },
                  status=404)

    with raises(BadStatusCode):
        cap_api.update(pid='some-pid', json_=json.dumps(mock_json_data))


@responses.activate
def test_update_method_when_success_returns_updated_data(cap_api, record_data):
    url = 'https://analysispreservation-dev.cern.ch/api/deposits/some-pid'
    mock_json_data = {
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
    }
    responses.add(responses.PUT, url, json=record_data, status=200)

    resp = cap_api.update(pid='some-pid', json_=json.dumps(mock_json_data))
    assert resp == record_data


def test_patch_method(mocked_cap_api, record_data):
    json_data = json.dumps(record_data)

    with patch('{}.open'.format(builtin_module_name),
               new_callable=mock_open,
               read_data=json_data):
        mocked_cap_api._make_request.return_value = record_data

        resp = mocked_cap_api.patch(filename='file', pid='some_pid')

        named_args = mocked_cap_api._make_request.call_args[1]

        assert resp == record_data
        assert named_args['method'] == 'patch'
        assert named_args['headers'] == {
            'Content-Type': 'application/json-patch+json'
        }


def test_patch_method_when_no_file_with_data_given(mocked_cap_api):
    with raises(IOError):
        mocked_cap_api.patch(pid='some_pid')


@patch('{}.open'.format(builtin_module_name),
       new_callable=mock_open,
       read_data='{,}]')
def test_patch_method_when_no_json_in_given_file(mock_open, mocked_cap_api):
    with raises(ValueError):
        mocked_cap_api.patch(filename='file')


@responses.activate
def test_set_field(cap_api):
    url = 'https://analysispreservation-dev.cern.ch/api/deposits/some-pid'
    mock_response = {
        "metadata": {
            "basic_info": {
                "abstract": "test_value_abstract"
            },
            "general_title": "test"
        }
    }

    responses.add(responses.PATCH, url, json=mock_response, status=200)

    resp = cap_api.set_field('test_field', 'test_value', 'some-pid')

    assert responses.calls[0].request.headers[
        'Content-Type'] == 'application/json-patch+json'
    assert responses.calls[0].request.headers[
        'Accept'] == 'application/basic+json'
    assert resp == mock_response['metadata']


@responses.activate
def test_set_field_as_array(cap_api):
    url = 'https://analysispreservation-dev.cern.ch/api/deposits/some-pid'
    mock_response = {
        "metadata": {
            "basic_info": {
                "abstract": "test_value_abstract",
                "test_array": ["a", "b"]
            },
            "general_title": "test"
        }
    }

    responses.add(responses.PATCH, url, json=mock_response, status=200)

    resp = cap_api.set_field('basic_info.test_array', '["a", "b"]', 'some-pid')

    assert responses.calls[0].request.headers[
        'Content-Type'] == 'application/json-patch+json'
    assert responses.calls[0].request.headers[
        'Accept'] == 'application/basic+json'
    assert resp == mock_response['metadata']


@responses.activate
def test_set_field_append_to_array(cap_api):
    url = 'https://analysispreservation-dev.cern.ch/api/deposits/some-pid'
    mock_response = {
        "metadata": {
            "basic_info": {
                "abstract": "test_value_abstract",
                "test_array": ["a", "b", "abc"]
            },
            "general_title": "test"
        }
    }

    responses.add(responses.PATCH, url, json=mock_response, status=200)

    resp = cap_api.set_field('basic_info.test_array',
                             'abc',
                             'some-pid',
                             append=True)

    assert responses.calls[0].request.headers[
        'Content-Type'] == 'application/json-patch+json'
    assert responses.calls[0].request.headers[
        'Accept'] == 'application/basic+json'
    assert resp == mock_response['metadata']


@responses.activate
def test_set_field_in_nested_dict(cap_api):
    url = 'https://analysispreservation-dev.cern.ch/api/deposits/some-pid'
    mock_response = {
        "metadata": {
            "basic_info": {
                "abstract": "test_value_abstract",
                "test_array": [{
                    "test": "test-one"
                }]
            },
            "general_title": "test"
        }
    }

    responses.add(responses.PATCH, url, json=mock_response, status=200)

    resp = cap_api.set_field('basic_info.test_array.0.test',
                             'test-one',
                             'some-pid',
                             append=True)

    assert responses.calls[0].request.headers[
        'Content-Type'] == 'application/json-patch+json'
    assert responses.calls[0].request.headers[
        'Accept'] == 'application/basic+json'
    assert resp == mock_response['metadata']


@responses.activate
def test_set_field_when_pid_is_wrong(cap_api):
    responses.add(
        responses.PATCH,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={
            'status_code': 404,
            'message': 'PID does not exist.'
        },
        status=404)

    with raises(BadStatusCode):
        cap_api.set_field('basic_info.test', 'test', 'some-pid')


@responses.activate
def test_set_field_when_no_permission(cap_api):
    responses.add(
        responses.PATCH,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={
            'status_code': 403,
            'message': 'Forbidden'
        },
        status=403)

    with raises(BadStatusCode):
        cap_api.set_field('basic_info.test', 'test', 'some-pid')


@responses.activate
def test_upload_repo_no_webhook(cap_api):
    url = 'https://analysispreservation-dev.cern.ch/api/deposits/some-pid/actions/upload'
    responses.add(responses.POST, url, json={'webhooks': []}, status=201)

    resp = cap_api.upload_repository('some-pid', 'endpoint')

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/repositories+json'
    assert resp == {'webhooks': []}


@responses.activate
def test_upload_repo_push_webhook(cap_api):
    url = 'https://analysispreservation-dev.cern.ch/api/deposits/some-pid/actions/upload'
    webhooks = [{
        "branch": "master",
        "event_type": "push",
        "host": "github.com",
        "name": "some_repo",
        "owner": "SomeUser",
        "snapshots": []
    }]

    responses.add(responses.POST, url, json=webhooks, status=201)

    resp = cap_api.upload_repository('some-pid', 'endpoint')

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/repositories+json'
    assert resp == webhooks


@responses.activate
def test_upload_repo_400_from_server(cap_api):
    url = 'https://analysispreservation-dev.cern.ch/api/deposits/some-pid/actions/upload'
    responses.add(responses.POST,
                  url,
                  json={
                      'status': 400,
                      'message': 'Error'
                  },
                  stream=True,
                  status=400)

    with raises(BadStatusCode):
        cap_api.upload_repository('some-pid', 'endpoint')


@responses.activate
def test_get_repositories_from_server_without_snapshots(cap_api):
    url = 'https://analysispreservation-dev.cern.ch/api/deposits/some-pid'
    mock_response = {
        'webhooks': [{
            "branch": "master",
            "event_type": "release",
            "host": "github.com",
            "name": "test-repo",
            "owner": "user",
            "snapshots": []
        }]
    }

    responses.add(responses.GET,
                  url,
                  json=mock_response,
                  stream=True,
                  status=200)

    resp = cap_api.get_repositories('some-pid')

    mock_response['webhooks'][0].pop('snapshots')

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/repositories+json'
    assert resp == mock_response


@responses.activate
def test_get_repositories_from_server_with_snapshots(cap_api):
    url = 'https://analysispreservation-dev.cern.ch/api/deposits/some-pid'
    mock_response = {
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
    }

    responses.add(responses.GET,
                  url,
                  json=mock_response,
                  stream=True,
                  status=200)

    resp = cap_api.get_repositories('some-pid', True)

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/repositories+json'
    assert resp == mock_response


@responses.activate
def test_get_repo_400_from_server(cap_api):
    url = 'https://analysispreservation-dev.cern.ch/api/deposits/some-pid'
    responses.add(responses.GET,
                  url,
                  json={
                      'status': 400,
                      'message': 'Error'
                  },
                  stream=True,
                  status=400)

    with raises(BadStatusCode):
        cap_api.get_repositories('some-pid')


@responses.activate
def test_get_permissions(cap_api):
    url = 'https://analysispreservation-dev.cern.ch/api/deposits/some-pid'
    mock_permissions = {
        'permissions': {
            'deposit-admin': {
                'roles': [],
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
    }

    responses.add(responses.GET,
                  url,
                  json=mock_permissions,
                  stream=True,
                  status=200)

    resp = cap_api.get_permissions('some-pid')

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/permissions+json'
    assert resp == mock_permissions


@responses.activate
def test_add_permissions(cap_api):
    url = 'https://analysispreservation-dev.cern.ch/api/deposits/some-pid/actions/permissions'
    mock_permissions = {
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
    }

    responses.add(responses.POST,
                  url,
                  json=mock_permissions,
                  stream=True,
                  status=201)

    resp = cap_api.add_permissions(pid='some-pid',
                                   email='cms2@inveniosoftware.org',
                                   rights=['read', 'update'])

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/permissions+json'
    assert resp == mock_permissions


@responses.activate
def test_add_permissions_no_access(cap_api):
    url = 'https://analysispreservation-dev.cern.ch/api/deposits/some-pid/actions/permissions'

    responses.add(responses.POST,
                  url,
                  json={
                      'status': 403,
                      'message': 'Error'
                  },
                  status=403)

    with raises(BadStatusCode):
        cap_api.add_permissions(pid='some-pid',
                                email='cms@inveniosoftware.org',
                                rights=['read'])


@responses.activate
def test_remove_permissions(cap_api):
    url = 'https://analysispreservation-dev.cern.ch/api/deposits/some-pid/actions/permissions'
    mock_permissions = {
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
    }

    responses.add(responses.POST, url, json=mock_permissions, status=201)

    resp = cap_api.remove_permissions(pid='some-pid',
                                      email='cms@inveniosoftware.org',
                                      rights=['read'])

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/permissions+json'
    assert resp == mock_permissions


@responses.activate
def test_get_schema_deposit(cap_api):
    url = 'https://analysispreservation-dev.cern.ch/api/jsonschemas/some-type?resolve=True'
    mock_schema = {
        'record_schema': {},
        'deposit_schema': {
            'title': 'Test',
            'properties': {
                '_deposit': {},
                '_files': {},
                'basic_info': {
                    'id': 'basic_info',
                    'title': 'Basic Information'
                },
            }
        }
    }
    mock_response = {
        'title': 'Test',
        'properties': {
            'basic_info': {
                'id': 'basic_info',
                'title': 'Basic Information'
            },
        }
    }

    responses.add(responses.GET, url, json=mock_schema, status=200)

    resp = cap_api.get_schema(ana_type='some-type')
    assert resp == mock_response


@responses.activate
def test_get_schema_record(cap_api):
    url = 'https://analysispreservation-dev.cern.ch/api/jsonschemas/some-type/0.0.1?resolve=True'
    mock_schema = {
        'deposit_schema': {},
        'record_schema': {
            'title': 'Record Test',
            'properties': {
                '_deposit': {},
                '_files': {},
                'basic_info': {
                    'id': 'basic_info',
                    'title': 'Basic Information'
                },
            }
        }
    }
    mock_response = {
        'title': 'Record Test',
        'properties': {
            'basic_info': {
                'id': 'basic_info',
                'title': 'Basic Information'
            },
        }
    }

    responses.add(responses.GET, url, json=mock_schema, status=200)

    resp = cap_api.get_schema(ana_type='some-type',
                              version='0.0.1',
                              record=True)
    assert resp == mock_response


@responses.activate
def test_get_schema_not_found(cap_api):
    url = 'https://analysispreservation-dev.cern.ch/api/jsonschemas/some-type?resolve=True'
    responses.add(responses.GET,
                  url,
                  json={
                      'status': 404,
                      'message': 'Error'
                  },
                  status=404)

    with raises(BadStatusCode):
        cap_api.get_schema(ana_type='some-type', record=True)


@responses.activate
def test_get_schema_version_not_found(cap_api):
    url = 'https://analysispreservation-dev.cern.ch/api/jsonschemas/some-type/0.0.5?resolve=True'
    responses.add(responses.GET,
                  url,
                  json={
                      'status': 404,
                      'message': 'Error'
                  },
                  status=404)

    with raises(BadStatusCode):
        cap_api.get_schema(ana_type='some-type', record=True)


@responses.activate
def test_get_schema_version_not_found(cap_api):
    url = 'https://analysispreservation-dev.cern.ch/api/jsonschemas/some-type/0.0.5?resolve=True'
    responses.add(responses.GET,
                  url,
                  json={
                      'status': 404,
                      'message': 'Error'
                  },
                  status=404)

    with raises(BadStatusCode):
        cap_api.get_schema(ana_type='some-type', version='0.0.5', record=True)
