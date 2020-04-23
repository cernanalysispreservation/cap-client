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
"""Repositories CAP Client CLI."""

import click

from cap_client.api import RepositoriesAPI
from cap_client.utils import ColoredGroup, json_dumps, logger, pid_option

pass_api = click.make_pass_decorator(RepositoriesAPI, ensure=True)


@click.group(cls=ColoredGroup)
def repositories():
    """Manage analysis repositories and webhooks."""


@repositories.command()
@pid_option(required=True)
@click.option(
    '--with-snapshots',
    '-ws',
    default=False,
    is_flag=True,
    help='Show snapshots.',
)
@pass_api
@logger
def get(api, pid, with_snapshots):
    """Get all repositories connected with your analysis."""
    res = api.get(
        pid=pid,
        with_snapshots=with_snapshots,
    )

    click.echo(json_dumps(res))


@repositories.command()
@pid_option(required=True)
@click.argument('url')
@pass_api
@logger
def upload(api, pid, url):
    """Upload repository tarball to your analysis."""
    api.upload(
        pid=pid,
        url=url,
    )

    click.echo('Repository tarball was saved with your analysis files. '
               '(access using `cap-client files` methods)')


@repositories.command()
@pid_option(required=True)
@click.option(
    '--event',
    type=click.Choice(['push', 'release']),
    default='release',
    help='Download repository tarball on every (push|release)',
)
@click.argument('url')
@pass_api
@logger
def connect(api, pid, url, event):
    """Connect repository with your analysis."""
    api.upload(
        pid=pid,
        url=url,
        event_type=event,
    )

    click.echo(
        'Repository was connected with analysis.\n'
        'Now on every {}, we will attach the latest version to your analysis.'.
        format(event))
