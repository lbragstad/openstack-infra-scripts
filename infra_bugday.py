#! /usr/bin/env python
# Copyright (c) 2013 Hewlett-Packard Development Company, L.P.
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
#
# infra_bugday.py pulls out all the bugs from the openstack-ci project in
# launchpad

import os
import sys
from launchpadlib.launchpad import Launchpad


LPCACHEDIR = os.path.expanduser(os.environ.get('LPCACHEDIR',
                                               '~/.launchpadlib/cache'))
LPPROJECT = os.environ.get('LPPROJECT',
                           'openstack-ci')
LPSTATUS = ('New', 'Confirmed', 'Triaged', 'In Progress')


def main():
    launchpad = Launchpad.login_anonymously('OpenStack Infra Bugday',
                                            'production',
                                            LPCACHEDIR)
    project = launchpad.projects[LPPROJECT]
    for task in project.searchTasks(status=LPSTATUS,
                                    omit_duplicates=True,
                                    order_by='-importance'):
        bug = launchpad.load(task.bug_link)
        print '[%s] %s %s' % (task.importance, bug.title, task.web_link)
        print 'COPIED FROM LAST REVIEW:\n'


if __name__ == "__main__":
    main()
