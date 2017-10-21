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

"""General CAP Client CLI."""

import json
import logging

import click


@click.command()
@click.pass_context
def ping(ctx):
    """Health check CAP Server."""
    try:
        response = ctx.obj.cap_api.ping()
        logging.info('Server response:\n{}'.format(
            json.dumps(response, indent=4)))
    except Exception as e:
        logging.info('Unexpected error.')
        logging.debug(str(e))


@click.command()
@click.pass_context
def me(ctx):
    """Retrieve user info."""
    try:
        response = ctx.obj.cap_api.me()
        logging.info('Server response:\n{}'.format(
            json.dumps(response, indent=4)))
    except Exception as e:
        logging.info('Unexpected error.')
        logging.debug(str(e))


@click.command()
@click.option(
    '--pid',
    '-p',
    help='Get deposit with given pid',
    default=None)
@click.pass_context
def get(ctx, pid):
    """Retrieve one or all analyses from a user."""
    try:
        response = ctx.obj.cap_api.get(pid=pid)
        logging.info('Server response:\n{}'.format(
            json.dumps(response, indent=4)))

    except Exception as e:
        logging.info('Unexpected error.')
        logging.debug(str(e))


@click.command()
@click.option(
    '--file',
    '-f',
    help='File with JSON data',
    default=None,
    required=True,
)
@click.option(
    '--type',
    '-t',
    help='Type of analysis',
    default=None
)
@click.option(
    '--version',
    '-v',
    help='JSON schema version to api ',
)
@click.pass_context
def create(ctx, file, type, version):
    """Create an analysis."""
    try:
        response = ctx.obj.cap_api.create(
            filename=file,
            ana_type=type,
            version=version
        )
        logging.info('Server response:\n{}'.format(response))

    except Exception as e:
        logging.info('Unexpected error.')
        logging.debug(str(e))


@click.command()
@click.option(
    '--pid',
    '-p',
    help='Delete deposit with given pid',
    default=None,
    required=True
)
@click.pass_context
def delete(ctx, pid):
    """Delete analysis with given pid."""
    try:
        response = ctx.obj.cap_api.delete(pid=pid)
        logging.info('Server response:\n{}'.format(response))

    except Exception as e:
        logging.info('Unexpected error.')
        logging.debug(str(e))


@click.command()
@click.option(
    '--pid',
    '-p',
    help='Update deposit with given pid',
    default=None,
    required=True
)
@click.option(
    '--file',
    '-f',
    help='File with JSON data.',
    default=None,
    required=True
)
@click.pass_context
def update(ctx, pid, file):
    """Update analysis with given pid."""
    try:
        response = ctx.obj.cap_api.update(pid=pid, filename=file)
        logging.info('Server response:\n{}'.format(
            json.dumps(response, indent=4)))

    except Exception as e:
        logging.info('Unexpected error.')
        logging.debug(str(e))


@click.command()
@click.option(
    '--pid',
    '-p',
    help='Upload file to deposit with given pid',
    default=None,
    required=True
)
@click.argument('file', type=click.Path(exists=True))
@click.option(
    '--output-file',
    '-o',
    help='Filename to be given to uploaded file',
    default=None,
)
@click.option(
    '--yes',
    is_flag=True,
    help="Bypasses prompts..Say YES to everything"
)
@click.pass_context
def upload(ctx, pid, file, yes, output_file=None):
    """Update analysis with given pid."""
    try:
        response = ctx.obj.cap_api.upload(
            pid=pid, filepath=file, output_filename=output_file, yes=yes)
        logging.info('Server response:\n{}'.format(
            json.dumps(response, indent=4)))

    except Exception as e:
        logging.info('Unexpected error.')
        logging.debug(str(e))


@click.command()
@click.option(
    '--pid',
    '-p',
    help='Patch deposit with given pid',
    default=None,
    required=True
)
@click.option(
    '--file',
    '-f',
    help='File with JSON data.',
    default=None,
    required=True
)
@click.pass_context
def patch(ctx, pid, file):
    """Patch analysis with given pid."""
    try:
        response = ctx.obj.cap_api.patch(pid=pid, filename=file)
        logging.info('Server response:\n{}'.format(
            json.dumps(response, indent=4)))

    except Exception as e:
        logging.info('Unexpected error.')
        logging.debug(str(e))


@click.command()
@click.pass_context
def types(ctx):
    """Retrieve all types of analyses."""
    try:
        response = ctx.obj.cap_api.types()
        logging.info('Available types:\n{}'.format('\n'.join(response)))

    except Exception as e:
        logging.info('Unexpected error.')
        logging.debug(str(e))
