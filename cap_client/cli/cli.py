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

import json
import logging

import click

from cap_client.errors import BadStatusCode, UnknownAnalysisType, \
    MissingJsonFile


# @click.command()
# @click.pass_context
# def ping(ctx):
#     """Health check CAP Server."""
#     try:
#         response = ctx.obj.cap_api.ping()
#         click.echo(response)

#     except BadStatusCode as e:
#         logging.error(str(e))

#     except Exception as e:
#         logging.error('Unexpected error.')
#         logging.debug(str(e))


@click.command()
@click.pass_context
def me(ctx):
    """Retrieve user info."""
    try:
        response = ctx.obj.cap_api.me()
        click.echo(json.dumps(response,
                              indent=4))

    except BadStatusCode as e:
        logging.error(str(e))

    except Exception as e:
        logging.error('Unexpected error.')
        logging.debug(str(e))


@click.command('get-shared')
@click.option(
    '--pid',
    '-p',
    help='Get record with given pid',
    default=None)
@click.option(
    '--all',
    is_flag=True,
    help="Retrieve all shared analyses you can access."
)
@click.pass_context
def get_shared(ctx, pid, all):
    """Retrieve one or all shared analyses from a user."""
    try:
        response = ctx.obj.cap_api.get_shared(pid=pid)
        click.echo(json.dumps(response,
                              indent=4))

    except BadStatusCode as e:
        logging.error(str(e))

    except Exception as e:
        logging.error('Unexpected error.')
        logging.debug(str(e))


@click.command()
@click.option(
    '--pid',
    '-p',
    help='Get deposit with given pid',
    default=None)
@click.option(
    '--all',
    is_flag=True,
    help="Retrieve all analyses you can access."
)
@click.pass_context
def get(ctx, pid, all):
    """Retrieve one or all analyses from a user."""
    try:
        response = ctx.obj.cap_api.get(pid=pid, all=all)
        click.echo(json.dumps(response,
                              indent=4))

    except BadStatusCode as e:
        logging.error(str(e))

    except Exception as e:
        logging.error('Unexpected error.')
        logging.debug(str(e))


@click.command()
@click.option(
    '--json-file',
    help='JSON data from file or command line',
    default=None,
)
@click.option(
    '--type',
    '-t',
    help='Type of analysis',
    default=None,
)
@click.option(
    '--version',
    help='JSON schema version to api ',
)
@click.pass_context
def create(ctx, json_file, type, version):
    """Create an analysis."""
    try:
        response = ctx.obj.cap_api.create(
            json_=json_file,
            ana_type=type,
            version=version
        )

        click.echo(json.dumps(response,
                              indent=4))

    except UnknownAnalysisType as e:
        logging.error(str(e))

    except BadStatusCode as e:
        logging.error(str(e))

    except MissingJsonFile as e:
        logging.error(str(e))

    except Exception as e:
        logging.error('Unexpected error.')
        logging.debug(str(e))


@click.command()
@click.option(
    '--pid',
    '-p',
    help='Delete deposit with given pid',
    default=None,
    required=True
)
@click.pass_context
def delete(ctx, pid):
    """Delete analysis with given pid."""
    try:
        ctx.obj.cap_api.delete(pid=pid)
        click.echo('Analysis {} deleted.'.format(pid))

    except BadStatusCode as e:
        logging.error(str(e))

    except Exception as e:
        logging.error('Unexpected error.')
        logging.debug(str(e))


@click.command()
@click.option(
    '--pid',
    '-p',
    help='Publish deposit with given pid',
    default=None,
    required=True
)
@click.pass_context
def publish(ctx, pid):
    """Publish analysis with given pid."""
    try:
        response = ctx.obj.cap_api.publish(pid=pid)
        click.echo(json.dumps(response,
                              indent=4))

    except BadStatusCode as e:
        logging.error(str(e))

    except Exception as e:
        logging.error('Unexpected error.')
        logging.debug(str(e))


@click.command()
@click.option(
    '--pid',
    '-p',
    help='Clone deposit with given pid',
    default=None,
    required=True
)
@click.pass_context
def clone(ctx, pid):
    """Clone analysis with given pid."""
    try:
        response = ctx.obj.cap_api.clone(pid=pid)
        click.echo(json.dumps(response,
                              indent=4))

    except BadStatusCode as e:
        logging.error(str(e))

    except Exception as e:
        logging.error('Unexpected error.')
        logging.debug(str(e))


@click.command()
@click.pass_context
def types(ctx):
    """Retrieve all types of analyses."""
    try:
        response = ctx.obj.cap_api.types()
        click.echo('Available types:\n{}'.format('\n'.join(response)))

    except BadStatusCode as e:
        logging.error(str(e))

    except Exception as e:
        logging.error('Unexpected error.')
        logging.debug(str(e))


@click.command('get-schema')
@click.option(
    '--type',
    '-t',
    help='Type of analysis',
    default=None,
    required=True
)
@click.pass_context
def get_schema(ctx, type):
    """Retrieve analysis schema."""
    try:
        response = ctx.obj.cap_api.get_schema(ana_type=type)
        click.echo(json.dumps(response,
                              indent=4))
    except UnknownAnalysisType as e:
        logging.error(str(e))

    except BadStatusCode as e:
        logging.error(str(e))

    except Exception as e:
        logging.error('Unexpected error.')
        logging.debug(str(e))
