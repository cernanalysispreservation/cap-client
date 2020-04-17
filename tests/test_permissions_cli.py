import json

import responses


# GET
@responses.activate
def test_permissions_get(cli_run):
    responses.add(
        responses.GET,
        "https://analysispreservation-dev.cern.ch/api/deposits/some-pid",
        json={
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
        },
        status=200)

    res = cli_run("permissions get -p some-pid")

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/permissions+json'
    assert res.exit_code == 0
    assert json.loads(res.stripped_output) == {
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


def test_permissions_get_no_pid_given(cli_run):
    res = cli_run("permissions get")

    assert res.exit_code == 2
    assert "Error: Missing option '--pid' / '-p'." in res.output


@responses.activate
def test_permissions_get_pid_not_exists(cli_run):
    responses.add(
        responses.GET,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={
            'status': 404,
            'message': 'PID does not exist.'
        },
        status=404)

    res = cli_run("permissions get -p some-pid")

    assert res.exit_code == 1
    assert res.stripped_output == 'PID does not exist.'


@responses.activate
def test_permissions_get_no_access(cli_run):
    responses.add(
        responses.GET,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={
            'message': "You don't have the permission to access the requested resource. "
            "It is either read-protected or not readable by the server.",
            'status': 403
        },
        status=403)

    res = cli_run("permissions get -p some-pid")

    assert res.exit_code == 1
    assert res.stripped_output == "You don't have sufficient permissions."


@responses.activate
def test_permissions_get_no_access_tokens(cli_run):
    responses.add(
        responses.GET,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={
            'message': "The server could not verify that you are authorized to "
            "access the URL requested.  You either supplied the wrong credentials "
            "(e.g. a bad password), or your browser doesn't understand how to supply the credentials required.",
            'status': 401
        },
        status=401)

    res = cli_run('permissions get -p some-pid')

    assert res.exit_code == 1
    assert res.stripped_output == 'You are not authorized to access the server (invalid access token?)'


# ADD
@responses.activate
def test_permissions_add(cli_run):
    responses.add(
        responses.POST,
        "https://analysispreservation-dev.cern.ch/api/deposits/some-pid/actions/permissions",
        json={
            'permissions': {
                "deposit-admin": {
                    "roles": [],
                    "users": ["info@inveniosoftware.org"]
                },
                "deposit-read": {
                    "roles": [],
                    "users": [
                        "info@inveniosoftware.org", "cms@inveniosoftware.org"
                    ]
                },
                "deposit-update": {
                    "roles": [],
                    "users": ["info@inveniosoftware.org"]
                }
            }
        },
        status=201)

    res = cli_run(
        "permissions add -p some-pid -u info@inveniosoftware.org -r read")

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/permissions+json'
    assert responses.calls[0].request.headers[
        'Content-Type'] == 'application/json'

    assert json.loads(responses.calls[0].request.body) == [{
        "email": "info@inveniosoftware.org",
        "type": "user",
        "op": "add",
        "action": "deposit-read"
    }]

    assert res.exit_code == 0
    assert json.loads(res.stripped_output) == {
        "deposit-admin": {
            "roles": [],
            "users": ["info@inveniosoftware.org"]
        },
        "deposit-read": {
            "roles": [],
            "users": ["info@inveniosoftware.org", "cms@inveniosoftware.org"]
        },
        "deposit-update": {
            "roles": [],
            "users": ["info@inveniosoftware.org"]
        }
    }


@responses.activate
def test_permissions_add_egroup(cli_run):
    responses.add(
        responses.POST,
        "https://analysispreservation-dev.cern.ch/api/deposits/some-pid/actions/permissions",
        json={
            'permissions': {
                "deposit-admin": {
                    "roles": [],
                    "users": ["info@inveniosoftware.org"]
                },
                "deposit-read": {
                    "roles": ['egroup@inveniosoftware.org'],
                    "users": ["info@inveniosoftware.org"]
                },
                "deposit-update": {
                    "roles": [],
                    "users": ["info@inveniosoftware.org"]
                }
            }
        },
        status=201)

    res = cli_run(
        "permissions add -p some-pid -e egroup@inveniosoftware.org -r read")

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/permissions+json'
    assert responses.calls[0].request.headers[
        'Content-Type'] == 'application/json'

    assert json.loads(responses.calls[0].request.body) == [{
        "email": "egroup@inveniosoftware.org",
        "type": "egroup",
        "op": "add",
        "action": "deposit-read"
    }]

    assert res.exit_code == 0
    assert json.loads(res.stripped_output) == {
        "deposit-admin": {
            "roles": [],
            "users": ["info@inveniosoftware.org"]
        },
        "deposit-read": {
            "roles": ['egroup@inveniosoftware.org'],
            "users": ["info@inveniosoftware.org"]
        },
        "deposit-update": {
            "roles": [],
            "users": ["info@inveniosoftware.org"]
        }
    }


def test_permissions_add_no_pid_given(cli_run):
    res = cli_run("permissions add -u cms@inveniosoftware.com -r read")

    assert res.exit_code == 2
    assert "Error: Missing option '--pid' / '-p'." in res.output


def test_permissions_add_no_user_given(cli_run):
    res = cli_run("permissions add -p some-pid -r read")

    assert res.exit_code == 2
    assert "Error: You need to specify --user or --egroup." in res.output


def test_permissions_add_no_rights_given(cli_run):
    res = cli_run("permissions add -p some-pid -u cms@inveniosoftware.com")

    assert res.exit_code == 2
    assert "Error: Missing option '--rights' / '-r'." in res.output


def test_permissions_add_wrong_rights_given(cli_run):
    res = cli_run(
        "permissions remove -p some-pid -u cms@inveniosoftware.com -r RAND")

    assert res.exit_code == 2
    assert "Error: Invalid value for '--rights' / '-r': " \
           "invalid choice: RAND. (choose from read, update, admin)" in res.output


def test_permissions_add_mutually_exclusive_user_egroup(cli_run):
    res = cli_run("permissions add -u user -e egroup")

    assert res.exit_code == 2
    assert "Error: --user is mutually exclusive with --egroup" in res.output


@responses.activate
def test_permissions_add_pid_not_exists(cli_run):
    responses.add(
        responses.POST,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid/actions/permissions',
        json={
            'status': 404,
            'message': 'PID does not exist.'
        },
        status=404)

    res = cli_run(
        "permissions add -p some-pid -u cms@inveniosoftware.com -r read")

    assert res.exit_code == 1
    assert res.stripped_output == 'PID does not exist.'


@responses.activate
def test_permissions_add_user_not_exists(cli_run):
    responses.add(
        responses.POST,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid/actions/permissions',
        json={
            'status': 400,
            'message': 'User with this mail does not exist in LDAP.'
        },
        status=400)

    res = cli_run(
        "permissions add -p some-pid -u cms@inveniosoftware.com -r read")

    assert res.exit_code == 1
    assert res.stripped_output == 'User with this mail does not exist in LDAP.'


@responses.activate
def test_permissions_add_no_access(cli_run):
    responses.add(
        responses.POST,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid/actions/permissions',
        json={
            'message': "You don't have the permission to access the requested resource. "
            "It is either read-protected or not readable by the server.",
            'status': 403
        },
        status=403)

    res = cli_run(
        "permissions add -p some-pid -u cms@inveniosoftware.com -r read")

    assert res.exit_code == 1
    assert res.stripped_output == "You don't have sufficient permissions."


@responses.activate
def test_permissions_add_no_access_tokens(cli_run):
    responses.add(
        responses.POST,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid/actions/permissions',
        json={
            'message': "The server could not verify that you are authorized to "
            "access the URL requested.  You either supplied the wrong credentials "
            "(e.g. a bad password), or your browser doesn't understand how to supply the credentials required.",
            'status': 401
        },
        status=401)

    res = cli_run(
        'permissions add -p some-pid -u cms@inveniosoftware.com -r read')

    assert res.exit_code == 1
    assert res.stripped_output == 'You are not authorized to access the server (invalid access token?)'


# REMOVE
@responses.activate
def test_permissions_remove(cli_run):
    responses.add(
        responses.POST,
        "https://analysispreservation-dev.cern.ch/api/deposits/some-pid/actions/permissions",
        json={
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
        },
        status=201)

    res = cli_run(
        "permissions remove -p some-pid -u info@inveniosoftware.org -r read")

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/permissions+json'
    assert responses.calls[0].request.headers[
        'Content-Type'] == 'application/json'

    assert json.loads(responses.calls[0].request.body) == [{
        "email": "info@inveniosoftware.org",
        "type": "user",
        "op": "remove",
        "action": "deposit-read"
    }]

    assert res.exit_code == 0
    assert json.loads(res.stripped_output) == {
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


@responses.activate
def test_permissions_remove_egroup(cli_run):
    responses.add(
        responses.POST,
        "https://analysispreservation-dev.cern.ch/api/deposits/some-pid/actions/permissions",
        json={
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
        },
        status=201)

    res = cli_run(
        "permissions remove -p some-pid -e egroup@inveniosoftware.org -r read")

    assert responses.calls[0].request.headers[
        'Accept'] == 'application/permissions+json'
    assert responses.calls[0].request.headers[
        'Content-Type'] == 'application/json'

    assert json.loads(responses.calls[0].request.body) == [{
        "email": "egroup@inveniosoftware.org",
        "type": "egroup",
        "op": "remove",
        "action": "deposit-read"
    }]

    assert res.exit_code == 0
    assert json.loads(res.stripped_output) == {
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


def test_permissions_remove_no_pid_given(cli_run):
    res = cli_run("permissions remove")

    assert res.exit_code == 2
    assert "Error: Missing option '--pid' / '-p'." in res.output


def test_permissions_remove_no_user_given(cli_run):
    res = cli_run("permissions remove -p some-pid -r read")

    assert res.exit_code == 2
    assert "Error: You need to specify --user or --egroup." in res.output


def test_permissions_remove_no_rights_given(cli_run):
    res = cli_run("permissions remove -p some-pid -u cms@inveniosoftware.com")

    assert res.exit_code == 2
    assert "Error: Missing option '--rights' / '-r'." in res.output


def test_permissions_remove_wrong_rights_given(cli_run):
    res = cli_run(
        "permissions remove -p some-pid -u cms@inveniosoftware.com -r RAND")

    assert res.exit_code == 2
    assert "Error: Invalid value for '--rights' / '-r': " \
           "invalid choice: RAND. (choose from read, update, admin)" in res.output


def test_permissions_remove_mutually_exclusive_user_egroup(cli_run):
    res = cli_run("permissions remove -u user -e egroup")

    assert res.exit_code == 2
    assert "Error: --user is mutually exclusive with --egroup" in res.output


@responses.activate
def test_permissions_remove_pid_not_exists(cli_run):
    responses.add(
        responses.POST,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid/actions/permissions',
        json={
            'status': 404,
            'message': 'PID does not exist.'
        },
        status=404)

    res = cli_run(
        "permissions remove -p some-pid -u cms@inveniosoftware.com -r read")

    assert res.exit_code == 1
    assert res.stripped_output == 'PID does not exist.'


@responses.activate
def test_permissions_remove_user_not_exists(cli_run):
    responses.add(
        responses.POST,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid/actions/permissions',
        json={
            'status': 400,
            'message': 'User with this mail does not exist in LDAP.'
        },
        status=400)

    res = cli_run(
        "permissions remove -p some-pid -u cms@inveniosoftware.com -r read")

    assert res.exit_code == 1
    assert res.stripped_output == 'User with this mail does not exist in LDAP.'


@responses.activate
def test_permissions_remove_no_access(cli_run):
    responses.add(
        responses.POST,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid/actions/permissions',
        json={
            'message': "You don't have the permission to access the requested resource. "
            "It is either read-protected or not readable by the server.",
            'status': 403
        },
        status=403)

    res = cli_run(
        "permissions remove -p some-pid -u cms@inveniosoftware.com -r read")

    assert res.exit_code == 1
    assert res.stripped_output == "You don't have sufficient permissions."


@responses.activate
def test_permissions_remove_no_access_tokens(cli_run):
    responses.add(
        responses.POST,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid/actions/permissions',
        json={
            'message': "The server could not verify that you are authorized to "
            "access the URL requested.  You either supplied the wrong credentials "
            "(e.g. a bad password), or your browser doesn't understand how to supply the credentials required.",
            'status': 401
        },
        status=401)

    res = cli_run(
        'permissions remove -p some-pid -u cms@inveniosoftware.com -r read')

    assert res.exit_code == 1
    assert res.stripped_output == 'You are not authorized to access the server (invalid access token?)'
