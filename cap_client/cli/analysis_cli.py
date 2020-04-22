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
"""CAP Analysis command line interface."""

import click

from cap_client.api import AnalysisAPI
from cap_client.utils import (ColoredGroup, MutuallyExclusiveOption,
                              json_dumps, load_json, load_json_from_file,
                              logger, pid_option, validate_version)

pass_api = click.make_pass_decorator(AnalysisAPI, ensure=True)


@click.group(cls=ColoredGroup)
def analysis():
    """Manage your analysis."""


@analysis.command()
@logger
@pass_api
def types(api):
    """List all types of analysis you can create."""
    res = api.get_schema_types()

    click.echo(json_dumps(res))


@analysis.command()
@click.option(
    '--type',
    '-t',
    required=True,
    help='Analysis type',
)
@click.option(
    '--version',
    '-v',
    callback=validate_version,
    help='Version of the schema',
)
@click.option(
    '--for-published',
    is_flag=True,
    default=False,
    help="Show schema for published analysis"
    "(may be different than draft schema)",
)
@logger
@pass_api
def schema(api, type, version, for_published):
    """Get JSON schema for analysis metadata."""
    res = api.get_schema(
        type_=type,
        version=version,
        record_schema=for_published,
    )

    click.echo(json_dumps(res))


@analysis.command()
@pid_option(required=False)
@click.option(
    '--all',
    is_flag=True,
    help="Show all (not only yours).",
)
@logger
@pass_api
def get(api, pid, all):
    """List your draft analysis."""
    if pid:
        res = api.get_draft_by_pid(pid)
    else:
        res = api.get_drafts(all=all)

    click.echo(json_dumps(res))


@analysis.command('get-published')
@pid_option(required=False)
@click.option(
    '--all',
    is_flag=True,
    default=False,
    help="Show all (not only yours).",
)
@logger
@pass_api
def get_published(api, pid, all):
    """List your published analysis."""
    if pid:
        res = api.get_published_by_pid(pid)
    else:
        res = api.get_published(all=all)

    click.echo(json_dumps(res))


@analysis.command()
@click.option(
    '--json',
    '-j',
    cls=MutuallyExclusiveOption,
    not_required_if=["jsonfile"],
    callback=load_json,
    help='\nJSON data from command line.',
)
@click.option(
    '--jsonfile',
    '-f',
    type=click.File('r'),
    cls=MutuallyExclusiveOption,
    not_required_if=["json"],
    callback=load_json_from_file,
    help='\nJSON file.',
)
@click.option(
    '--type',
    '-t',
    default=None,
    help='Type of analysis',
)
@logger
@pass_api
def create(api, jsonfile, json, type):
    """Create an analysis."""
    res = api.create(
        data=jsonfile if json is None else json,
        type_=type,
    )

    click.echo(json_dumps(res))


@analysis.command()
@pid_option(required=True)
@logger
@pass_api
def publish(api, pid):
    """Publish analysis with given pid."""
    pid = api.publish(pid=pid)

    click.echo('Your analysis has been published with PID: {}'.format(pid))


@analysis.command()
@pid_option(required=True)
@logger
@pass_api
def delete(api, pid):
    """Delete your analysis."""
    api.delete(pid=pid)

    click.echo('Analysis has been deleted.'.format(pid))
