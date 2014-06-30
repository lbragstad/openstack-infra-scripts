Several basic scripts I use for OpenStack Infrastructure related tasks.

recent_bugs.py is intended to summarize the bugs opened in a given Launchpad
project, over a given period of time, the default is two days.

```
$ python recent_bugs.py -h
usage: recent_bugs.py [-h] [-d DAYS] -p PROJECT

summarize bugs from a launchpad project

optional arguments:
  -h, --help            show this help message and exit
  -d DAYS, --days DAYS  history in number of days
  -p PROJECT, --project PROJECT
                        launchpad project to pull bugs from

```

For example, the following will gather all OpenStack Keystone bugs opened
in the last week:

`$ python recent_bugs.py -d 7 -p keystone`
