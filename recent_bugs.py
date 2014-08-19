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

LPCACHEDIR = os.path.expanduser(os.environ.get('LPCACHEDIR',
                                               '~/.launchpadlib/cache'))

LPSTATUS = ('New', 'Confirmed', 'Triaged', 'In Progress')


def is_bug_recent(bug, num_of_days):
    """Determine if a bug was created in the last X days."""
    invalid_states = ["Incomplete", "Opinion", "Won't Fix", "Expired",
                      "Fix Released", "Fix Committed"]
    if bug.status not in invalid_states:
        # Create timedelta object to compare bug creation times against.
        # Let's print out the bug from the last two days.
        delta = datetime.timedelta(days=num_of_days)
        today = datetime.datetime.today()
        # Replace tzinfo so that it doesn't mess with comparisons.
        bug_created_time = bug.date_created.replace(tzinfo=None)
        if bug_created_time >= today - delta:
            return True


def generate_html_header():
    print('<!DOCTYPE html>')
    print('<html><body><pre style="font-family:verdana;font-size:15px">')


def generate_html_footer():
    print('</pre></body></html>')


def print_entry_in_html(bug, bug_counter):
    print "%d. [%s:%s] <a href=\"%s\" target=\"_blank\">%s</a>" % (
            bug_counter, bug.importance, bug.status, bug.web_link, bug.title)
    if bug.assignee is not None:
        print "\tAssigned to %s\n" % (bug.assignee.display_name)
    else:
        print "\tNot Assigned\n"

    #print "<a href=\"%s\">\t%s</a> \n" % (bug.web_link, bug.title)


def print_entry(bug, bug_counter):
    print "%d. [%s:%s] %s" % (bug_counter,
                              bug.importance,
                              bug.status,
                              bug.title)
    if bug.assignee is not None:
        print "\tAssigned to %s" % (bug.assignee.display_name)
    else:
        print "\tNot Assigned"

    print "\t%s \n" % (bug.web_link)


def main():
    parser = argparse.ArgumentParser(description='summarize bugs from a '
             'launchpad project')
    parser.add_argument('-d', '--days',
            default='2',
            type=int,
            help='history in number of days')
    parser.add_argument('-f', '--formatting',
                        action='store_true',
                        help='output report in generated HTML')
    parser.add_argument('-p', '--project',
            nargs=1,
            required=True,
            help='launchpad project to pull bugs from')
    args = parser.parse_args()

    launchpad = Launchpad.login_anonymously('OpenStack Recent Bugs',
                                            'production',
                                            args.project[0])

    if args.formatting:
        generate_html_header()
        output_method = print_entry_in_html
    else:
        output_method = print_entry

    project = launchpad.projects[args.project[0]]
    bug_counter = 0

    for bug in project.searchTasks(status=LPSTATUS,
                                   omit_duplicates=True,
                                   order_by='-importance'):
        if is_bug_recent(bug, args.days):
            output_method(bug, bug_counter)
            bug_counter += 1

    if args.formatting:
        generate_html_footer()


if __name__ == '__main__':
    main()
