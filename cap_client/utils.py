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

from click_help_colors import HelpColorsGroup


class ColoredGroup(HelpColorsGroup):
    """CAP command group with predefined colors."""
    def __init__(self, *args, **kwargs):
        """Initialize."""
        kwargs.setdefault('help_headers_color', 'bright_cyan')
        kwargs.setdefault('help_options_color', 'cyan')
        super(ColoredGroup, self).__init__(*args, **kwargs)


def make_tarfile(output_filename, source_dir):
    """Make a tarball out of {source_dir} into {output_filename}."""
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


def validate_version(ctx, param, version_value):
    """Validate the schema version requested."""
    if version_value:
        matched = re.match(r"(\d+)\.(\d+)\.(\d+)", version_value)
        if not matched:
            raise BadParameter(
                'Version has to be passed as string <major>.<minor>.<patch>')
        return version_value

    return None


def load_json_from_file(ctx, param, value):
    """Load json from file parameter."""
    if value is not None:
        try:
            return json.load(value)
        except (KeyError, ValueError):
            raise BadParameter('Not a valid JSON.')


def load_json(ctx, param, value):
    """Load json from parameter."""
    if value is not None:
        try:
            return json.loads(value)
        except (KeyError, ValueError):
            raise BadParameter('Not a valid JSON.')


class MutuallyExclusiveOption(click.Option):
    """Click option required dependent on other options."""
    def __init__(self, *args, **kwargs):
        """Initialize."""
        self.not_required_if = kwargs.pop("not_required_if")
        kwargs["help"] = "{} (mutually exclusive with --{})".format(
            kwargs.get("help", ""), self.not_required_if)
        super(MutuallyExclusiveOption, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        """Parse result handler."""
        is_option_present = self.name in opts
        is_another_option_present = self.not_required_if in opts
        if is_another_option_present:
            if is_option_present:
                raise click.UsageError(
                    "--{} is mutually exclusive with --{}".format(
                        self.name, self.not_required_if),
                    ctx=ctx)
        elif not is_option_present:
            raise click.UsageError("You need to specify --{} or --{}.".format(
                self.name, self.not_required_if),
                                   ctx=ctx)

        return super(MutuallyExclusiveOption,
                     self).handle_parse_result(ctx, opts, args)


def logger(fun):
    """Handle exceptions logging."""
    @wraps(fun)
    def wrapper(*args, **kwargs):
        try:
            fun(*args, **kwargs)
        except ClickException as e:
            raise e
        except Exception as e:
            logging.debug(str(e))
            click.secho(
                'The client encountered an unexpected error.\n'
                'Try again or use --verbose flag to see more details.',
                fg='red')
            exit(1)

    return wrapper


json_dumps = functools.partial(json.dumps, indent=4)


def pid_option(required):
    """Click option for analysis PID."""
    def inner_pid_option(fun):
        """Add pid option to your command."""
        @click.option(
            '--pid',
            '-p',
            required=required,
            help='Your analysis PID (Persistent Identifier)',
        )
        @wraps(fun)
        def wrapper(*args, **kwargs):
            return fun(*args, **kwargs)

        return wrapper

    return inner_pid_option
