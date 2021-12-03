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
"""Permissions CAP Client CLI."""

import click

from cap_client.api import PermissionsAPI
from cap_client.utils import (
    ColoredGroup, NotRequiredIf,
    json_dumps, logger, pid_option
)

pass_api = click.make_pass_decorator(PermissionsAPI, ensure=True)


@click.group(cls=ColoredGroup)
def permissions():
    """Manage analysis permissions."""


@permissions.command()
@pid_option(required=True)
@logger
@pass_api
def get(api, pid):
    """List analysis permissions."""
    res = api.get(pid=pid)

    click.echo(json_dumps(res))


@permissions.command()
@pid_option(required=True)
@click.option(
    '--user',
    '-u',
    cls=NotRequiredIf,
    not_required_if=["egroup"],
    help='User mail.',
)
@click.option(
    '--egroup',
    '-e',
    cls=NotRequiredIf,
    not_required_if=["user"],
    help='Egroup mail.',
)
@click.option(
    '--rights',
    '-r',
    type=click.Choice(['read', 'update', 'admin']),
    required=True,
    multiple=True,
)
@logger
@pass_api
def add(api, pid, rights, user, egroup):
    """Add user/egroup permissions for your analysis."""
    res = api.add(
        pid=pid,
        email=user or egroup,
        rights=rights,
        is_egroup=egroup and True,
    )

    click.echo(json_dumps(res))


@permissions.command()
@pid_option(required=True)
@click.option(
    '--user',
    '-u',
    cls=NotRequiredIf,
    not_required_if=["egroup"],
    help='User mail.',
)
@click.option(
    '--egroup',
    '-e',
    cls=NotRequiredIf,
    not_required_if=["user"],
    help='Egroup mail.',
)
@click.option(
    '--rights',
    '-r',
    type=click.Choice(['read', 'update', 'admin']),
    required=True,
    multiple=True,
)
@logger
@pass_api
def remove(api, pid, rights, user, egroup):
    """Remove user/egroup permissions for your analysis."""
    res = api.remove(
        pid=pid,
        email=user or egroup,
        rights=rights,
        is_egroup=egroup and True,
    )

    click.echo(json_dumps(res))
