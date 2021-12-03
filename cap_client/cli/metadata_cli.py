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
from cap_client.utils import (ColoredGroup, NotRequiredIf,
                              json_dumps, load_json, load_json_from_file,
                              load_num, logger, pid_option)

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
    '-j',
    cls=NotRequiredIf,
    not_required_if=["jsonfile", "text", "num"],
    callback=load_json,
    help='\nJSON data.',
)
@click.option(
    '--jsonfile',
    '-f',
    type=click.File('r'),
    cls=NotRequiredIf,
    not_required_if=["json", "text", "num"],
    callback=load_json_from_file,
    help='\nJSON file.',
)
@click.option(
    '--text',
    '-t',
    cls=NotRequiredIf,
    not_required_if=["jsonfile", "json", "num"],
    help='\nText data.',
)
@click.option(
    '--num',
    '-n',
    cls=NotRequiredIf,
    not_required_if=["jsonfile", "json", "text"],
    callback=load_num,
    help='\nNumeric data.',
)
@pass_api
@logger
def update(api, pid, json, jsonfile, text, num, field):
    """Update analysis metadata."""
    value = [
        option for option in [json, jsonfile, text, num] if option is not None
    ][0]

    res = api.set(
        pid=pid,
        value=value,
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
