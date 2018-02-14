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

"""Files CAP Client CLI."""

import json
import logging

import click

from cap_client.errors import BadStatusCode


@click.group()
def files():
    """Files managing commands."""


@files.command()
@click.option(
    '--pid',
    '-p',
    help='Upload file to deposit with given pid',
    default=None,
    required=True
)
@click.argument('file', type=click.Path(exists=False))
@click.option(
    '--output-file',
    '-o',
    help='Filename to be given to uploaded file',
    default=None,
)
@click.option(
    '--yes',
    is_flag=True,
    help="Bypasses prompts..Say YES to everything"
)
@click.option(
    '--docker',
    is_flag=True,
    help="Uploads docker image."
)
@click.pass_context
def upload(ctx, pid, file, yes, output_file=None, docker=False):
    """Upload file to deposit with given pid."""
    try:
        if docker:
            ctx.obj.cap_api.upload_docker_img(pid=pid, img_name=file,
                                              output_img_name=output_file)
        else:
            ctx.obj.cap_api.upload_file(
                pid=pid, filepath=file,
                output_filename=output_file, yes=yes)
        click.echo("File uploaded successfully.")

    except BadStatusCode as e:
        logging.error(str(e))

    except Exception as e:
        logging.error('Unexpected error.')
        logging.debug(str(e))


@files.command()
@click.option(
    '--pid',
    '-p',
    help='Get file uploaded with deposit with given pid',
    default=None,
    required=True
)
@click.option(
    '--output-file',
    '-o',
    help='Filename to be given to uploaded file',
    default=None,
)
@click.argument('filename')
@click.pass_context
def download(ctx, pid, output_file, filename):
    """Download file uploaded with given deposit."""
    try:
        ctx.obj.cap_api.download_file(pid, filename, output_file)
        click.echo("File saved as {}".format(output_file or filename))

    except BadStatusCode as e:
        logging.error(str(e))

    except Exception as e:
        logging.error('Unexpected error.')
        logging.debug(str(e))


@files.command()
@click.option(
    '--pid',
    '-p',
    help='List files of deposit with given pid',
    default=None,
    required=True
)
@click.pass_context
def list(ctx, pid):
    """List files associated with deposit with given pid."""
    try:
        response = ctx.obj.cap_api.list_files(pid=pid)
        click.echo(json.dumps(response,
                              indent=4))

    except BadStatusCode as e:
        logging.error(str(e))

    except Exception as e:
        logging.error('Unexpected error.')
        logging.debug(str(e))


@files.command()
@click.option(
    '--pid',
    '-p',
    help='Remove file from deposit with given pid',
    default=None,
    required=True
)
@click.argument('filename')
@click.pass_context
def remove(ctx, pid, filename):
    """Removefile from deposit with given pid."""
    try:
        ctx.obj.cap_api.remove_file(pid=pid, filename=filename)
        click.echo("File {} removed.".format(filename))

    except BadStatusCode as e:
        logging.error(str(e))

    except Exception as e:
        logging.error('Unexpected error.')
        logging.debug(str(e))
