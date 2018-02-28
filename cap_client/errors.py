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

"""CAP client exceptions."""

import json


class BadStatusCode(Exception):
    """Exception for status code different than expected."""

    def __init__(self,
                 message=None,
                 expected_status_code=None,
                 status_code=None,
                 endpoint=None,
                 data=None,
                 **kwargs):
        """Initialize BadStatusCode."""
        super(Exception, self)
        self.message = message
        self.expected_status_code = expected_status_code
        self.status_code = status_code
        self.endpoint = endpoint
        self.data = data

    def __str__(self):
        """Print BadStatusCode exception's details."""
        return "Something went wrong when trying to connect to {endpoint}\n" \
               "Server replied with:\n" \
               "{data}" .format(endpoint=self.endpoint,
                                data=json.dumps({'status': self.status_code,
                                                 'data': self.data
                                                 }, indent=4))


class UnknownAnalysisType(Exception):
    """Analysis type not supported."""

    def __init__(self,
                 types=None,
                 **kwargs):
        """Initialize UnknownAnalysisType."""
        super(Exception, self)
        self.types = types

    def __str__(self):
        """Print UnknownAnalysisType exception's details."""
        return "Choose one of the available analyses types:\n{}".format(
                '\n'.join(self.types))


class MissingJsonFile(Exception):
    """Json file not provided."""

    def __str__(self):
        """Print MissingJsonFile exception's details."""
        return "Please provide a JSON file for the analysis. " \
               "If you don't know the analysis fields, first call " \
               "cap-client get-schema --type <analysis-type> ."
