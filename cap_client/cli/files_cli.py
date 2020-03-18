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

import click

from ..utils import json_dumps, logger


@click.group()
def files():
    """Files managing commands."""


@files.command()
@click.option(
    '--pid',
    '-p',
    required=True,
    help='Upload file to deposit with given pid',
)
@click.option(
    '--output-file',
    '-o',
    help='Filename to be given to uploaded file',
)
@click.option(
    '--yes',
    is_flag=True,
    default=False,
    help="Bypasses prompts..Say YES to everything",
)
@click.argument(
    'file',
    type=click.Path(exists=False),
)
@click.pass_context
@logger
def upload(ctx, pid, file, output_file, yes):
    """Upload file to deposit with given pid."""
    ctx.obj.cap_api.upload_file(pid=pid,
                                filepath=file,
                                output_filename=output_file,
                                yes=yes)

    click.echo("File uploaded successfully.")


@files.command()
@click.option(
    '--pid',
    '-p',
    required=True,
    help='Get file uploaded with deposit with given pid',
)
@click.option(
    '--output-file',
    '-o',
    help='Filename to be given to uploaded file',
)
@click.argument('filename')
@click.pass_context
@logger
def download(ctx, pid, filename, output_file):
    """Download file uploaded with given deposit."""
    ctx.obj.cap_api.download_file(pid, filename, output_file)

    click.echo("File saved as {}".format(output_file or filename))


@files.command()
@click.option(
    '--pid',
    '-p',
    help='List files of deposit with given pid',
    required=True,
)
@click.pass_context
@logger
def get(ctx, pid):
    """List files associated with deposit with given pid."""
    res = ctx.obj.cap_api.get_files(pid=pid)

    click.echo(json_dumps(res))


@files.command()
@click.option(
    '--pid',
    '-p',
    help='Remove file from deposit with given pid',
    required=True,
)
@click.argument('filename')
@click.pass_context
@logger
def remove(ctx, pid, filename):
    """Removefile from deposit with given pid."""
    ctx.obj.cap_api.remove_file(pid=pid, filename=filename)

    click.echo("File {} removed.".format(filename))
