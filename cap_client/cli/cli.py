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

import logging

import click


@click.command()
@click.pass_context
def ping(ctx):
    """Health check CAP Server."""
    try:
        logging.info('Connecting to {0}'.format(ctx.obj.cap_api.server_url))
        response = ctx.obj.cap_api.ping()
        logging.info('Server is running.')
        logging.info('Server response:\n{}'.format(response))

    except Exception as e:
        logging.info('Something went wrong when trying to connect to {0}'
                     .format(ctx.obj.cap_api))
        logging.debug(str(e))


@click.command()
@click.option(
    '--pid',
    '-p',
    help='Get deposit with given pid',
    default=None)
@click.pass_context
def get(ctx, pid):
    """Retrieve one or all analyses from a user."""
    try:
        logging.info('Connecting to {0}'.format(ctx.obj.cap_api.server_url))
        response = ctx.obj.cap_api.get(pid=pid)
        logging.info('Server response:\n{}'.format(response))

    except Exception as e:
        logging.info('Something went wrong when trying to connect to {0}'
                     .format(ctx.obj.cap_api))
        logging.debug(str(e))


@click.command()
@click.option(
    '--data',
    '-d',
    help='Post data to api ',
    default=None
)
@click.option(
    '--type',
    '-t',
    help='Type of analysis',
    default=None
)
@click.option(
    '--version',
    '-v',
    help='JSON schema version to api ',
)
@click.pass_context
def create(ctx, data, type, version):
    """Create an analysis."""
    try:
        logging.info('Connecting to {0}'.format(
            ctx.obj.cap_api.server_url))
        response = ctx.obj.cap_api.create(
            data=data,
            type=type,
            version=version
        )
        logging.info('Server response:\n{}'.format(response))

    except Exception as e:
        logging.info('Something went wrong when trying to connect to {0}'
                     .format(ctx.obj.cap_api.server_url))
        logging.debug(str(e))
