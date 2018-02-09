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

import pytest
from click.testing import CliRunner
from mock import DEFAULT, Mock, patch

from cap_client.cap_api import CapAPI
from cap_client.cli import cli


@pytest.yield_fixture
def cli_run():
    """Fixture for CLI runner function.

    Returns a function accepting a single parameter (CLI command as string).
    """
    runner = CliRunner()

    def run(*args, **kwargs):
        """Run the command from the CLI."""
        params = ['-l', 'info']
        params.extend(args)
        return runner.invoke(cli, params, **kwargs)

    yield run


@pytest.yield_fixture
def cap_api():
    yield CapAPI('https://analysispreservation-dev.cern.ch',
                 'api', 'accesstoken')


@pytest.yield_fixture
def mocked_cap_api(cap_api):
    """ Mock all private methods in CapAPI class."""
    with patch.multiple(cap_api,
                        _get_available_types=DEFAULT,
                        _make_request=DEFAULT) as mocks:
        mocks['_get_available_types'].return_value = ['atlas-workflows',
                                                      'alice-analysis']
        mocks['_make_request'].return_value = {}

        yield cap_api


@pytest.yield_fixture
def record_data():
    data = {
        "metadata": {
            "$schema": "https://localhost:5000/schemas/"
                       "deposits/records/cms-analysis-v0.0.1.json",
            "_access": {
                "deposit-admin": {
                    "roles": [],
                    "user": []
                },
                "deposit-read": {
                    "roles": [],
                    "user": [
                        "alice@inveniosoftware.org"
                    ]
                },
                "deposit-update": {
                    "roles": [],
                    "user": [
                        "alice@inveniosoftware.org"
                    ]
                }
            },
            "basic_info": {
                "analysis_number": "HIN-16-007",
                "people_info": [
                    {
                        "name": "John Doe"
                    },
                    {
                        "name": "Albert Einstein"
                    }
                ],
            },
            "general_title": "General relativity",
        }
    }

    yield data


@pytest.yield_fixture
def user_data():
    user_data = {
        "collaborations": [
            "ATLAS",
            "ALICE"
        ],
        "current_experiment": "ATLAS",
        "deposit_groups": [
            {
                "deposit_group": "atlas-workflows",
                "description": "Create an ATLAS Workflow",
                "name": "ATLAS Workflow"
            },
            {
                "deposit_group": "alice-analysis",
                "description": "Create an ALICE Analysis",
                "name": "ALICE Analysis"
            }
        ],
        "email": "my_mail@cern.ch",
        "id": 1
    }
    yield user_data
