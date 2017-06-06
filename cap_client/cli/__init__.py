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

import click
import logging
import sys
import os

from cap_client.cli.cli import ping
from cap_client.cap_api import CapAPI


class Config(object):
    """Configuration object to share across commands."""

    def __init__(self, access_token=None, verbose=False):
        """Initialize config variables."""
        server = os.environ.get(
            'CAP_SERVER_URL', 'https://analysispreservation.cern.ch')
        apipath = os.environ.get('CAP_SERVER_API_PATH', None)
        access_token = access_token or os.environ.get('CAP_ACCESS_TOKEN', None)

        self.cap_api = CapAPI(server, apipath, access_token)
        self.verbose = verbose


@click.group()
@click.option(
    '--loglevel',
    '-l',
    help='Sets log level',
    type=click.Choice(['debug', 'info']),
    default='info')
@click.option(
    '--access_token',
    '-t',
    help='Sets users access token',)
@click.pass_context
def cli(ctx, loglevel, access_token):
    """CAP Client for interacting with CAP Server."""
    logging.basicConfig(
        format='[%(levelname)s] %(message)s',
        stream=sys.stderr,
        level=logging.DEBUG if loglevel == 'debug' else logging.INFO)
    ctx.access_token = access_token
    ctx.obj = Config(access_token=access_token)


cli.add_command(ping)
