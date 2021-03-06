# Copyright 2017 BBVA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import uuid

from datetime import datetime
from sqlalchemy import text
from behave import then, given


@then(u'the scan analysis_done is equals analysis_count')
def step_impl(context):
    sql = text('SELECT * FROM scan WHERE id = :scan_id')
    results = context.engine.execute(sql, scan_id=context.scan_id).fetchall()

    assert len(results) == 1  # this scan has 1 fetch
    assert results[0]['analysis_done'] == results[0]['analysis_count']
    assert results[0]['analysis_done'] > 0


@then(u'the scan state is {state}')
def step_impl(context, state):
    sql = text('SELECT * FROM scan WHERE id = :scan_id')
    results = context.engine.execute(sql, scan_id=context.scan_id).fetchall()

    assert len(results) == 1  # this scan has 1 fetch
    assert results[0]['state'] == state


@then(u'the results for the analysis in the database exists')
def step_impl(context):
    sql = text('SELECT * FROM scan_analysis_vulnerability WHERE scan_analysis_id = :scan_analysis_id')
    results = context.engine.execute(sql, scan_analysis_id=context.scan_analysis_id).fetchall()

    assert len(results) > 0  # this scan has at least 1 vuln


@given(u'a plugin for "{plugin_name}" exists in the plugin table for lang "{lang}"')
def step_impl(context, plugin_name, lang):
    """Plugins should be already loaded in the system and the database.
    Deactivate all except for the required one, and get its ID"""
    sql = text('UPDATE plugin SET active = :active WHERE name != :name AND lang != :lang')
    context.engine.execute(sql, active=False, name=plugin_name, lang=lang)

    sql = text('SELECT id FROM plugin WHERE active = :active AND name = :name AND lang = :lang')
    result = context.engine.execute(sql, active=True, name=plugin_name, lang=lang).fetchall()
    assert len(result) == 1
    plugin_row = result[0]
    context.plugin_id = plugin_row[0]


@given(u'a project with "{repo}" repo exists in the database')
def step_impl(context, repo):
    project_id = uuid.uuid4()
    sql = text('INSERT INTO project (id, repo) VALUES (:id, :repo)')
    context.engine.execute(sql, id=project_id, repo=repo)
    context.project_id = project_id


@given(u'a scan for lang "{lang}" exists for the project')
def step_impl(context, lang):
    scan_id = '123'
    sql = text('INSERT INTO scan (id, project_id, lang, created) VALUES (:id, :project_id, :lang, :created)')
    context.engine.execute(sql, id=scan_id, project_id=context.project_id, lang=lang, created=datetime.now())
    context.scan_id = scan_id


@then(u'{created} scan analysis is generated in the database')
def step_impl(context, created):
    sql = text('SELECT * FROM scan_analysis')
    results = context.engine.execute(sql).fetchall()

    assert len(results) == int(created)
    analysis = results[0]
    context.scan_analysis_id = analysis[0]  # id


@then(u'the results for the scan in the database exists')
def step_impl(context):
    sql = text('SELECT * FROM scan_vulnerability WHERE scan_id = :scan_id')
    results = context.engine.execute(sql, scan_id=context.scan_id).fetchall()

    assert len(results) > 0  # this scan has at least 1 vuln


@given(u'a project with "{repo}" repo with {repo_auth_type} repo auth type exists in the database')
def step_impl(context, repo, repo_auth_type):
    project_id = '123'

    sql = text('INSERT INTO project (id, repo, repo_auth_type) '
               'VALUES (:id, :repo, :repo_auth_type)')

    context.engine.execute(sql,
                           id=project_id,
                           repo=repo,
                           repo_auth_type=repo_auth_type)

    context.project_id = project_id
