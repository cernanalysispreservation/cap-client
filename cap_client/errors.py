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
"""CAP client exceptions."""

import logging

from click import ClickException, secho


class CLIError(ClickException):
    """Base CAP cli exception class."""

    def __str__(self):
        """Error details."""
        return self.message

    def show(self):
        """Show exception details to the user."""
        secho(str(self), fg='red')


class BadStatusCode(CLIError):
    """Response status code not as expected."""

    def __init__(self,
                 message='',
                 expected_status_code=None,
                 status_code=None,
                 endpoint=None,
                 data=None):
        """Initialize BadStatusCode."""
        self.message = message
        self.expected_status_code = expected_status_code
        self.status_code = status_code
        self.endpoint = endpoint
        self.data = data

    def __str__(self):
        """Error details."""
        if not self.message and isinstance(self.data, dict):
            msg = [self.data.get('message', '')]
            # validation errors
            for err in self.data.get('errors', []):
                if 'field' in err and 'message' in err:
                    field = '.'.join(err['field'])
                    msg.append((field + ' ' if field else '') + err['message'])

            return '\n'.join(msg)

        return self.message

    def show(self):
        """Show exception details to the user."""
        logging.debug(self.data)
        super(BadStatusCode, self).show()
