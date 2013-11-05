#!/usr/bin/env python

from datetime import datetime, timedelta
from random import choice, randrange, random
import time

USERS = ["irocha", "irr", "alessandra", "babi", "luma", "lara"]
METHODS = ["GET", "PUT", "POST", "DELETE"]
STATUS = { "GET" : 200, "PUT" : 201, "POST" : 204, "DELETE" : 204 }
USERAGENTS = ["Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.56 Safari/537.17",
              "Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201",
              "Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))",
              "Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02",
              "Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25"
              ]
HOSTS = ["10.133.133.189", "10.133.133.181", "10.133.9.119", "10.133.9.125", "10.133.9.127"]
CONTAINERS = ["/pub", "/priv", "/www", "/root", "/", ""]
OBJECTS = ["/linux.jpg", "/index.html", "/index.json", ""]

TEMPLATE = r'%(host1)s - - [%(time)s -0200]  "%(method)s /vi1/IRR_%(user)s%(container)s%(object)s HTTP/1.1" %(status)d %(size)d "-" "%(useragent)s" . 13 %(length)d %(host2)s:8080 upstream_response_time %(rt1)0.3f msec %(msec).3f request_time %(rt2)0.3f'

pc = datetime.utcnow()
pc = pc - timedelta(days = randrange(265) + 100)

def randomize():
    global pc
    data = {}
    data["host1"] = choice(HOSTS)
    while True:
        host = choice(HOSTS)
        if host != data["host1"]:
            data["host2"] = host
            break
    data["user"] = choice(USERS)
    data["method"] = choice(METHODS)
    data["status"] = STATUS[data["method"]]
    data["container"] = choice(CONTAINERS)
    data["object"] = (len(data["container"]) > 0) and choice(OBJECTS) or ""
    pc = pc + timedelta(seconds = randrange(10))
    data["time"] = pc.strftime("%d/%b/%Y:%H:%M:%S") 
    data["useragent"] = choice(USERAGENTS)
    if data["method"] == "DELETE":
        data["size"] = 0
        data["length"] = randrange(50) + 100
    elif data["method"] == "POST":
        data["size"] = 0
        data["length"] = randrange(100) + 100    
    elif data["method"] == "PUT":
        data["size"] = randrange(40) + 10
        data["length"] = randrange(1073741824) + 100     
    elif data["method"] == "GET":
        data["size"] = randrange(1073741824) + 100     
        data["length"] = randrange(200) + 100
    data["rt1"] = random()
    data["rt2"] = random()
    data["msec"] = time.time()
    return data

print TEMPLATE % randomize()
