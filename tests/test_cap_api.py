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

from mock import mock_open, patch
from pytest import raises

from cap_client.errors import BadStatusCode, UnknownAnalysisType, \
    MissingJsonFile


@patch('requests.delete')
def test_make_request_send_request_with_correct_params(mock_requests,
                                                       cap_api, record_data):
    cap_api.access_token = 'random_access_token'
    endpoint = 'endpoint'
    method = 'delete'
    expected_status = 204
    mock_requests.return_value.status_code = expected_status

    cap_api._make_request(url=endpoint,
                          expected_status_code=expected_status,
                          method=method,
                          data=record_data)

    # get named args from requests.post call
    named_args = mock_requests.call_args[1]

    assert named_args['verify'] is False
    assert named_args['params']['access_token'] == 'random_access_token'
    assert named_args['headers']['Content-type'] == 'application/json'
    assert named_args['data'] == record_data


@patch('requests.get')
def test_make_request_when_request_successful(mock_requests, cap_api,
                                              record_data):
    mock_requests.return_value.status_code = 200
    mock_requests.return_value.json.return_value = record_data

    resp = cap_api._make_request(url='endpoint',
                                 expected_status_code=200)

    assert mock_requests.called
    assert resp == record_data


@patch('requests.get')
def test_make_request_when_request_fails(mock_requests, cap_api):
    mock_requests.return_value.status_code = 400

    with raises(BadStatusCode):
        cap_api._make_request(url='endpoint',
                              expected_status_code=200)


@patch('requests.post')
def test_make_request_when_sending_record_data(mock_requests, cap_api,
                                               record_data):
    with raises(BadStatusCode):
        cap_api._make_request(url='endpoint',
                              method='post',
                              data=record_data)

    # get named args from requests.post call
    named_args = mock_requests.call_args[1]

    # check that data was send in requests.post
    assert named_args['data'] == record_data


@patch('requests.delete')
def test_make_request_when_no_json_in_resp(mock_requests, cap_api):
    mock_requests.return_value.json.side_effect = ValueError()
    mock_requests.return_value.status_code = 204

    resp = cap_api._make_request(url='endpoint',
                                 expected_status_code=204,
                                 method='delete')

    # when no json in resp no error raised, just no data returned
    assert resp is None


@patch('requests.get')
def test_get_available_types_when_no_available_types(mock_requests, cap_api,
                                                     user_data):
    user_data['deposit_groups'] = []
    mock_requests.return_value.status_code = 200
    mock_requests.return_value.json.return_value = user_data

    types = cap_api._get_available_types()

    assert types == []


@patch('requests.get')
def test_get_method_with_given_pid(mock_requests, cap_api, record_data):
    mock_requests.return_value.status_code = 200
    mock_requests.return_value.json.return_value = record_data

    resp = cap_api.get('some_pid')

    assert resp == record_data


@patch('requests.get')
def test_get_field_when_field_unspecified(mock_requests, cap_api,
                                          record_data):
    mock_requests.return_value.status_code = 200
    mock_requests.return_value.json.return_value = record_data

    resp = cap_api.get_field('some_pid')

    assert resp == record_data['metadata']


@patch('requests.get')
def test_get_field_when_field_specified(mock_requests, cap_api,
                                        record_data):
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
    mock_requests.return_value.json.return_value = ''

    resp = cap_api.delete('some_pid')

    assert resp == ''


@patch('requests.get')
def test_types(mock_requests, cap_api, mocked_cap_api):
    mock_requests.return_value.status_code = 200
    mock_requests.return_value.json.return_value = ['atlas-workflows',
                                                    'alice-analysis']

    resp = cap_api.types()

    assert resp == ['atlas-workflows', 'alice-analysis']


# Public methods
@patch('requests.get')
def test_get_available_types_returns_all_available_types(mock_requests,
                                                         cap_api, user_data):
    mock_requests.return_value.status_code = 200
    mock_requests.return_value.json.return_value = user_data

    types = cap_api._get_available_types()

    assert 'atlas-workflows' in types
    assert 'alice-analysis' in types


@patch('requests.get')
def test_get_permissions(mock_requests, cap_api,
                         record_data):
    mock_requests.return_value.status_code = 200
    mock_requests.return_value.json.return_value = record_data

    resp = cap_api.get_permissions('some_pid')

    assert 'alice@inveniosoftware.org' in resp['metadata']['_access']['deposit-read']['user'][0]  # noqa


def test_create_method_when_no_type_given_returns_list_of_options(mocked_cap_api):  # noqa
    with raises(UnknownAnalysisType):
        mocked_cap_api.create(ana_type=None)


def test_create_method_when_type_given_not_in_available_options(mocked_cap_api):  # noqa
    with raises(UnknownAnalysisType):
        mocked_cap_api.create(ana_type='non-atlas-workflows')


def test_create_method_when_no_file_with_data_given(mocked_cap_api):
    with raises(MissingJsonFile):
        mocked_cap_api.create(ana_type='atlas-workflows')


@patch('__builtin__.open', new_callable=mock_open, read_data='{,}]')
def test_create_method_when_no_json_in_given_file(mock_open, mocked_cap_api):
    with raises(ValueError):
        mocked_cap_api.create(json_='file',
                              ana_type='atlas-workflows')


def test_create_method_when_validate_failed_raises_exception(mocked_cap_api,
                                                             record_data):
    json_data = json.dumps(record_data)
    with patch('__builtin__.open', new_callable=mock_open,
               read_data=json_data):
        mocked_cap_api._make_request.side_effect = [BadStatusCode(),
                                                    None]
        with raises(BadStatusCode):
            mocked_cap_api.create(json_='file',
                                  ana_type='atlas-workflows')


def test_update_method_when_no_file_with_data_given(mocked_cap_api):
    with raises(IOError):
        mocked_cap_api.update(pid='some_pid')


@patch('__builtin__.open', new_callable=mock_open, read_data='{,}]')
def test_update_method_when_no_json_in_given_file(mock_open, mocked_cap_api):
    with raises(ValueError):
        mocked_cap_api.update(filename='file')


def test_update_method_when_validate_failed_raises_exception(mocked_cap_api,
                                                             record_data):
    json_data = json.dumps(record_data)
    with patch('__builtin__.open', new_callable=mock_open,
               read_data=json_data):
        mocked_cap_api._make_request.side_effect = [BadStatusCode(),
                                                    None]
        with raises(BadStatusCode):
            mocked_cap_api.update(filename='file',
                                  pid='some_pid')


def test_update_method_when_success_returns_updated_data(mocked_cap_api,
                                                         record_data):
    json_data = json.dumps(record_data)

    with patch('__builtin__.open', new_callable=mock_open,
               read_data=json_data):
        mocked_cap_api._make_request.side_effect = [record_data]

        resp = mocked_cap_api.update(filename='file',
                                     pid='some_pid')

        assert resp == record_data


def test_patch_method(mocked_cap_api, record_data):
    json_data = json.dumps(record_data)

    with patch('__builtin__.open', new_callable=mock_open,
               read_data=json_data):
        mocked_cap_api._make_request.return_value = record_data

        resp = mocked_cap_api.patch(filename='file',
                                    pid='some_pid')

        named_args = mocked_cap_api._make_request.call_args[1]

        assert resp == record_data
        assert named_args['method'] == 'patch'
        assert named_args['headers'] == {
            'Content-Type': 'application/json-patch+json'
        }


def test_patch_method_when_no_file_with_data_given(mocked_cap_api):
    with raises(IOError):
        mocked_cap_api.patch(pid='some_pid')


@patch('__builtin__.open', new_callable=mock_open, read_data='{,}]')
def test_patch_method_when_no_json_in_given_file(mock_open, mocked_cap_api):
    with raises(ValueError):
        mocked_cap_api.patch(filename='file')


def test_set_field_when_setting_string_field(mocked_cap_api, record_data):
    mocked_cap_api._make_request.return_value = record_data

    mocked_cap_api.set_field('field_name.nested.nested2',
                             'field_val', 'some_pid')

    named_args = mocked_cap_api._make_request.call_args[1]
    sent_json = json.loads(named_args['data'])[0]

    assert sent_json['op'] == 'add'
    assert sent_json['path'] == '/field_name/nested/nested2'
    assert sent_json['value'] == 'field_val'


def test_set_field_when_appending_string_field_to_array(mocked_cap_api,
                                                        record_data):
    mocked_cap_api._make_request.return_value = record_data

    mocked_cap_api.set_field('field_name.nested.nested2',
                             'field_val', 'some_pid', append=True)

    named_args = mocked_cap_api._make_request.call_args[1]
    sent_json = json.loads(named_args['data'])[0]

    assert sent_json['op'] == 'add'
    assert sent_json['path'] == '/field_name/nested/nested2/-'
    assert sent_json['value'] == 'field_val'
