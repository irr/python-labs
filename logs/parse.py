#!/usr/bin/env python

from email.utils import parsedate_tz, mktime_tz

import re

PARTS = [
    r'(?P<host>\S+)',                   # host %h
    r'\S+',                             # indent %l (unused)
    r'(?P<user>\S+)',                   # user %u
    r'\[(?P<time>.+)\]',                # time %t
    r'"(?P<request>.+)"',               # request "%r"
    r'(?P<status>[0-9]+)',              # status %>s
    r'(?P<size>\S+)',                   # size %b (careful, can be '-')
    r'"(?P<referer>.*)"',               # referer 
    r'"(?P<agent>.*)"',                 # user agent
    r'(?P<pipe>.*)',                    # pipe
    r'(?P<connection>[0-9]+)',          # connection
    r'(?P<length>[0-9]+)',              # request length
    r'.*',      
]

PATTERN = re.compile(r'\s+'.join(PARTS)+r'\s*\Z')

def num(s):
    try:
        return int(s)
    except exceptions.ValueError:
        return 0


def parse(line):
    try:
        m = PATTERN.match(line)
        if m:
            d = m.groupdict()
            if d["status"][:2] == "20":
                # 30/Jan/2013:08:55:18 -0200 => 30 Jan 2013 08:55:18 -0200 (RFC822)
                d["utc"] = parsedate_tz(d["time"].replace("/", " ").replace(":", " ", 1))
                d["epoch"] = mktime_tz(d["utc"])
                d["bytes"] = num(d["request"].startswith("GET") and d["size"] or d["length"])
                return d
        return None
    except:
        return None


fname = "./test.log"

with open(fname) as f:
    for line in f:
        d = parse(line)
        if d:
            print d["time"], d["epoch"], d["request"], d["bytes"]


