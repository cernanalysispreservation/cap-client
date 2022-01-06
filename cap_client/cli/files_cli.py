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
"""Files CAP Client CLI."""

import os

import click

from cap_client.api import FilesAPI
from cap_client.utils import ColoredGroup, json_dumps, logger, pid_option, load_file_names_from_directory

pass_api = click.make_pass_decorator(FilesAPI, ensure=True)


@click.group(cls=ColoredGroup)
def files():
    """Manage analysis files."""


@files.command()
@pid_option(required=True)
@logger
@pass_api
def get(api, pid):
    """Get list of files attached to analysis with given PID."""
    res = api.get(pid=pid)

    click.echo(json_dumps(res))


@files.command()
@pid_option(required=True)
@click.option(
    '--output-filename',
    '-o',
    help='Upload file as..',
)
@click.option(
    '--yes-i-know',
    is_flag=True,
    default=False,
    help="Bypasses prompts..Say YES to everything",
)
@click.option(
    '--dir-files',
    '-df',
    type=click.Path(exists=True),
    help='Upload all the files individually of the specified directory.',
)
@click.argument(
    'path',
    nargs=-1,
    type=click.Path(exists=True),
)
@logger
@pass_api
def upload(api, pid, path, output_filename, yes_i_know, dir_files):
    """Upload a file to your analysis."""
    if not path and not dir_files:
        click.echo("Error: Missing argument 'PATH' or option 'DIR_FILES'.")
        return

    file_names = list(path) if path else []
    if dir_files:
        file_names += load_file_names_from_directory(dir_files)
        if file_names:
            if not yes_i_know and not click.confirm(
                "{} contains {} files. Do you want to upload them individually?".format(
                    dir_files, len(file_names)
                )
            ):
                click.echo("Use 'PATH' argument for uploading as tarball.")
                return
        else:
            click.echo("No files found in parent directory {}.".format(dir_files))

    for _file in file_names:
        if os.path.isdir(_file):
            if yes_i_know or click.confirm(
                "{} is a directory. Do you want to upload a tarball?".format(_file)
            ):
                api.upload_directory(
                    pid=pid,
                    filepath=_file,
                    output_filename=output_filename,
                )
                click.echo("Directory {} uploaded successfully.".format(_file))
            else:
                click.echo("Use --dir-files for uploading files individually.")
                click.echo("Aborting upload of {}.".format(_file))
                continue
        elif os.stat(_file).st_size != 0:
            api.upload_file(
                pid=pid,
                filepath=_file,
                output_filename=output_filename,
            )
            click.echo("File {} uploaded successfully.".format(_file))


@files.command()
@pid_option(required=True)
@click.option(
    '--output-file',
    '-o',
    type=click.Path(exists=False),
    help='Download file as..',
)
@click.option(
    '--yes-i-know',
    is_flag=True,
    default=False,
    help="Bypasses prompts..Say YES to everything",
)
@click.argument('filename')
@logger
@pass_api
def download(api, pid, filename, output_file, yes_i_know):
    """Download file uploaded with given deposit."""
    if not yes_i_know:
        path = output_file or filename
        if os.path.exists(path):
            if not click.confirm(
                    text="File already exists. Do you want to overwrite?",
                    default=False,
                    abort=False,
                    show_default=True):
                click.echo("Aborting download of {}".format(output_file or filename))
                return
    api.download(pid, filename, output_file)

    click.echo("File saved as {}".format(output_file or filename))


@files.command()
@pid_option(required=True)
@click.argument('filename')
@logger
@pass_api
def remove(api, pid, filename):
    """Removefile from deposit with given pid."""
    api.remove(pid=pid, filename=filename)

    click.echo("File {} removed.".format(filename))
