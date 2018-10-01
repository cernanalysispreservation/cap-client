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


"""CAP Client CLI init."""

import click
import logging
import os
import sys

from cap_client.cap_api import CapAPI
from cap_client.cli.cli import (create, clone, publish, delete, get, me,
                                types, get_shared, get_schema)
from cap_client.cli.metadata_cli import metadata
from cap_client.cli.files_cli import files
from cap_client.cli.permissions_cli import permissions


class Config(object):
    """Configuration object to share across commands."""

    def __init__(self, access_token=None, verbose=False):
        """Initialize config variables."""
        self.server = os.environ.get(
            'CAP_SERVER_URL', 'https://analysispreservation.cern.ch')
        apipath = os.environ.get('CAP_SERVER_API_PATH', 'api')
        access_token = access_token or os.environ.get('CAP_ACCESS_TOKEN', None)

        self.cap_api = CapAPI(self.server, apipath, access_token)
        self.verbose = verbose


@click.group()
@click.option(
    '--verbose',
    '-v',
    help='Verbose output',
    flag_value=logging.DEBUG,
    default=False,
)
@click.option(
    '--loglevel',
    '-l',
    help='Sets log level',
    type=click.Choice(['error', 'debug', 'info']),
    default='info'
)
@click.option(
    '--access_token',
    '-t',
    help='Sets users access token',
)
@click.pass_context
def cli(ctx, loglevel, verbose, access_token):
    """CAP Client for interacting with CAP Server."""
    if verbose:
        lvl = verbose
    else:
        lvl = getattr(logging, loglevel.upper())
    logging.basicConfig(
        format='[%(levelname)s] %(message)s',
        stream=sys.stderr,
        level=lvl)
    ctx.obj = Config(access_token=access_token)


# cli.add_command(ping)
cli.add_command(get)
cli.add_command(get_shared)
cli.add_command(get_schema)
cli.add_command(me)
cli.add_command(create)
cli.add_command(delete)
cli.add_command(publish)
cli.add_command(clone)
cli.add_command(types)
cli.add_command(files)
cli.add_command(metadata)
cli.add_command(permissions)
