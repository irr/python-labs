#!/usr/bin/env python

"""A fork that demonstrates a copied environment"""

import os, psutil, time
from os import environ

def loop(p):
    for i in range(10):
        print os.getpid(), "...", p.get_cpu_affinity()
        time.sleep(2)

def my_fork():
    environ['FOO']="baz"
    print "FOO environmental variable set to: %s" % environ['FOO']
    environ['FOO']="bar"
    print "FOO environmental variable changed to: %s" % environ['FOO']
    child_pid = os.fork()
    if child_pid == 0:
        p = psutil.Process(os.getpid())
        p.set_cpu_affinity([1])
        print "Child Process: PID# %s [%s]" % (os.getpid(), p.get_cpu_affinity())
        print "Child FOO environmental variable == %s" % environ['FOO']
        loop(p)
    else:
        p = psutil.Process(os.getpid())
        p.set_cpu_affinity([0])
        print "Parent Process: PID# %s [%s]" % (os.getpid(), p.get_cpu_affinity())
        print "Parent FOO environmental variable == %s" % environ['FOO']
        loop(p)

if __name__ == "__main__":
    my_fork()
