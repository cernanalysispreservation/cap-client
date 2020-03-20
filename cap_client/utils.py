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
"""CAP Client Utils."""
import functools
import json
import logging
import os
import re
import tarfile
from functools import wraps
from sys import exit

import click
from click import BadParameter, ClickException

from .errors import BadStatusCode, CLIError


def make_tarfile(output_filename, source_dir):
    """Make a tarball out of {source_dir} into {output_filename}."""
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


def validate_version(ctx, param, version_value):
    """Validate the schema version requested."""
    if version_value:
        matched = re.match(r"(\d+).(\d+).(\d+)", version_value)
        if not matched:
            raise BadParameter(
                'Version has to be passed as string <major>.<minor>.<patch>')
        return version_value

    return None


def logger(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):
        try:
            fun(*args, **kwargs)
        except ClickException as e:
            e.show()
            exit(1)
        except BadStatusCode as e:
            logging.debug(e.data)
            click.secho(str(e), fg='red')
            exit(1)
        except CLIError as e:
            click.secho(str(e), fg='red')
            exit(1)
        except Exception as e:
            logging.debug(str(e))
            click.echo('The client encountered an unexpected error.\n'
                       'Try again or use --verbose flag to see more details.')
            exit(1)

    return wrapper


json_dumps = functools.partial(json.dumps, indent=4)
