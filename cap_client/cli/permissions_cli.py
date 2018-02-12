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

"""Permissions CAP Client CLI."""

import json
import logging

import click


@click.group()
def permissions():
    """Permissions managing commands."""


@permissions.command()
@click.option(
    '--pid',
    '-p',
    help='PID of draft to update.',
    default=None,
    required=True
)
@click.option(
    '--user',
    '-u',
    help='User mail to assign permissions.',
    default=None,
    required=True
)
@click.option('--rights',
              '-r',
              required=True,
              type=click.Choice(
                  ['read',
                   'update',
                   'admin']),
              multiple=True)
@click.pass_context
def add(ctx, pid, user, rights):
    """Set analysis user permissions."""
    try:
        response = ctx.obj.cap_api.add_permissions(pid=pid,
                                                   email=user,
                                                   rights=rights,
                                                   )
        click.echo(json.dumps(response, indent=4))

    except Exception as e:
        logging.error('Unexpected error.')
        logging.debug(str(e))


@permissions.command()
@click.option(
    '--pid',
    '-p',
    help='PID of draft to update.',
    default=None,
    required=True
)
@click.option(
    '--user',
    '-u',
    help='User email to assign permissions.',
    default=None,
    required=True
)
@click.option('--rights',
              '-r',
              required=True,
              type=click.Choice(
                  ['read',
                   'update',
                   'admin']),
              multiple=True)
@click.pass_context
def remove(ctx, pid, user, rights):
    """Set analysis user permissions."""
    try:
        response = ctx.obj.cap_api.remove_permissions(pid=pid,
                                                      email=user,
                                                      rights=rights,
                                                      )
        click.echo(json.dumps(response, indent=4))

    except Exception as e:
        logging.error('Unexpected error.')
        logging.debug(str(e))


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
