import json
import os

import responses


@responses.activate
def test_files_get(cli_run):
    responses.add(
        responses.GET,
        "https://analysispreservation-dev.cern.ch/api/deposits/some-pid/files",
        json=[{
            "id": "c033caa6-a97e-4f10-92e8-50193eebb6c5",
            "filename": "test.txt",
            "filesize": 10,
            "checksum": "md5:5065fe1d609d403918ac99b172b88ace"
        }],
        status=200)

    res = cli_run("files get -p some-pid")

    assert res.exit_code == 0
    assert json.loads(res.stripped_output) == [{
        "id": "c033caa6-a97e-4f10-92e8-50193eebb6c5",
        "filename": "test.txt",
        "filesize": 10,
        "checksum": "md5:5065fe1d609d403918ac99b172b88ace"
    }]


def test_files_get_no_pid_given(cli_run):
    res = cli_run("files get")

    assert res.exit_code == 2
    assert "Error: Missing option '--pid' / '-p'." in res.output


@responses.activate
def test_files_get_pid_not_exists(cli_run):
    responses.add(
        responses.GET,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid/files',
        json={
            'status': 404,
            'message': 'PID does not exist.'
        },
        status=404)

    res = cli_run("files get -p some-pid")

    assert res.exit_code == 1
    assert res.stripped_output == 'PID does not exist.'


@responses.activate
def test_files_get_no_access(cli_run):
    responses.add(
        responses.GET,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid/files',
        json={
            'message': "You don't have the permission to access the requested resource. "
            "It is either read-protected or not readable by the server.",
            'status': 403
        },
        status=403)

    res = cli_run("files get -p some-pid")

    assert res.exit_code == 1
    assert res.stripped_output == "You don't have sufficient permissions."


@responses.activate
def test_files_download(runner):
    responses.add(
        responses.GET,
        "https://analysispreservation-dev.cern.ch/api/deposits/some-pid",
        json={
            'links': {
                'bucket': 'http://analysispreservation.cern.ch/api/files/bucket-id'
            }
        },
        status=200)

    responses.add(
        responses.GET,
        'http://analysispreservation.cern.ch/api/files/bucket-id/test.txt',
        body=b'text',
        stream=True,
        status=200)

    with runner.isolated_filesystem():
        res = runner.run("files download -p some-pid test.txt")
        with open('test.txt', 'r') as fp:
            file_content = fp.read()

    assert file_content == 'text'
    assert res.exit_code == 0
    assert res.stripped_output == 'File saved as test.txt'


@responses.activate
def test_files_download_with_output_file_param(runner):
    responses.add(
        responses.GET,
        "https://analysispreservation-dev.cern.ch/api/deposits/some-pid",
        json={
            'links': {
                'bucket': 'http://analysispreservation.cern.ch/api/files/bucket-id'
            }
        },
        status=200)

    responses.add(
        responses.GET,
        'http://analysispreservation.cern.ch/api/files/bucket-id/test.txt',
        body=b'text',
        stream=True,
        status=200)

    with runner.isolated_filesystem():
        os.mkdir('dir')
        res = runner.run(
            "files download -p some-pid test.txt --output-file dir/newtest.txt"
        )

        with open('dir/newtest.txt', 'r') as fp:
            file_content = fp.read()

    assert file_content == 'text'
    assert res.exit_code == 0
    assert res.stripped_output == 'File saved as dir/newtest.txt'


def test_files_download_no_pid_given(cli_run):
    res = cli_run("files download test.txt")

    assert res.exit_code == 2
    assert "Error: Missing option '--pid' / '-p'." in res.output


def test_files_download_no_filename_given(cli_run):
    res = cli_run("files download -p some-pid")

    assert res.exit_code == 2
    assert "Error: Missing argument 'FILENAME'." in res.output


def test_files_download_path_not_exists(cli_run):
    res = cli_run(
        "files download -p some-pid filename --output-file missingdir/test.txt"
    )

    assert res.exit_code == 2
    assert "Error: Directory missingdir does not exist." in res.output


@responses.activate
def test_files_download_pid_not_exists(cli_run):
    responses.add(
        responses.GET,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={
            'status': 404,
            'message': 'PID does not exist.'
        },
        status=404)

    res = cli_run("files download -p some-pid test.txt")

    assert res.exit_code == 1
    assert res.stripped_output == 'PID does not exist.'


@responses.activate
def test_files_download_file_not_exists(cli_run):
    responses.add(
        responses.GET,
        "https://analysispreservation-dev.cern.ch/api/deposits/some-pid",
        json={
            'links': {
                'bucket': 'http://analysispreservation.cern.ch/api/files/bucket-id'
            }
        },
        status=200)

    responses.add(
        responses.GET,
        'http://analysispreservation.cern.ch/api/files/bucket-id/test.txt',
        json={
            'status': 404,
            'message': 'Object does not exists.'
        },
        status=404)

    res = cli_run("files download -p some-pid test.txt")

    assert res.exit_code == 1
    assert res.stripped_output == 'Object does not exists.'


@responses.activate
def test_files_remove(cli_run):
    responses.add(
        responses.GET,
        "https://analysispreservation-dev.cern.ch/api/deposits/some-pid",
        json={
            'links': {
                'bucket': 'http://analysispreservation.cern.ch/api/files/bucket-id'
            }
        },
        status=200)

    responses.add(
        responses.DELETE,
        'http://analysispreservation.cern.ch/api/files/bucket-id/test.txt',
        body='',
        status=204)

    res = cli_run("files remove -p some-pid test.txt")

    assert res.exit_code == 0
    assert res.stripped_output == 'File test.txt removed.'


def test_files_remove_no_pid_given(cli_run):
    res = cli_run("files remove test.txt")

    assert res.exit_code == 2
    assert "Error: Missing option '--pid' / '-p'." in res.output


def test_files_remove_no_filename_given(cli_run):
    res = cli_run("files remove -p some-pid")

    assert res.exit_code == 2
    assert "Error: Missing argument 'FILENAME'." in res.output


@responses.activate
def test_files_remove_pid_not_exists(cli_run):
    responses.add(
        responses.GET,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={
            'status': 404,
            'message': 'PID does not exist.'
        },
        status=404)

    res = cli_run("files download -p some-pid test.txt")

    assert res.exit_code == 1
    assert res.stripped_output == 'PID does not exist.'


@responses.activate
def test_files_remove_file_not_exists(cli_run):
    responses.add(
        responses.GET,
        "https://analysispreservation-dev.cern.ch/api/deposits/some-pid",
        json={
            'links': {
                'bucket': 'http://analysispreservation.cern.ch/api/files/bucket-id'
            }
        },
        status=200)

    responses.add(
        responses.DELETE,
        'http://analysispreservation.cern.ch/api/files/bucket-id/test.txt',
        json={
            'message': 'Object does not exists.',
            'status': 404
        },
        status=404)

    res = cli_run("files remove -p some-pid test.txt")

    assert res.exit_code == 1
    assert res.stripped_output == 'Object does not exists.'


@responses.activate
def test_files_upload_file(runner):
    responses.add(
        responses.GET,
        "https://analysispreservation-dev.cern.ch/api/deposits/some-pid",
        json={
            'links': {
                'bucket': 'http://analysispreservation.cern.ch/api/files/bucket-id'
            }
        },
        status=200)

    responses.add(
        responses.PUT,
        'http://analysispreservation.cern.ch/api/files/bucket-id/file.txt',
        json={
            'tags': {},
            'mimetype': 'application/octet-stream',
            'key': 'file.txt',
            'size': 10,
            'updated': '2020-04-15T14:08:03.028436+00:00',
            'checksum': 'md5:1c02b016968b102de60a18013314fb75',
            'links': {
                'self': 'http://analysispreservation.cern.ch/api/files/bucket-id/file.txt',
                'uploads': 'http://analysispreservation.cern.ch/api/files/bucket-id/file.txt?uploads'
            }
        },
        status=200)

    with runner.isolated_filesystem():
        os.mkdir('dir')
        with open('dir/file.txt', 'wb') as fp:
            fp.write(b'Hello world')

        res = runner.run("files upload -p some-pid dir/file.txt")

    assert responses.calls[1].request.body.name == 'dir/file.txt'
    assert res.exit_code == 0
    assert res.stripped_output == 'File uploaded successfully.'


@responses.activate
def test_files_upload_directory(runner):
    responses.add(
        responses.GET,
        "https://analysispreservation-dev.cern.ch/api/deposits/some-pid",
        json={
            'links': {
                'bucket': 'http://analysispreservation.cern.ch/api/files/bucket-id'
            }
        },
        status=200)

    responses.add(
        responses.PUT,
        'http://analysispreservation.cern.ch/api/files/bucket-id/dir.tar.gz',
        json={
            'key': 'dir.tar.gz',
            'mimetype': 'application/gzip',
            'checksum': 'md5:cdba97fedaccd33d849d5960a582fd43',
            'tags': {},
            'size': 10,
            'links': {
                'self': 'http://analysispreservation.cern.ch/api/files/bucket-id/dir.tar.gz',
                'uploads': 'http://analysispreservation.cern.ch/api/files/bucket-id/dir.tar.gz?uploads'
            }
        },
        status=200)

    with runner.isolated_filesystem():
        os.mkdir('dir')
        with open('dir/file.txt', 'wb') as fp:
            fp.write(b'Hello world')

        res = runner.run("files upload -p some-pid --yes-i-know dir")

    assert res.exit_code == 0
    assert res.stripped_output == 'File uploaded successfully.'


def test_files_upload_no_pid_given(cli_run):
    res = cli_run("files upload setup.py")

    assert res.exit_code == 2
    assert "Error: Missing option '--pid' / '-p'." in res.output


def test_files_upload_no_file_given(cli_run):
    res = cli_run("files upload -p some-pid")

    assert res.exit_code == 2
    assert "Error: Missing argument 'FILE'." in res.output


def test_files_upload_file_not_exists(cli_run):
    res = cli_run("files upload -p some-pid missing-file.txt")

    assert res.exit_code == 2
    assert "Error: Invalid value for 'FILE': Path 'missing-file.txt' does not exist." in res.output


@responses.activate
def test_files_upload_pid_not_exists(cli_run):
    responses.add(
        responses.GET,
        'https://analysispreservation-dev.cern.ch/api/deposits/some-pid',
        json={
            'status': 404,
            'message': 'PID does not exist.'
        },
        status=404)

    res = cli_run("files upload -p some-pid setup.py")

    assert res.exit_code == 1
    assert res.stripped_output == 'PID does not exist.'
