### Finding Recent Bugs

Some basic scripts for wrangling bug information from Launchpad.

recent_bugs.py is intended to summarize the bugs opened in a given Launchpad
project, over a given period of time, the default is two days.

```
$ python recent_bugs.py -h
usage: recent_bugs.py [-h] [-d DAYS] [-f] -p PROJECT [PROJECT ...]

summarize bugs from a launchpad project

optional arguments:
  -h, --help            show this help message and exit
  -d DAYS, --days DAYS  history in number of days
  -f, --formatting      output report in generated HTML
  -p PROJECT [PROJECT ...], --project PROJECT [PROJECT ...]
                        launchpad project to pull bugs from
```

For example, the following will gather all OpenStack Keystone bugs opened
in the last week:

`$ python recent_bugs.py -d 7 -p keystone`

You can also use the `--formatting` option to output bug reports in HTML and
write them out to files, for example:

`$ python recent_bugs.py -d 7 -f -p keystone > /var/www/html/bug_report.html`

The above command will generate a weekly bug report for Keystone, format the
output as HTML, and write it out to an HTML file. This can be handy for setting
up cronjobs to run on a schedule and publish reports.

### Installing Dependencies

To run this script, you'll need launchpadlib

```
$ pip install --allow-all-external --allow-unverified \
lazr.authentication launchpadlib
```
