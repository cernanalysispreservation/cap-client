# -*- coding: utf-8 -*-
#
# This file is part of Zenodo.
# Copyright (C) 2015, 2016 CERN.
#
# Zenodo is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Zenodo is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Zenodo; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.
"""Pytest configuration."""

from __future__ import absolute_import, print_function

import os

import pytest
from click.testing import CliRunner

from cap_client.cli import cli


@pytest.fixture(autouse=True)
def env():
    """Set environment."""
    os.environ['CAP_SERVER_URL'] = 'https://analysispreservation-dev.cern.ch'
    os.environ['CAP_SERVER_API_PATH'] = 'api/'
    os.environ['CAP_ACCESS_TOKEN'] = 'token'


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


@pytest.yield_fixture(scope='module')
def runner():
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

    runner.run = run

    yield runner


@pytest.yield_fixture
def record_data():
    data = {
        "metadata": {
            "$schema": "https://analysispreservation-dev.cern.ch/schemas/"
            "deposits/records/cms-analysis-v0.0.1.json",
            "_access": {
                "deposit-admin": {
                    "roles": [],
                    "user": []
                },
                "deposit-read": {
                    "roles": [],
                    "user": ["alice@inveniosoftware.org"]
                },
                "deposit-update": {
                    "roles": [],
                    "user": ["alice@inveniosoftware.org"]
                }
            },
            "basic_info": {
                "analysis_number": "hin-16-007",
                "people_info": [{
                    "name": "john doe"
                }, {
                    "name": "albert einstein"
                }],
            },
            "general_title": "general relativity",
        }
    }

    yield data
