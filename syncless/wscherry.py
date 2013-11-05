import sys
sys.path.append("/usr/lib/python2.7/site-packages")

import redis
_r = redis.Redis(host='localhost', port=6379, db=0)

import cherrypy

class Test(object):
    def index(self):
        _r.incr("/")
        return "OK!"
    index.exposed = True

cherrypy.quickstart(Test())
