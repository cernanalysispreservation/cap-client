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
"""Metadata CAP Client CLI."""

import click

from cap_client.api.metadata_api import MetadataAPI
from cap_client.utils import (ColoredGroup, MutuallyExclusiveOption,
                              json_dumps, load_json, load_json_from_file,
                              logger, pid_option)

pass_api = click.make_pass_decorator(MetadataAPI, ensure=True)


@click.group(cls=ColoredGroup)
def metadata():
    """Manage analysis metadata."""


@metadata.command()
@pid_option(required=True)
@click.option(
    '--field',
    help="Specify an EXISTING field\n eg. object.nested_array.0",
)
@click.option(
    '--json',
    cls=MutuallyExclusiveOption,
    not_required_if="jsonfile",
    callback=load_json,
    help='\nJSON data or text.',
)
@click.option(
    '--jsonfile',
    type=click.File('r'),
    cls=MutuallyExclusiveOption,
    not_required_if="json",
    callback=load_json_from_file,
    help='\nJSON file.',
)
@pass_api
@logger
def update(api, pid, json, jsonfile, field):
    """Update analysis metadata."""
    res = api.set(
        pid=pid,
        value=jsonfile if json is None else json,
        field=field,
    )

    click.echo(json_dumps(res))


@metadata.command()
@pid_option(required=True)
@click.option(
    '--field',
    required=True,
    help="Specify field, eg. object.nested_array.0",
)
@pass_api
@logger
def remove(api, pid, field):
    """Remove from analysis metadata."""
    res = api.remove(
        pid=pid,
        field=field,
    )

    click.echo(json_dumps(res))


@metadata.command()
@pid_option(required=True)
@click.option(
    '--field',
    help="Specify field, eg. object.nested_array.0",
)
@pass_api
@logger
def get(api, pid, field):
    """Get analysis metadata."""
    res = api.get(
        pid=pid,
        field=field,
    )

    click.echo(json_dumps(res))
