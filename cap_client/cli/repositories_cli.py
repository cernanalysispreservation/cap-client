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
"""Repositories CAP Client CLI."""

import click

from ..utils import json_dumps, logger, pid_option


@click.group()
def repositories():
    """Repositories managing commands."""


@repositories.command()
@pid_option(required=True)
@click.option(
    '--url',
    '-u',
    required=True,
    help='The repo url.',
)
@click.option(
    '--webhook',
    '-w',
    type=click.Choice(['push', 'release']),
    help='Webhook type (push|release)',
)
@click.pass_context
@logger
def upload(ctx, pid, url, webhook):
    """Upload repository and/or create webhook for your analysis."""
    res = ctx.obj.cap_api.upload_repository(pid=pid,
                                            url=url,
                                            event_type=webhook)

    if webhook:
        click.echo(json_dumps(res))
    else:
        click.echo('Repository {} saved in analysis {}.'.format(url, pid))


@repositories.command()
@pid_option(required=True)
@click.option(
    '--with-snapshots',
    '-ws',
    default=False,
    is_flag=True,
    help='Include the snapshots of each repository.',
)
@click.pass_context
@logger
def get(ctx, pid, with_snapshots):
    """Get all the repositories for your analysis."""
    res = ctx.obj.cap_api.get_repositories(pid=pid,
                                           with_snapshots=with_snapshots)
    click.echo(json_dumps(res))
