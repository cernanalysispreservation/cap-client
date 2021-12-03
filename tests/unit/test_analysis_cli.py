import json
from tempfile import NamedTemporaryFile

import responses
from cap_client.utils import json_dumps


@responses.activate
def test_analysis_types(cli_run):
    responses.add(
        responses.GET,
        "https://analysispreservation-dev.cern.ch/api/me",
        json={
            "deposit_groups": [{
                "deposit_group": "atlas-workflows",
                "description": "Create an ATLAS Workflow",
                "name": "ATLAS Workflow"
            }, {
                "deposit_group": "alice-analysis",
                "description": "Create an ALICE Analysis",
                "name": "ALICE Analysis"
            }],
            "email": "my_mail@cern.ch",
            "id": 1
        },
    )

    res = cli_run("analysis types")

    assert res.exit_code == 0
    assert res.stripped_output == json_dumps(
        ["atlas-workflows", "alice-analysis"])


@responses.activate
def test_analysis_types_when_no_types_for_this_user(cli_run):
    responses.add(
        responses.GET,
        "https://analysispreservation-dev.cern.ch/api/me",
        json={
            "deposit_groups": [],
            "email": "my_mail@cern.ch",
            "id": 1
        },
    )

    res = cli_run("analysis types")

    assert res.exit_code == 0
    assert res.stripped_output == json_dumps([])


@responses.activate
def test_analysis_schema(cli_run):
    responses.add(
        responses.GET,
        'https://analysispreservation-dev.cern.ch/api/jsonschemas/some-type?resolve=True',
        json={
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
        },
    )

    res = cli_run("analysis schema some-type")

    assert json.loads(res.stripped_output) == {
        'title': 'Test',
        'properties': {
            'basic_info': {
                'id': 'basic_info',
                'title': 'Basic Information'
            },
        }
    }


@responses.activate
def test_analysis_schema_when_asked_for_published_schema(cli_run):
    responses.add(
        responses.GET,
        'https://analysispreservation-dev.cern.ch/api/jsonschemas/some-type/0.0.1?resolve=True',
        json={
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
        })

    res = cli_run("analysis schema some-type --version 0.0.1 --for-published")

    assert res.exit_code == 0
    assert json.loads(res.stripped_output) == {
        'title': 'Record Test',
        'properties': {
            'basic_info': {
                'id': 'basic_info',
                'title': 'Basic Information'
            },
        }
    }


@responses.activate
def test_analysis_schema_when_schema_with_this_type_does_not_exist(cli_run):
    responses.add(
        responses.GET,
        'https://analysispreservation-dev.cern.ch/api/jsonschemas/non-existing-type?resolve=True',
        json={
            "message": "The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.",
            "status": 404
        },
        status=404,
    )

    res = cli_run("analysis schema non-existing-type")

    assert res.exit_code == 1
    assert res.stripped_output == 'Schema non-existing-type does not exist.'


def test_analysis_schema_when_invalid_version_format(cli_run):
    res = cli_run("analysis schema some-type --version 0a0b0c")

    assert res.exit_code == 2
    assert ("Error: Invalid value for '--version': "
            "Version has to be passed as string <major>.<minor>.<patch>"
            ) in res.stripped_output


def test_analysis_schema_when_type_not_provided(cli_run):
    res = cli_run("analysis schema --version 0.0.1")

    assert res.exit_code == 2
    assert "Error: Missing argument 'ANALYSIS_TYPE'." in res.stripped_output


@responses.activate
def test_create_method_when_success_returns_newly_created_deposit_via_basic_serializer(
        cli_run):
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
                      "metadata": {
                          "title": "my_analysis"
                      },
                  },
                  status=201)
    responses.add(
        responses.PUT,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={
            "created": "2020-03-25T09:25:19.578823+00:00",
            "metadata": {
                "title": "my_analysis"
            },
            "pid": "some-pid",
            "updated": "2020-03-25T09:25:19.904106+00:00"
        },
    )

    res = cli_run('analysis create --type lhcb --json {"title":"my_analysis"}')

    assert json.loads(responses.calls[0].request.body) == {
        "$ana_type": "lhcb",
        "title": "my_analysis"
    }

    assert responses.calls[0].request.headers[
        'Content-Type'] == 'application/json'
    assert responses.calls[1].request.headers[
        'Accept'] == 'application/basic+json'
    assert responses.calls[1].request.headers[
        'Content-Type'] == 'application/json'
    assert json.loads(res.output) == {
        "updated": "2020-03-25T09:25:19.904106+00:00",
        "created": "2020-03-25T09:25:19.578823+00:00",
        "pid": "some-pid",
        "metadata": {
            "title": "my_analysis"
        }
    }


def test_analysis_create_when_no_json_nor_jsonfile_provided(cli_run):
    res = cli_run("analysis create --type some-type")

    assert res.exit_code == 2
    assert 'Error: You need to specify one of --json, --jsonfile.' in res.output


def test_analysis_create_when_both_json_and_jsonfile_provided(cli_run):
    res = cli_run(
        "analysis create --type some-type --json {} --jsonfile file.json")

    assert res.exit_code == 2
    assert 'Error: --json is mutually exclusive with --jsonfile' in res.output


def test_analysis_create_when_both_type_and_schema_in_json_provided(cli_run):
    res = cli_run(
        'analysis create --type some-type --json {"$schema":"https://analysispreservation-dev.cern.ch/schemas/cms.json"}'
    )

    assert res.exit_code == 2
    assert 'Error: Your JSON data already provides $schema - --type/-t parameter forbidden.' in res.output


def test_analysis_create_when_no_type_nor_schema_in_json_provided(cli_run):
    res = cli_run('analysis create --json {}')

    assert res.exit_code == 2
    assert 'Error: You need to provide the --type/-t parameter OR add $schema field in your JSON data.' in res.output


def test_analysis_create_when_json_with_not_json_data_provided(cli_run):
    res = cli_run('analysis create --json {a')

    assert res.exit_code == 2
    assert "Error: Invalid value for '--json' / '-j': Not a valid JSON." in res.stripped_output


def test_analysis_create_when_json_with_not_json_object_provided(cli_run):
    res = cli_run('analysis create --json []')

    assert res.exit_code == 2
    assert 'Error: Not a JSON object.' in res.output


def test_analysis_create_when_jsonfile_with_not_json_data_provided(cli_run):
    with NamedTemporaryFile('r+') as f:
        res = cli_run('analysis create --jsonfile {}'.format(f.name))

    assert res.exit_code == 2
    assert "Error: Invalid value for '--jsonfile' / '-f': Not a valid JSON." in res.stripped_output


@responses.activate
def test_analysis_create_when_non_existing_schema_type(cli_run):
    responses.add(responses.POST,
                  'https://analysispreservation-dev.cern.ch/api/deposits/',
                  json={
                      'status': 400,
                      'message': 'Schema doesnt exist.'
                  },
                  status=400)

    res = cli_run(
        'analysis create --type non-exiting-type --json {"title":"my_analysis"}'
    )

    assert json.loads(responses.calls[0].request.body) == {
        "$ana_type": "non-exiting-type",
        "title": "my_analysis"
    }
    assert res.exit_code == 1
    assert res.stripped_output == 'Schema doesnt exist.'


@responses.activate
def test_analysis_create_when_validation_error(cli_run):
    responses.add(
        responses.POST,
        'https://analysispreservation-dev.cern.ch/api/deposits/',
        json={
            "status": 400,
            "message": "Validation error. Try again with valid data",
            "errors": [{
                "field": [],
                "message": "Additional properties are not allowed ('title' was unexpected)"
            }]
        },
        status=400)

    res = cli_run(
        'analysis create --type analysis-type --json {"title":"my_analysis"}')

    assert json.loads(responses.calls[0].request.body) == {
        "$ana_type": "analysis-type",
        "title": "my_analysis"
    }
    assert res.exit_code == 1
    assert ('Validation error. Try again with valid data\n'
            'Additional properties are not allowed (\'title\' was unexpected)'
            ) in res.stripped_output


# GET
@responses.activate
def test_analysis_get_drafts(cli_run):
    responses.add(responses.GET,
                  'https://analysispreservation-dev.cern.ch/api/deposits/',
                  json={
                      'aggregations': {},
                      'hits': {
                          'hits': [{
                              'metadata': {
                                  'general_title': 'test-1'
                              },
                              'pid': 'some-pid-1',
                          }, {
                              'metadata': {
                                  'general_title': 'test-2'
                              },
                              'pid': 'some-pid-2',
                          }],
                          'total': 2
                      }
                  },
                  status=200)

    res = cli_run('analysis get')

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/basic+json'
    assert res.exit_code == 0
    assert json.loads(res.stripped_output) == [{
        'metadata': {
            'general_title': 'test-1'
        },
        'pid': 'some-pid-1',
    }, {
        'metadata': {
            'general_title': 'test-2'
        },
        'pid': 'some-pid-2',
    }]


@responses.activate
def test_analysis_get_drafts_with_page(cli_run):
    responses.add(responses.GET,
                  'https://analysispreservation-dev.cern.ch/api/deposits/',
                  json={
                      'aggregations': {},
                      'hits': {
                          'hits': [{
                              'metadata': {
                                  'general_title': 'test-1'
                              },
                              'pid': 'some-pid-1',
                          }, {
                              'metadata': {
                                  'general_title': 'test-2'
                              },
                              'pid': 'some-pid-2',
                          }],
                          'total': 2
                      }
                  },
                  status=200)

    res = cli_run('analysis get --page 1')

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/basic+json'
    assert res.exit_code == 0
    assert json.loads(res.stripped_output) == [{
        'metadata': {
            'general_title': 'test-1'
        },
        'pid': 'some-pid-1',
    }, {
        'metadata': {
            'general_title': 'test-2'
        },
        'pid': 'some-pid-2',
    }]


@responses.activate
def test_analysis_get_draft_by_pid(cli_run):
    responses.add(
        responses.GET,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={
            'metadata': {
                'basic_info': {
                    'abstract': 'test',
                },
                'general_title': 'test-title'
            },
            'pid': 'some-pid'
        },
        status=200)

    res = cli_run('analysis get -p some-pid')

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/basic+json'
    assert res.exit_code == 0
    assert json.loads(res.stripped_output) == {
        'metadata': {
            'basic_info': {
                'abstract': 'test',
            },
            'general_title': 'test-title'
        },
        'pid': 'some-pid'
    }


@responses.activate
def test_analysis_get_draft_by_pid_when_pid_not_exists(cli_run):
    responses.add(
        responses.GET,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={
            'status': 404,
            'message': 'PID does not exist.'
        },
        status=404)

    res = cli_run('analysis get -p some-pid')

    assert res.exit_code == 1
    assert res.stripped_output == 'PID does not exist.'


@responses.activate
def test_analysis_get_draft_by_pid_when_no_access(cli_run):
    responses.add(
        responses.GET,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={
            'message': "You don't have the permission to access the requested resource. "
            "It is either read-protected or not readable by the server.",
            'status': 403
        },
        status=403)

    res = cli_run('analysis get -p some-pid')

    assert res.exit_code == 1
    assert res.stripped_output == "You don't have sufficient permissions."


@responses.activate
def test_analysis_get_drafts_no_access_tokens(cli_run):
    responses.add(
        responses.GET,
        'https://analysispreservation-dev.cern.ch/api/deposits/',
        json={
            'message': "The server could not verify that you are authorized to "
            "access the URL requested.  You either supplied the wrong credentials "
            "(e.g. a bad password), or your browser doesn't understand how to supply the credentials required.",
            'status': 401
        },
        status=401)

    res = cli_run('analysis get')

    assert res.exit_code == 1
    assert res.stripped_output == 'You are not authorized to access the server (invalid access token?)'


@responses.activate
def test_analysis_get_published(cli_run):
    responses.add(responses.GET,
                  'https://analysispreservation-dev.cern.ch/api/records/',
                  json={
                      'aggregations': {},
                      'hits': {
                          'hits': [{
                              'metadata': {
                                  'general_title': 'test-1'
                              },
                              'pid': 'some-pid-1',
                              'recid': 'some-pid-1',
                          }, {
                              'metadata': {
                                  'general_title': 'test-2'
                              },
                              'pid': 'some-pid-2',
                              'recid': 'some-pid-2',
                          }],
                          'total': 2
                      }
                  },
                  status=200)

    res = cli_run('analysis get-published')

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/basic+json'
    assert res.exit_code == 0
    assert json.loads(res.stripped_output) == [{
        'metadata': {
            'general_title': 'test-1'
        },
        'pid': 'some-pid-1',
        "recid": "some-pid-1"
    }, {
        'metadata': {
            'general_title': 'test-2'
        },
        'pid': 'some-pid-2',
        "recid": "some-pid-2"
    }]


@responses.activate
def test_analysis_get_published_by_pid(cli_run):
    responses.add(
        responses.GET,
        'https://analysispreservation-dev.cern.ch/api/records/some-pid',
        json={
            "metadata": {
                "general_title": "test",
            },
            "pid": "some-pid",
            "recid": "some-pid",
        },
        status=200)

    res = cli_run('analysis get-published -p some-pid')

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/basic+json'
    assert res.exit_code == 0
    assert json.loads(res.stripped_output) == {
        "metadata": {
            "general_title": "test",
        },
        "pid": "some-pid",
        "recid": "some-pid",
    }


@responses.activate
def test_analysis_get_published_by_pid_when_pid_not_exists(cli_run):
    responses.add(
        responses.GET,
        'https://analysispreservation-dev.cern.ch/api/records/some-pid',
        json={
            'status': 404,
            'message': 'PID does not exist.'
        },
        status=404)

    res = cli_run('analysis get-published -p some-pid')

    assert res.exit_code == 1
    assert res.stripped_output == 'PID does not exist.'


@responses.activate
def test_analysis_get_published_by_pid_when_no_access(cli_run):
    responses.add(
        responses.GET,
        'https://analysispreservation-dev.cern.ch/api/records/some-pid',
        json={
            'message': "You don't have the permission to access the requested resource. "
            "It is either read-protected or not readable by the server.",
            'status': 403
        },
        status=403)

    res = cli_run('analysis get-published -p some-pid')

    assert res.exit_code == 1
    assert res.stripped_output == "You don't have sufficient permissions."


@responses.activate
def test_analysis_get_published_no_access_tokens(cli_run):
    responses.add(
        responses.GET,
        'https://analysispreservation-dev.cern.ch/api/records/',
        json={
            'message': "The server could not verify that you are authorized to "
            "access the URL requested.  You either supplied the wrong credentials "
            "(e.g. a bad password), or your browser doesn't understand how to supply the credentials required.",
            'status': 401
        },
        status=401)

    res = cli_run('analysis get-published')

    assert res.exit_code == 1
    assert res.stripped_output == 'You are not authorized to access the server (invalid access token?)'


# PUBLISH
@responses.activate
def test_analysis_publish(cli_run):
    responses.add(
        responses.POST,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid/actions/publish',
        json={
            'metadata': {
                'general_title': 'test'
            },
            'pid': 'some-pid',
            'recid': 'some-record-pid',
        },
        status=202)

    res = cli_run('analysis publish -p some-pid')

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/basic+json'
    assert res.exit_code == 0
    assert 'Your analysis has been published with PID: some-record-pid' in res.stripped_output


@responses.activate
def test_analysis_publish_when_pid_not_exists(cli_run):
    responses.add(
        responses.POST,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid/actions/publish',
        json={
            'status': 404,
            'message': 'PID does not exist.'
        },
        status=404)

    res = cli_run('analysis publish -p some-pid')

    assert res.exit_code == 1
    assert res.stripped_output == 'PID does not exist.'


@responses.activate
def test_analysis_publish_when_no_access(cli_run):
    responses.add(
        responses.POST,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid/actions/publish',
        json={
            'message': 'Forbidden',
            'status': 403
        },
        status=403)

    res = cli_run('analysis publish -p some-pid')

    assert res.exit_code == 1
    assert res.stripped_output == "You don't have sufficient permissions."


@responses.activate
def test_analysis_publish_no_access_tokens(cli_run):
    responses.add(
        responses.POST,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid/actions/publish',
        json={
            'message': "The server could not verify that you are authorized to "
            "access the URL requested.  You either supplied the wrong credentials "
            "(e.g. a bad password), or your browser doesn't understand how to supply the credentials required.",
            'status': 401
        },
        status=401)

    res = cli_run('analysis publish -p some-pid')

    assert res.exit_code == 1
    assert res.stripped_output == 'You are not authorized to access the server (invalid access token?)'


# DELETE
@responses.activate
def test_analysis_delete(cli_run):
    responses.add(
        responses.DELETE,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        body='',
        status=204)

    res = cli_run('analysis delete -p some-pid')

    assert res.exit_code == 0
    assert 'Analysis "some-pid" has been deleted.' in res.stripped_output


@responses.activate
def test_analysis_delete_when_pid_not_exists(cli_run):
    responses.add(
        responses.DELETE,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={
            'status': 404,
            'message': 'PID does not exist.'
        },
        status=404)

    res = cli_run('analysis delete -p some-pid')

    assert res.exit_code == 1
    assert res.stripped_output == 'PID does not exist.'


@responses.activate
def test_analysis_delete_when_no_access(cli_run):
    responses.add(
        responses.DELETE,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={
            'message': 'Forbidden',
            'status': 403
        },
        status=403)

    res = cli_run('analysis delete -p some-pid')

    assert res.exit_code == 1
    assert res.stripped_output == "You don't have sufficient permissions."


@responses.activate
def test_analysis_delete_no_access_tokens(cli_run):
    responses.add(
        responses.DELETE,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={
            'message': "The server could not verify that you are authorized to "
            "access the URL requested.  You either supplied the wrong credentials "
            "(e.g. a bad password), or your browser doesn't understand how to supply the credentials required.",
            'status': 401
        },
        status=401)

    res = cli_run('analysis delete -p some-pid')

    assert res.exit_code == 1
    assert res.stripped_output == 'You are not authorized to access the server (invalid access token?)'
