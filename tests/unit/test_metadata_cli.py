import json

import responses
from pytest import mark


# GET
@responses.activate
def test_metadata_get(cli_run):
    responses.add(
        responses.GET,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={'metadata': {
            "general_title": "test"
        }},
        status=200)

    res = cli_run("metadata get -p some-pid")

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/basic+json'
    assert res.exit_code == 0
    assert json.loads(res.stripped_output) == {"general_title": "test"}


@responses.activate
def test_metadata_get_field(cli_run):
    responses.add(
        responses.GET,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={'metadata': {
            "general_title": "test"
        }},
        status=200)

    res = cli_run("metadata get -p some-pid --field general_title")

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/basic+json'
    assert res.exit_code == 0
    assert res.stripped_output == '"test"'


@responses.activate
def test_metadata_get_field_not_exists(cli_run):
    responses.add(
        responses.GET,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={'metadata': {
            "general_title": "test"
        }},
        status=200)

    res = cli_run("metadata get -p some-pid --field myfield")

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/basic+json'
    assert res.exit_code == 2
    assert 'Error: The field myfield does not exist. Try a different field.' in res.stripped_output


@responses.activate
def test_metadata_get_index_not_exists(cli_run):
    responses.add(
        responses.GET,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={'metadata': {
            "basic_info": {
                "ana_notes": ["ANA-1", "ANA-2"]
            }
        }},
        status=200)
    res = cli_run("metadata get -p some-pid --field basic_info.ana_notes.3")

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/basic+json'
    assert res.exit_code == 2
    assert 'Error: The index you are trying to access does not exist.' in res.stripped_output


@responses.activate
def test_metadata_get_pid_not_exists(cli_run):
    responses.add(
        responses.GET,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={
            'status': 404,
            'message': 'PID does not exist.'
        },
        status=404)

    res = cli_run("metadata get -p some-pid")

    assert res.exit_code == 1
    assert res.stripped_output == 'PID does not exist.'


@responses.activate
def test_metadata_no_access(cli_run):
    responses.add(
        responses.GET,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={
            'message': "You don't have the permission to access the requested resource. "
            "It is either read-protected or not readable by the server.",
            'status': 403
        },
        status=403)

    res = cli_run("metadata get -p some-pid")

    assert res.exit_code == 1
    assert res.stripped_output == "You don't have sufficient permissions."


def test_metadata_get_no_pid_given(cli_run):
    res = cli_run("metadata get")

    assert res.exit_code == 2
    assert "Error: Missing option '--pid' / '-p'." in res.output


# UPDATE
@mark.skip
@responses.activate
def test_metadata_update_with_text_field_str(cli_run):
    responses.add(
        responses.PATCH,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={'metadata': {
            "general_title": "new-test"
        }},
        status=200)

    res = cli_run(
        "metadata update -p some-pid --field general_title --json new-test")

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/basic+json'
    assert responses.calls[0].request.headers[
        'Content-Type'] == 'application/json-patch+json'

    assert json.loads(responses.calls[0].request.body) == [{
        'op': 'replace',
        'path': '/general_title',
        'value': 'new-test'
    }]
    assert res.exit_code == 0
    assert json.loads(res.stripped_output) == {
        'metadata': {
            "general_title": "new-test"
        }
    }


@responses.activate
def test_metadata_update_with_text(cli_run):
    responses.add(
        responses.PATCH,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={'metadata': {
            "general_title": "new-test"
        }},
        status=200)

    res = cli_run(
        "metadata update -p some-pid --field general_title -t new-test")

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/basic+json'
    assert responses.calls[0].request.headers[
        'Content-Type'] == 'application/json-patch+json'

    assert json.loads(responses.calls[0].request.body) == [{
        'op': 'replace',
        'path': '/general_title',
        'value': 'new-test'
    }]

    assert res.exit_code == 0
    assert json.loads(res.stripped_output) == {
        'metadata': {
            "general_title": "new-test"
        }
    }


@mark.skip
@responses.activate
def test_metadata_update_with_text_field_int(cli_run):
    responses.add(
        responses.PATCH,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={'metadata': {
            "myfield": 10
        }},
        status=200)

    res = cli_run("metadata update -p some-pid --field myfield --json 10")

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/basic+json'
    assert responses.calls[0].request.headers[
        'Content-Type'] == 'application/json-patch+json'
    assert json.loads(responses.calls[0].request.body) == [{
        'op': 'replace',
        'path': '/myfield',
        'value': 10
    }]
    assert res.exit_code == 0
    assert json.loads(res.stripped_output) == {'metadata': {'myfield': 10}}


@responses.activate
def test_metadata_update_with_num_int(cli_run):
    responses.add(
        responses.PATCH,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={'metadata': {
            "myfield": 10
        }},
        status=200)

    res = cli_run("metadata update -p some-pid --field myfield -n 10")

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/basic+json'
    assert responses.calls[0].request.headers[
        'Content-Type'] == 'application/json-patch+json'

    assert json.loads(responses.calls[0].request.body) == [{
        'op': 'replace',
        'path': '/myfield',
        'value': 10
    }]

    assert res.exit_code == 0
    assert json.loads(res.stripped_output) == {'metadata': {'myfield': 10}}


@mark.skip
@responses.activate
def test_metadata_update_with_text_field_float(cli_run):
    responses.add(
        responses.PATCH,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={'metadata': {
            "myfield": 1.2
        }},
        status=200)

    res = cli_run("metadata update -p some-pid --field myfield --json 1.2")

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/basic+json'
    assert responses.calls[0].request.headers[
        'Content-Type'] == 'application/json-patch+json'
    assert json.loads(responses.calls[0].request.body) == [{
        'op': 'replace',
        'path': '/myfield',
        'value': 1.2
    }]
    assert res.exit_code == 0
    assert json.loads(res.stripped_output) == {'metadata': {'myfield': 1.2}}


@responses.activate
def test_metadata_update_with_num_float(cli_run):
    responses.add(
        responses.PATCH,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={'metadata': {
            "myfield": 1.2
        }},
        status=200)

    res = cli_run("metadata update -p some-pid --field myfield -n 1.2")

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/basic+json'
    assert responses.calls[0].request.headers[
        'Content-Type'] == 'application/json-patch+json'

    assert json.loads(responses.calls[0].request.body) == [{
        'op': 'replace',
        'path': '/myfield',
        'value': 1.2
    }]

    assert res.exit_code == 0
    assert json.loads(res.stripped_output) == {'metadata': {'myfield': 1.2}}


@responses.activate
def test_metadata_update_with_json(cli_run):
    responses.add(
        responses.PUT,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={'metadata': {
            "basic_info": {
                "abstract": "test"
            }
        }},
        status=200)

    res = cli_run('metadata update -p some-pid '
                  '--json {"basic_info":{"abstract":"test"}}')

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/basic+json'
    assert json.loads(responses.calls[0].request.body) == {
        "basic_info": {
            "abstract": "test"
        }
    }
    assert res.exit_code == 0


@responses.activate
def test_metadata_update_when_data_in_jsonfile(runner):
    responses.add(
        responses.PUT,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        content_type='application/basic+json',
        json={'metadata': {
            "basic_info": {
                "abstract": "test"
            }
        }},
        status=200)

    with runner.isolated_filesystem():
        with open('file.json', 'w+') as fp:
            json.dump({"basic_info": {"abstract": "test"}}, fp)

        res = runner.run("metadata update -p some-pid --jsonfile file.json")

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/basic+json'
    assert json.loads(responses.calls[0].request.body) == {
        "basic_info": {
            "abstract": "test"
        }
    }
    assert res.exit_code == 0


@responses.activate
def test_metadata_update_when_given_field_and_data_in_json(cli_run):
    responses.add(
        responses.PATCH,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={'metadata': {
            "basic_info": {
                "authors": [{
                    "name": "pam"
                }]
            }
        }},
        status=200)

    res = cli_run(
        'metadata update -p some-pid --field basic_info.authors.0 --json {"name":"pam"}'
    )

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/basic+json'
    assert responses.calls[0].request.headers[
        'Content-Type'] == 'application/json-patch+json'
    assert json.loads(responses.calls[0].request.body) == [{
        'op': 'replace',
        'path': '/basic_info/authors/0',
        'value': {
            "name": "pam"
        }
    }]

    assert res.exit_code == 0
    assert json.loads(res.stripped_output) == {
        'metadata': {
            "basic_info": {
                "authors": [
                    {
                        "name": "pam"
                    },
                ]
            }
        }
    }


def test_metadata_update_no_pid_given(cli_run):
    res = cli_run("metadata update")

    assert res.exit_code == 2
    assert "Error: Missing option '--pid' / '-p'." in res.output


def test_metadata_update_no_input_options_given(cli_run):
    res = cli_run("metadata update -p some-pid --field field")

    assert res.exit_code == 2
    assert "Error: You need to specify one of --json, --jsonfile, --text, --num." in res.output


def test_metadata_update_mutually_exclusive_json_with_others(cli_run):
    res = cli_run("metadata update -p some-pid -j json -f json-file")

    assert res.exit_code == 2
    assert "Error: --json is mutually exclusive with --jsonfile, --text, --num" in res.output


def test_metadata_update_mutually_exclusive_jsonfile_with_others(cli_run):
    res = cli_run("metadata update -p some-pid -f json-file -j json")

    assert res.exit_code == 2
    assert "Error: --jsonfile is mutually exclusive with --json, --text, --num" in res.output


def test_metadata_update_mutually_exclusive_text_with_others(cli_run):
    res = cli_run("metadata update -p some-pid -t text -f json-file")

    assert res.exit_code == 2
    assert "Error: --text is mutually exclusive with --jsonfile, --json, --num" in res.output


def test_metadata_update_mutually_exclusive_num_with_others(cli_run):
    res = cli_run("metadata update -p some-pid -n number -f json-file")

    assert res.exit_code == 2
    assert "Error: --num is mutually exclusive with --jsonfile, --json, --text" in res.output


# REMOVE
@responses.activate
def test_metadata_remove(cli_run):
    responses.add(
        responses.PATCH,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={'metadata': {}},
        status=200)

    res = cli_run("metadata remove -p some-pid --field general_title")

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/basic+json'
    assert responses.calls[0].request.headers[
        'Content-type'] == 'application/json-patch+json'

    assert json.loads(responses.calls[0].request.body) == [{
        'op': 'remove',
        'path': '/general_title',
    }]

    assert res.exit_code == 0
    assert json.loads(res.stripped_output) == {}


@responses.activate
def test_metadata_remove_pid_not_exists(cli_run):
    responses.add(
        responses.PATCH,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={
            'status': 404,
            'message': 'PID does not exist.'
        },
        status=404)

    res = cli_run("metadata remove -p some-pid --field general-title")

    assert res.exit_code == 1
    assert res.stripped_output == 'PID does not exist.'


@responses.activate
def test_metadata_remove_no_access(cli_run):
    responses.add(
        responses.PATCH,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={
            'message': "You don't have the permission to access the requested resource. "
            "It is either read-protected or not readable by the server.",
            'status': 403
        },
        status=403)

    res = cli_run("metadata remove -p some-pid --field general-title")

    assert res.exit_code == 1
    assert res.stripped_output == "You don't have sufficient permissions."


def test_metadata_remove_no_pid_given(cli_run):
    res = cli_run("metadata remove")

    assert res.exit_code == 2
    assert "Error: Missing option '--pid' / '-p'." in res.output


def test_metadata_remove_no_field_given(cli_run):
    res = cli_run("metadata remove -p some-pid")

    assert res.exit_code == 2
    assert "Error: Missing option '--field'." in res.output
