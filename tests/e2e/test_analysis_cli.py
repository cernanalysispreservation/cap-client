# -*- coding: utf-8 -*-
#
# This file is part of CERN Analysis Preservation Framework.
# Copyright (C) 2021 CERN.
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

import json, os


def test_analysis_get_drafts_e2e(cli_run, user_tokens):
    # create a draft analysis
    user_tokens("info@inveniosoftware.org")

    create_draft_res = cli_run('analysis create --json {} --type cms-analysis')

    # get the pid of the draft
    draft_pid = json.loads(create_draft_res.output).get('pid')

    # test `analysis get`
    res = cli_run(f'analysis get -p {draft_pid}')
    assert res.exit_code == 0
    assert draft_pid in res.output

    # delete the draft
    cli_run(f'analysis delete -p {draft_pid}')