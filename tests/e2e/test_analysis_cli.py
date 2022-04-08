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

import json
import time
import pytest


@pytest.mark.vcr
def test_analysis_get_drafts_e2e(cli_run, user_tokens, vcr_config):
    # apply the token
    user_tokens('info@inveniosoftware.org')

    # create a draft analysis
    create_draft_res = cli_run('analysis create --json {} --type cms-analysis')

    # get the pid of the draft
    draft_pid = json.loads(create_draft_res.output).get('pid')

    # test `analysis get`
    res = cli_run(f'analysis get -p {draft_pid}')
    assert res.exit_code == 0
    assert draft_pid in res.output

    # delete the draft
    cli_run(f'analysis delete -p {draft_pid}')


@pytest.mark.vcr
def test_analysis_get_drafts_with_page_without_results(cli_run, user_tokens, vcr_config):
    # apply the token
    user_tokens('info@inveniosoftware.org')

    # create draft analyses
    create_draft_res_one = cli_run('analysis create --json {} --type alice-analysis')
    create_draft_res_two = cli_run('analysis create --json {} --type cms-analysis')
    draft_pid_one = json.loads(create_draft_res_one.output).get('pid')
    draft_pid_two = json.loads(create_draft_res_two.output).get('pid')

    # test `analysis get --page`
    res = cli_run('analysis get --page 2')
    assert res.exit_code == 0
    assert len(json.loads(res.output)) == 0
    cli_run(f'analysis delete -p {draft_pid_one}')
    cli_run(f'analysis delete -p {draft_pid_two}')


@pytest.mark.vcr
def test_analysis_get_drafts_with_page_with_results(cli_run, user_tokens, vcr_config):
    # apply the token
    user_tokens('info@inveniosoftware.org')

    # create draft analyses
    create_draft_res_one = cli_run('analysis create --json {} --type alice-analysis')
    time.sleep(2)
    create_draft_res_two = cli_run('analysis create --json {} --type cms-analysis')
    time.sleep(2)
    draft_pid_one = json.loads(create_draft_res_one.output).get('pid')
    draft_pid_two = json.loads(create_draft_res_two.output).get('pid')

    # test `analysis get --page`
    res = cli_run('analysis get --size 1 --page 2')
    assert res.exit_code == 0
    assert len(json.loads(res.output)) >= 1
    cli_run(f'analysis delete -p {draft_pid_one}')
    cli_run(f'analysis delete -p {draft_pid_two}')


@pytest.mark.vcr
def test_analysis_get_drafts_with_size(cli_run, user_tokens, vcr_config):
    # apply the token
    user_tokens('info@inveniosoftware.org')

    # create draft analyses
    create_draft_res_one = cli_run('analysis create --json {} --type alice-analysis')
    time.sleep(2)
    create_draft_res_two = cli_run('analysis create --json {} --type cms-analysis')
    time.sleep(2)
    draft_pid_one = json.loads(create_draft_res_one.output).get('pid')
    draft_pid_two = json.loads(create_draft_res_two.output).get('pid')

    # test `analysis get --size`
    res = cli_run('analysis get --size 1')
    assert res.exit_code == 0
    assert len(json.loads(res.output)) == 1
    cli_run(f'analysis delete -p {draft_pid_one}')
    cli_run(f'analysis delete -p {draft_pid_two}')


@pytest.mark.vcr
def test_analysis_get_drafts_with_sort(cli_run, user_tokens, vcr_config):
    # apply the token
    user_tokens('info@inveniosoftware.org')

    # create draft analyses
    create_draft_res_one = cli_run('analysis create --json {} --type alice-analysis')
    time.sleep(2)
    create_draft_res_two = cli_run('analysis create --json {} --type cms-analysis')
    time.sleep(2)
    draft_pid_one = json.loads(create_draft_res_one.output).get('pid')
    draft_pid_two = json.loads(create_draft_res_two.output).get('pid')

    # test `analysis get --sort`
    res = cli_run('analysis get --sort mostrecent')
    assert res.exit_code == 0
    assert json.loads(res.output)[0].get('pid') == draft_pid_two
    cli_run(f'analysis delete -p {draft_pid_one}')
    cli_run(f'analysis delete -p {draft_pid_two}')
