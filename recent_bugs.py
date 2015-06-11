#! /usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import argparse
import datetime
import os

from launchpadlib.launchpad import Launchpad
from lxml import html
from lxml.html import builder as E

LPCACHEDIR = os.path.expanduser(os.environ.get('LPCACHEDIR',
                                               '~/.launchpadlib/cache'))

LPSTATUS = ('New', 'Confirmed', 'Triaged', 'In Progress')


def is_bug_recent(bug, num_of_days):
    """Determine if a bug was created in the last X days."""
    invalid_states = ["Incomplete", "Opinion", "Won't Fix", "Expired",
                      "Fix Released", "Fix Committed"]
    if bug.status not in invalid_states:
        # Create timedelta object to compare bug creation times against.
        delta = datetime.timedelta(days=num_of_days)
        today = datetime.datetime.today()
        # Replace tzinfo so that it doesn't mess with comparisons.
        bug_created_time = bug.date_created.replace(tzinfo=None)
        if bug_created_time >= today - delta:
            return True
        return False
    return False


def get_project(project_name):
    """Return a launchpad project object given a project name."""
    lp = Launchpad.login_anonymously('OpenStack Recent Bugs', 'production',
                                     project_name)
    return lp.projects[project_name]


def get_open_project_bugs(project):
    """Given a launchpad project object, grab all bugs."""
    project_bugs = project.searchTasks(status=LPSTATUS,
                                       omit_duplicates=True,
                                       order_by='-importance')
    return project_bugs


def get_project_report(project_name, project_bugs):
    """Return html from a list of bugs."""
    report = E.BODY(E.H2(E.CLASS("heading"), "%s (%d)" % (
        project_name, len(project_bugs))))
    for bug in project_bugs:
        bug_link = E.A(bug.title, href=bug.web_link, target='_blank')
        report.append(E.P("[%s:%s] " % (bug.importance, bug.status),
                      bug_link))
        if bug.assignee:
            report.append(E.P("Assigned to: %s" % (bug.assignee.display_name)))
    return report


def main(days, project_names):
    reports = []
    for project_name in project_names:
        try:
            project = get_project(project_name)
        except KeyError:
            raise Exception('%s does not exist in Launchpad' % project_name)

        open_project_bugs = get_open_project_bugs(project)
        recent_project_bugs = []
        for bug in open_project_bugs:
            if is_bug_recent(bug, days):
                recent_project_bugs.append(bug)

        # format bugs into html
        reports.append(get_project_report(project_name, recent_project_bugs))

    entire_bug_report = E.HTML()
    for report in reports:
        entire_bug_report.append(report)

    print html.tostring(entire_bug_report)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='summarize bugs from a '
                                     'launchpad project')
    parser.add_argument('-d',
                        '--days',
                        default='2',
                        type=int,
                        help='history in number of days')
    parser.add_argument('-p',
                        '--project',
                        nargs='+',
                        required=True,
                        help='launchpad project(s) to pull bugs from')
    args = parser.parse_args()

    main(args.days, args.project)
