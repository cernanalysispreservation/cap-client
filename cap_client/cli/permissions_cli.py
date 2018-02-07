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


@click.group()
def permissions():
    """Permissions managing commands."""


# @permissions.command()
# @click.option(
#     '--pid',
#     '-p',
#     help='PID of draft to update.',
#     default=None,
#     required=True
# )
# @click.option(
#     '--file',
#     '-f',
#     type=click.Path(),
#     help='Path to file to upload.',
#     default=None,
#     required=False
# )
# @click.pass_context
# def set(ctx, field_name, field_value, pid, file):
#     """Edit analysis field value."""
#     try:
#         response = ctx.obj.cap_api.set(field_name, field_value, pid, file)
#         click.echo(json.dumps(response, indent=4))
#
#     except Exception as e:
#         logging.error('Unexpected error.')
#         logging.debug(str(e))


@permissions.command()
@click.option(
    '--pid',
    '-p',
    help='Get permissions of the deposit with given pid',
    default=None,
    required=True,
)
@click.pass_context
def get(ctx, pid):
    """Retrieve analysis user permissions."""
    try:
        response = ctx.obj.cap_api.get_permissions(pid=pid)
        click.echo(json.dumps(response, indent=4))
    except Exception as e:
        logging.error('Unexpected error.')
        logging.debug(str(e))


