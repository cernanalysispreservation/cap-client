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
"""Files API class."""

import os
import tarfile
import tempfile

from click import UsageError
from future.moves.urllib.parse import urljoin

from .base import CapAPI


class FilesAPI(CapAPI):
    """Interface for CAP files methods."""

    def get(self, pid):
        """Get list of files attached to analysis.

        :param pid: analysis PID
        :type pid: str
        :return: list of files
        :rtype: list
        """
        return self._make_request(url='deposits/{}/files'.format(pid))

    def download(self, pid, filename, output_filepath=None):
        """Download a file attached to your analysis.

        :param pid: analysis PID
        :type pid: str
        :param filename: filename
        :type filename: str
        :param output_filepath: save your file as..
        :type output_filepath: str, optional
        :return: None
        """
        if output_filepath:
            dirpath = os.path.dirname(output_filepath)
            if dirpath and not os.path.exists(dirpath):
                raise UsageError(
                    'Directory {} does not exist.'.format(dirpath))

        bucket_url = self._get_bucket_link(pid)
        data = self._make_request(
            url=bucket_url + '/' + filename,
            headers={},
            stream=True,
        )

        with open(output_filepath or filename, 'wb') as fp:
            fp.write(data.content)

    def upload_directory(self, pid, filepath, output_filename=None):
        """Upload a directory to your analysis.

        :param pid: analysis PID
        :type pid: str
        :param filepath: filepath to uploaded file
        :type filepath: str
        :param output_filename: save your file as..
        :type output_filename: str
        :return: None
        """
        bucket_url = self._get_bucket_link(pid)
        fname = output_filename or os.path.basename(filepath)
        fname = fname if fname.endswith('.tar.gz') else fname + '.tar.gz'

        with tempfile.TemporaryFile() as fp:
            with tarfile.open(fileobj=fp, mode='w:gz') as tar:
                tar.add(filepath)

            fp.flush()
            fp.seek(0)

            self._make_request(
                url=bucket_url + '/' + fname,
                method='put',
                headers={},
                data=fp,
            )

    def upload_file(self, pid, filepath, output_filename=None):
        """Upload a file to your analysis.

        :param pid: analysis PID
        :type pid: str
        :param filepath: filepath to uploaded file
        :type filepath: str
        :param output_filename: save your file as..
        :type output_filename: str
        :return: None
        """
        bucket_url = self._get_bucket_link(pid)
        fname = output_filename or os.path.basename(filepath)

        with open(filepath, 'rb') as fp:
            self._make_request(
                url=bucket_url + '/' + fname,
                method='put',
                headers={},
                data=fp,
            )

    def remove(self, pid, filename):
        """Remove a file attached to your analysis.

        :param pid: analysis PID
        :type pid: str
        :param filename: filename
        :type filename: str
        :return: None
        """
        bucket_url = self._get_bucket_link(pid)

        self._make_request(
            url=bucket_url + '/' + filename,
            method='delete',
            expected_status_code=204,
        )

    def _get_bucket_link(self, pid):
        """Make request to server to fetch link to analysis bucket.

        :param pid: analysis PID
        :type pid: str
        :return: url to analysis bucket
        :rtype: str
        """
        ana = self._make_request(urljoin('deposits/', pid))
        return ana['links']['bucket']
