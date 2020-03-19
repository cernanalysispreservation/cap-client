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

import click

from ..utils import json_dumps, logger, pid_option


@click.group()
def permissions():
    """Permissions managing commands."""


@permissions.command()
@pid_option(required=True)
@click.option(
    '--user',
    '-u',
    required=True,
    help='User mail to assign permissions.',
)
@click.option(
    '--rights',
    '-r',
    type=click.Choice(['read', 'update', 'admin']),
    required=True,
    multiple=True,
)
@click.pass_context
@logger
def add(ctx, pid, user, rights):
    """Set analysis user permissions."""
    res = ctx.obj.cap_api.add_permissions(
        pid=pid,
        email=user,
        rights=rights,
    )

    click.echo(json_dumps(res))


@permissions.command()
@pid_option(required=True)
@click.option(
    '--user',
    '-u',
    required=True,
    help='User email to assign permissions.',
)
@click.option(
    '--rights',
    '-r',
    type=click.Choice(['read', 'update', 'admin']),
    required=True,
    multiple=True,
)
@click.pass_context
@logger
def remove(ctx, pid, user, rights):
    """Set analysis user permissions."""
    res = ctx.obj.cap_api.remove_permissions(
        pid=pid,
        email=user,
        rights=rights,
    )

    click.echo(json_dumps(res))


@permissions.command()
@pid_option(required=True)
@click.pass_context
@logger
def get(ctx, pid):
    """Retrieve analysis user permissions."""
    res = ctx.obj.cap_api.get_permissions(pid=pid)

    click.echo(json_dumps(res))
