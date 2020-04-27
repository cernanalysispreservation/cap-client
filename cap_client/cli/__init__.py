# -*- coding: utf-8 -*-
#
# This file is part of CERN Analysis Preservation Framework.
# Copyright (C) 2020 CERN.
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
"""CAP cli module."""

import logging
import sys

import click

from cap_client.version import __version__
from cap_client.cli.analysis_cli import analysis
from cap_client.cli.files_cli import files
from cap_client.cli.metadata_cli import metadata
from cap_client.cli.permissions_cli import permissions
from cap_client.cli.repositories_cli import repositories
from cap_client.utils import ColoredGroup


@click.group(cls=ColoredGroup)
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
    default='info',
)
@click.version_option(__version__, message='%(version)s')
@click.pass_context
def cli(ctx, loglevel, verbose):
    """CAP command line interface."""
    if verbose:
        lvl = verbose
    else:
        lvl = getattr(logging, loglevel.upper())

    logging.basicConfig(format='[%(levelname)s] %(message)s',
                        stream=sys.stderr,
                        level=lvl)


cli.add_command(analysis)
cli.add_command(files)
cli.add_command(metadata)
cli.add_command(permissions)
cli.add_command(repositories)
