import json

import responses


# GET
@responses.activate
def test_repositories_get(cli_run):
    responses.add(
        responses.GET,
        "https://analysispreservation-dev.cern.ch/api/deposits/some-pid",
        json={
            'webhooks': [{
                'branch': 'test',
                'event_type': 'release',
                'host': 'github.com',
                'id': 1,
                'name': 'test-repo',
                'owner': 'test-user',
                'snapshots': []
            }]
        },
        status=200)

    res = cli_run("repositories get -p some-pid")

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/repositories+json'
    assert res.exit_code == 0
    assert json.loads(res.stripped_output) == [{
        "branch": 'test',
        "event_type": "release",
        "host": "github.com",
        "id": 1,
        "name": "test-repo",
        "owner": "test-user"
    }]


@responses.activate
def test_repositories_get_with_snapshots(cli_run):
    responses.add(
        responses.GET,
        "https://analysispreservation-dev.cern.ch/api/deposits/some-pid",
        json={
            'webhooks': [{
                'branch': 'test',
                'event_type': 'release',
                'host': 'github.com',
                'id': 1,
                'name': 'test-repo',
                'owner': 'test-user',
                'snapshots': []
            }]
        },
        status=200)

    res = cli_run("repositories get -p some-pid -ws")

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/repositories+json'
    assert res.exit_code == 0
    assert json.loads(res.stripped_output) == [{
        "branch": 'test',
        "event_type": "release",
        "host": "github.com",
        "id": 1,
        "name": "test-repo",
        "owner": "test-user",
        'snapshots': []
    }]


def test_repositories_get_no_pid_given(cli_run):
    res = cli_run("repositories get")

    assert res.exit_code == 2
    assert "Error: Missing option '--pid' / '-p'." in res.output


@responses.activate
def test_repositories_get_pid_not_exists(cli_run):
    responses.add(
        responses.GET,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={
            'status': 404,
            'message': 'PID does not exist.'
        },
        status=404)

    res = cli_run("repositories get -p some-pid")

    assert res.exit_code == 1
    assert res.stripped_output == 'PID does not exist.'


@responses.activate
def test_repositories_get_no_access(cli_run):
    responses.add(
        responses.GET,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={
            'message': "You don't have the permission to access the requested resource. "
            "It is either read-protected or not readable by the server.",
            'status': 403
        },
        status=403)

    res = cli_run("repositories get -p some-pid")

    assert res.exit_code == 1
    assert res.stripped_output == "You don't have sufficient permissions."


# UPLOAD
@responses.activate
def test_repositories_upload(cli_run):
    responses.add(
        responses.POST,
        "https://analysispreservation-dev.cern.ch/api/deposits/some-pid/actions/upload",
        status=201)

    res = cli_run(
        "repositories upload -p some-pid https://github.com/test-user/test-repo"
    )

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/repositories+json'
    assert responses.calls[0].request.headers[
        'Content-Type'] == 'application/json'

    assert json.loads(responses.calls[0].request.body) == {
        'url': 'https://github.com/test-user/test-repo',
        'webhook': False,
        'event_type': None
    }

    assert res.exit_code == 0
    assert res.stripped_output == 'Repository tarball was saved with your ' \
                                  'analysis files. (access using `cap-client files` methods)'


@responses.activate
def test_repositories_upload_repo_does_not_exist(cli_run):
    responses.add(
        responses.POST,
        "https://analysispreservation-dev.cern.ch/api/deposits/some-pid/actions/upload",
        json={
            'status': 400,
            'message': "This repository does not exist or you don't have access."
        },
        status=400)

    res = cli_run(
        "repositories upload -p some-pid https://github.com/test-user/no-exist-repo"
    )

    assert res.exit_code == 1
    assert res.stripped_output == "This repository does not exist or you don't have access."


@responses.activate
def test_repositories_upload_repo_not_valid(cli_run):
    responses.add(
        responses.POST,
        "https://analysispreservation-dev.cern.ch/api/deposits/some-pid/actions/upload",
        json={
            'status': 400,
            'message': 'Invalid git URL.'
        },
        status=400)

    res = cli_run(
        "repositories upload -p some-pid https://hubhub.com/test-user/test-repo"
    )

    assert res.exit_code == 1
    assert res.stripped_output == 'Invalid git URL.'


def test_repositories_upload_no_pid_given(cli_run):
    res = cli_run("repositories upload http://some-url")

    assert res.exit_code == 2
    assert "Error: Missing option '--pid' / '-p'." in res.output


def test_repositories_upload_no_url_given(cli_run):
    res = cli_run("repositories upload -p some-pid")

    assert res.exit_code == 2
    assert "Error: Missing argument 'URL'." in res.output


@responses.activate
def test_repositories_upload_no_access(cli_run):
    responses.add(
        responses.POST,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid/actions/upload',
        json={
            'message': "You don't have the permission to access the requested resource. "
            "It is either read-protected or not readable by the server.",
            'status': 403
        },
        status=403)

    res = cli_run(
        "repositories upload -p some-pid https://github.com/test-user/repo")

    assert res.exit_code == 1
    assert res.stripped_output == "You don't have sufficient permissions."


# CONNECT
@responses.activate
def test_repositories_connect(cli_run):
    responses.add(
        responses.POST,
        "https://analysispreservation-dev.cern.ch/api/deposits/some-pid/actions/upload",
        status=201)

    res = cli_run(
        "repositories connect -p some-pid https://github.com/test-user/test-repo --event release"
    )

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/repositories+json'
    assert responses.calls[0].request.headers[
        'Content-Type'] == 'application/json'

    assert json.loads(responses.calls[0].request.body) == {
        'url': 'https://github.com/test-user/test-repo',
        'webhook': True,
        'event_type': 'release'
    }

    assert res.exit_code == 0
    assert res.stripped_output == 'Repository was connected with analysis.\n' \
                                  'Now on every release, we will attach the latest version to your analysis.'


@responses.activate
def test_repositories_connect_default_release(cli_run):
    responses.add(
        responses.POST,
        "https://analysispreservation-dev.cern.ch/api/deposits/some-pid/actions/upload",
        status=201)

    res = cli_run(
        "repositories connect -p some-pid https://github.com/test-user/test-repo"
    )

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/repositories+json'
    assert responses.calls[0].request.headers[
        'Content-Type'] == 'application/json'

    assert json.loads(responses.calls[0].request.body) == {
        'url': 'https://github.com/test-user/test-repo',
        'webhook': True,
        'event_type': 'release'
    }

    assert res.exit_code == 0
    assert res.stripped_output == 'Repository was connected with analysis.\n' \
                                  'Now on every release, we will attach the latest version to your analysis.'


@responses.activate
def test_repositories_connect_repo_not_valid(cli_run):
    responses.add(
        responses.POST,
        "https://analysispreservation-dev.cern.ch/api/deposits/some-pid/actions/upload",
        json={
            'status': 400,
            'message': 'Invalid git URL.'
        },
        status=400)

    res = cli_run(
        "repositories connect -p some-pid https://hubhub.com/test-user/test-repo --event release"
    )

    assert res.exit_code == 1
    assert res.stripped_output == 'Invalid git URL.'


@responses.activate
def test_repositories_connect_repo_already_connected(cli_run):
    responses.add(
        responses.POST,
        "https://analysispreservation-dev.cern.ch/api/deposits/some-pid/actions/upload",
        json={
            'status': 400,
            'message': 'Analysis already connected with release webhook.'
        },
        status=400)

    res = cli_run(
        "repositories connect -p some-pid https://github.com/test-user/test-repo --event release"
    )

    assert res.exit_code == 1
    assert res.stripped_output == 'Analysis already connected with release webhook.'


def test_repositories_connect_no_pid_given(cli_run):
    res = cli_run("repositories connect http://some-url")

    assert res.exit_code == 2
    assert "Error: Missing option '--pid' / '-p'." in res.output


def test_repositories_connect_no_url_given(cli_run):
    res = cli_run("repositories connect -p some-pid")

    assert res.exit_code == 2
    assert "Error: Missing argument 'URL'." in res.output


@responses.activate
def test_repositories_connect_pid_not_exists(cli_run):
    responses.add(
        responses.POST,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid/actions/upload',
        json={
            'status': 404,
            'message': 'PID does not exist.'
        },
        status=404)

    res = cli_run(
        "repositories connect -p some-pid https://github.com/test-user/no-exist-repo --event release"
    )

    assert res.exit_code == 1
    assert res.stripped_output == 'PID does not exist.'


@responses.activate
def test_repositories_connect_no_access(cli_run):
    responses.add(
        responses.POST,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid/actions/upload',
        json={
            'message': "You don't have the permission to access the requested resource. "
            "It is either read-protected or not readable by the server.",
            'status': 403
        },
        status=403)

    res = cli_run(
        "repositories connect -p some-pid https://github.com/test-user/repo --event release"
    )

    assert res.exit_code == 1
    assert res.stripped_output == "You don't have sufficient permissions."
