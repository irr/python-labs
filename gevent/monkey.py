import gevent
from gevent import monkey
from gevent.coros import Semaphore

# patches stdlib (including socket and ssl modules) to cooperate with other greenlets
monkey.patch_all()

import urllib2
import memcache
import _mysql
import redis

import unittest

n = 0
sem = Semaphore()

class SyncTest(unittest.TestCase):
    def testMySQL(self):
        (_, v) = do_mysql()
        self.assertEqual('1', v)

    def testMemcache(self):
        (_, v) = do_memcache("irr", "http://irrlab.com/")
        self.assertEqual("http://irrlab.com/", v)

    def testURL(self):
        (_, v) = do_url("http://irrlab.com/")
        self.assertTrue(v > 8192)

    def testRedis(self):
        (_, v) = do_redis("irr", "http://irrlab.com/")
        self.assertEqual("http://irrlab.com/", v)

    def testZ(self):
        global n
        print("Semaphore=%d" % n)
        self.assertEqual(n, 12)

def register():
    global sem, n
    try:
        sem.acquire()
        n = n + 1
        return n
    finally:
        sem.release()

def do_mysql():
    db = _mysql.connect("localhost", "root", "mysql", "mysql")
    db.query("SELECT 1")
    res = db.store_result()
    row = res.fetch_row()[0]
    print("MySQL: %s" % row)
    db.close()    
    return (register(), row[0])

def do_memcache(key, url):
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    mc.set(key, url)
    res = mc.get(key)
    print("Memcache: %s=%s" % (key, res))
    mc.disconnect_all()
    return (register(), res)

def do_url(url):
    data = urllib2.urlopen(url).read()
    size = len(data)
    print('URL: %s: %s bytes' % (url, size))
    return (register(), size)

def do_redis(key, url):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    r.set(key, url)
    res = r.get(key)
    print("Redis: %s=%s" % (key, res))
    r = None
    return (register(), res)

def do_jobs(val):
    (key, url) = val
    gevent.joinall([gevent.spawn(do_mysql), 
                    gevent.spawn(do_memcache, key, url),
                    gevent.spawn(do_url, url),
                    gevent.spawn(do_redis, key, url)])


if __name__ == "__main__":
    urls = [('google', 'http://www.google.com'), 
            ('python', 'http://www.python.org')]

    gevent.joinall([gevent.spawn(do_jobs, url) for url in urls])

    print("n=%d" % n)

    unittest.main()
