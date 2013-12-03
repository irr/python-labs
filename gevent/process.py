#!/usr/bin/env python
import gevent
from gevent import subprocess

# run 2 jobs in parallel
p1 = subprocess.Popen(['uname'], stdout=subprocess.PIPE)
p2 = subprocess.Popen(['ls'], stdout=subprocess.PIPE)

gevent.wait([p1, p2], timeout=10)

# print the results (if available)
if p1.poll() is not None:
    print ('uname: %r (%d)' % (p1.stdout.read(), p1.returncode))
else:
    print ('uname: job is still running')

if p2.poll() is not None:
    print ('ls: %r (%d)' % (p2.stdout.read(), p2.returncode))
else:
    print ('ls: job is still running')
