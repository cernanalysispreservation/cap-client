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

"""Metadata CAP Client CLI."""

import json
import logging

import click

from cap_client.errors import BadStatusCode


@click.group()
def metadata():
    """Metadata managing commands."""


@metadata.command()
@click.option(
    '--pid',
    '-p',
    help='PID of draft to update.',
    default=None,
    required=True
)
@click.option(
    '--file',
    '-f',
    type=click.Path(),
    help='Path to file to upload.',
    default=None,
    required=False
)
@click.argument('field_name')
@click.argument('field_value')
@click.pass_context
def set(ctx, field_name, field_value, pid, file):
    """Edit analysis field value."""
    try:
        response = ctx.obj.cap_api.set_field(field_name, field_value, pid,
                                             file)
        click.echo(json.dumps(response, indent=4))

    except BadStatusCode as e:
        logging.error(str(e))

    except Exception as e:
        logging.error('Unexpected error.')
        logging.debug(str(e))


@metadata.command()
@click.option(
    '--pid',
    '-p',
    help='PID of draft to update.',
    default=None,
    required=True
)
@click.argument('field_name')
@click.pass_context
def remove(ctx, field_name, pid):
    """Remove analysis field."""
    try:
        response = ctx.obj.cap_api.remove_field(field_name, pid)
        click.echo(json.dumps(response, indent=4))

    except BadStatusCode as e:
        logging.error(str(e))

    except Exception as e:
        logging.error('Unexpected error.')
        logging.debug(str(e))


@metadata.command()
@click.option(
    '--pid',
    '-p',
    help='Append value to metadata array field',
    default=None,
    required=True
)
@click.option(
    '--file',
    '-f',
    type=click.Path(),
    help='Path to file to upload.',
    default=None,
    required=False
)
@click.argument('field_name')
@click.argument('field_value')
@click.pass_context
def append(ctx, field_name, field_value, pid, file):
    """Edit analysis field adding a new value to an array."""
    try:
        response = ctx.obj.cap_api.set_field(field_name, field_value, pid,
                                             file, append=True)
        click.echo(json.dumps(response, indent=4))

    except BadStatusCode as e:
        logging.error(str(e))

    except Exception as e:
        logging.error('Unexpected error.')
        logging.debug(str(e))


@metadata.command()
@click.argument(
    'field',
    default=None,
    required=False,
)
@click.option(
    '--pid',
    '-p',
    help='Get metadata of the deposit with given pid',
    default=None,
    required=True,
)
@click.pass_context
def get(ctx, field, pid):
    """Retrieve one or more fields in analysis metadata."""
    try:
        response = ctx.obj.cap_api.get_field(pid=pid, field=field)
        click.echo(json.dumps(response,
                              indent=4))

    except KeyError:
        logging.error('Field {} doesn\'t exist'
                      .format(field))

    except BadStatusCode as e:
        logging.error(str(e))

    except Exception as e:
        logging.error('Unexpected error.')
        logging.debug(str(e))
