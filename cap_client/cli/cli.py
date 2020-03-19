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

import click

from ..utils import json_dumps, logger, pid_option, validate_version


@click.command()
@click.pass_context
@logger
def me(ctx):
    """Retrieve user info."""
    res = ctx.obj.cap_api.me()

    click.echo(json_dumps(res))


@click.command('get-shared')
@pid_option(required=False)
@click.option(
    '--all',
    is_flag=True,
    default=False,
    help="Retrieve all shared (published) analyses you can access.",
)
@click.pass_context
@logger
def get_shared(ctx, pid, all):
    """Retrieve user's published analysis."""
    if pid:
        res = ctx.obj.cap_api.get_shared_by_pid(pid)
    else:
        res = ctx.obj.cap_api.get_shared(all=all)

    click.echo(json_dumps(res))


@click.command()
@pid_option(required=False)
@click.option(
    '--all',
    is_flag=True,
    help="Retrieve all draft analyses you can access.",
)
@click.pass_context
@logger
def get(ctx, pid, all):
    """Retrieve user's drafts."""
    if pid:
        res = ctx.obj.cap_api.get_draft_by_pid(pid)
    else:
        res = ctx.obj.cap_api.get_drafts(all=all)

    click.echo(json_dumps(res))


@click.command()
@click.option(
    '--json',
    '-j',
    'json_',
    required=True,
    help='JSON data from file or command line',
)
@click.option(
    '--type',
    '-t',
    'type_',
    default=None,
    help='Type of analysis',
)
@click.pass_context
@logger
def create(ctx, json_, type_):
    """Create an analysis."""
    res = ctx.obj.cap_api.create(json_=json_, ana_type=type_)

    click.echo(json_dumps(res))


@click.command()
@pid_option(required=True)
@click.option(
    '--json',
    '-j',
    'json_',
    required=True,
    help='JSON data from file or command line',
)
@click.pass_context
@logger
def update(ctx, pid, json_):
    """Update an analysis."""
    res = ctx.obj.cap_api.update(pid=pid, json_=json_)

    click.echo(json_dumps(res))


@click.command()
@pid_option(required=True)
@click.pass_context
@logger
def delete(ctx, pid):
    """Delete analysis with given pid."""
    ctx.obj.cap_api.delete(pid=pid)

    click.echo('Analysis {} deleted.'.format(pid))


@click.command()
@pid_option(required=True)
@click.pass_context
@logger
def publish(ctx, pid):
    """Publish analysis with given pid."""
    ctx.obj.cap_api.publish(pid=pid)

    click.echo('Your analysis has been published')


@click.command()
@pid_option(required=True)
@click.pass_context
@logger
def clone(ctx, pid):
    """Clone analysis with given pid."""
    res = ctx.obj.cap_api.clone(pid=pid)

    click.echo(json_dumps(res))


@click.command()
@click.pass_context
@logger
def types(ctx):
    """Retrieve all types of analyses."""
    res = ctx.obj.cap_api.types()

    click.echo('Available types:\n{}'.format('\n'.join(res)))


@click.command('get-schema')
@click.option(
    '--type',
    '-t',
    required=True,
    help='Type of analysis',
)
@click.option(
    '--version',
    '-v',
    callback=validate_version,
    help='Version of the schema',
)
@click.option(
    '--record',
    is_flag=True,
    default=False,
    help="Retrieve the record schema, instead of the deposit",
)
@click.pass_context
@logger
def get_schema(ctx, type, version, record):
    """Retrieve analysis schema."""
    res = ctx.obj.cap_api.get_schema(ana_type=type,
                                     version=version,
                                     record=record)

    click.echo(json_dumps(res))
