# -*- coding: utf-8 -*-
#
# This file is part of CERN Analysis Preservation Framework.
# Copyright (C) 2021 CERN.
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
"""E2E testing configuration."""

import os

import pytest

from click.testing import CliRunner

from cap_client.cli import cli


@pytest.fixture(autouse=True)
def env_e2e():
    """Set environment."""
    os.environ['CAP_SERVER_URL'] = os.environ.get('TESTS_SERVER_HOST', 'https://nginx')


@pytest.fixture()
def user_tokens():
    """Set environment."""
    def _f(user=None):
        if os.environ.get('TEST_E2E_TOKEN'):
            os.environ['CAP_ACCESS_TOKEN'] = os.environ.get('TEST_E2E_TOKEN')
        else:
            file_path = os.environ.get('TESTS_E2E_TOKEN_FILE', '/test_data/test_tokens')
            with open(file_path, 'r') as f:
                tokens = f.read()
                tokens = tokens.split("\n")
                _tokens = {}

                for t in tokens:
                    _t = t.split(":")
                    if len(_t) == 2:
                        email, token = _t
                        _tokens[email] = token
            os.environ['CAP_ACCESS_TOKEN'] = _tokens.get(user, 'token')
    return _f


@pytest.yield_fixture
def cli_run():
    """Fixture for CLI runner function.
    Returns a function accepting a single parameter (cli command as string).
    """
    runner = CliRunner()

    def run(cmd, **kwargs):
        """Run the command from the CLI.
        :param cmd: command with its arguments
        :type cmd: str
        :warn: when passing your command remember
        to not have any whitespaces inside an argument values!
        :return: runner result
        :rtype: `click.testing.Result`
        """
        res = runner.invoke(cli, cmd.split(), **kwargs)

        if res.output:
            res.stripped_output = res.output.strip()

        return res

    yield run


@pytest.fixture(scope='module')
def vcr_config():
    return {
        "filter_headers": [('authorization', 'DUMMY')],
    }
