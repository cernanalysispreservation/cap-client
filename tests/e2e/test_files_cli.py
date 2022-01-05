# -*- coding: utf-8 -*-
#
# This file is part of CERN Analysis Preservation Framework.
# Copyright (C) 2022 CERN.
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

import os
import json
import pytest


@pytest.mark.vcr
def test_files_upload_and_download(cli_run, user_tokens, vcr_config):
    # apply the token
    user_tokens('info@inveniosoftware.org')

    # create a draft analysis
    create_draft_res = cli_run('analysis create --json {} --type cms-analysis')

    # get the pid of the draft
    draft_pid = json.loads(create_draft_res.output).get('pid')

    with open('file.txt', 'wb') as fp:
        fp.write(b'Hello world')

    # test `files upload`
    res_upload = cli_run(f'files upload -p {draft_pid} file.txt')
    assert res_upload.exit_code == 0
    assert res_upload.stripped_output == 'File uploaded successfully.'
    os.remove('file.txt')

    # test `files download`
    res_download = cli_run(f'files download -p {draft_pid} file.txt')
    assert res_download.exit_code == 0
    assert res_download.stripped_output == 'File saved as file.txt'

    # delete the draft
    cli_run(f'analysis delete -p {draft_pid}')
