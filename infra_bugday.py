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
import re

import json
from launchpadlib.launchpad import Launchpad
import requests

LPCACHEDIR = os.path.expanduser(os.environ.get('LPCACHEDIR',
                                               '~/.launchpadlib/cache'))
LPPROJECT = os.environ.get('LPPROJECT',
                           'openstack-ci')
LPSTATUS = ('New', 'Confirmed', 'Triaged', 'In Progress')

RE_LINK = re.compile(' https://review.openstack.org/(\d+)')


def get_reviews_from_bug(bug):
    """Return a list of gerrit reviews extracted from the bug's comments."""
    reviews = set()
    for comment in bug.messages:
        reviews |= set(RE_LINK.findall(comment.content))
    return reviews


def get_review_status(review_number):
    """Return status of a given review number."""
    r = requests.get("https://review.openstack.org:443/changes/%s"
                     % review_number)
    # strip off first few chars because 'the JSON response body starts with a
    # magic prefix line that must be stripped before feeding the rest of the
    # response body to a JSON parser'
    #https://review.openstack.org/Documentation/rest-api.html
    return json.loads(r.text[4:])['status']


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
        for line in map(lambda x: "(%s - %s)" %
                        (x.bug_target_name, x.status),
                        bug.bug_tasks):
            print line
        for review in get_reviews_from_bug(bug):
            print (" - https://review.openstack.org/%s -- %s"
                   % (review, get_review_status(review)))


if __name__ == "__main__":
    main()
