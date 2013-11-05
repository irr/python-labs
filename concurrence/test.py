from __future__ import with_statement

import time

# hack to work with StaticPython
# sudo yum install python-redis
# sudo yum install python-routes
# sudo yum install python-webob

import sys
sys.path.append("/usr/lib/python2.7/site-packages")

import redis

from concurrence import unittest, Tasklet

from concurrence.database.mysql import client, dbapi
from concurrence.memcache.client import MemcacheNode

from concurrence.web import Application, Controller, web
from concurrence.web.filter import JSONFilter
from concurrence.http.client import HTTPConnection

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWD = 'mysql'
DB_DB = 'test'

# Database setup
# CREATE TABLE `test`.`test` (
#   `id` INTEGER UNSIGNED NOT NULL,
#   `name` VARCHAR(255)  CHARACTER SET latin1 COLLATE latin1_bin NOT NULL,
#   PRIMARY KEY (`id`)
# )
# ENGINE = InnoDB
# CHARACTER SET latin1 COLLATE latin1_bin;

class TestMySQL(unittest.TestCase):

    def testMySQLClient(self):
        cnn = client.connect(host=DB_HOST, user=DB_USER,
                             passwd=DB_PASSWD, db=DB_DB)

        rs = cnn.query("select 1")

        self.assertEqual([('1',)], list(rs))

        rs.close()
        cnn.close()

    def testMySQLClient2(self):
        cnn = client.connect(host=DB_HOST, user=DB_USER,
                             passwd=DB_PASSWD, db=DB_DB)

        cnn.query("truncate test")

        for i in range(10):
            self.assertEquals((1, 0), cnn.query("insert into test (id, name) values (%d, 'test%d')" % (i, i)))

        rs = cnn.query("select id, name from test")

        #trying to close it now would give an error, e.g. we always need to read
        #the result from the database otherwise connection would be in wrong stat
        try:
            rs.close()
            self.fail('expected exception')
        except client.ClientProgrammingError:
            pass

        for i, row in enumerate(rs):
            self.assertEquals((i, 'test%d' % i), row)

        rs.close()
        cnn.close()

    def testParallelQuery(self):

        def query(s):
            cnn = dbapi.connect(host=DB_HOST, user=DB_USER,
                                passwd=DB_PASSWD, db=DB_DB)
            cur = cnn.cursor()
            cur.execute("select sleep(%d)" % s)
            cur.close()
            cnn.close()

        start = time.time()
        ch1 = Tasklet.new(query)(1)
        ch2 = Tasklet.new(query)(2)
        ch3 = Tasklet.new(query)(3)
        Tasklet.join_all([ch1, ch2, ch3])

        end = time.time()
        self.assertAlmostEqual(3.0, end - start, places=1)

    def testMySQLDBAPI(self):

        cnn = dbapi.connect(host=DB_HOST, user=DB_USER,
                            passwd=DB_PASSWD, db=DB_DB)

        cur = cnn.cursor()

        cur.execute("truncate test")

        for i in range(10):
            cur.execute("insert into test (id, name) values (%d, 'test%d')" % (i, i))

        cur.close()

        cur = cnn.cursor()

        cur.execute("select id, name from test")

        self.assertEquals((0, 'test0'), cur.fetchone())

        #check that fetchall gets the remainder
        self.assertEquals([(1, 'test1'), (2, 'test2'), (3, 'test3'), (4, 'test4'), (5, 'test5'), (6, 'test6'), (7, 'test7'), (8, 'test8'), (9, 'test9')], cur.fetchall())

        #another query on the same cursor should work
        cur.execute("select id, name from test")

        #fetch some but not all
        self.assertEquals((0, 'test0'), cur.fetchone())
        self.assertEquals((1, 'test1'), cur.fetchone())
        self.assertEquals((2, 'test2'), cur.fetchone())

        #close whould work even with half read resultset
        cur.close()

        #this should not work, cursor was closed
        try:
            cur.execute("select * from test")
            self.fail("expected exception")
        except dbapi.ProgrammingError:
            pass

    def testMemcacheBasic(self):

        node = MemcacheNode()
        node.connect(('127.0.0.1', 11211))

        node.set('test1', '12345')
        node.set('test2', '67890')

        self.assertEquals('12345', node.get('test1'))
        self.assertEquals(None, node.get('test3'))
        self.assertEquals({'test1': '12345', 'test2': '67890'}, node.get(['test1', 'test2', 'test3']))

        #update test2
        node.set('test2', 'hello world!')

        self.assertEquals({'test1': '12345', 'test2': 'hello world!'}, node.get(['test1', 'test2', 'test3']))

        #update to unicode type
        node.set('test2', u'C\xe9line')
        self.assertEquals(u'C\xe9line', node.get('test2'))

        #update to some other type
        node.set('test2', {'piet': 'blaat', 10: 20})
        self.assertEquals({'piet': 'blaat', 10: 20}, node.get('test2'))

        node.close()


class TestController(Controller):

    @web.route('/hello')
    def hello(self):
        return "Hello World!"

    @web.route('/json')
    @web.filter(JSONFilter())
    def json(self):
        return "[1,2,3,4]"


class TestWeb(unittest.TestCase):

    def setUp(self):

        application = Application()
        application.add_controller(TestController())
        application.configure()
        self.server = application.serve(('localhost', 8080))

    def tearDown(self):

        self.server.close()

    def testWeb(self):

        cnn = None
        try:           
            cnn = HTTPConnection()
            cnn.connect(('localhost', 8080))
            response = cnn.perform(cnn.get('/hello'))
            status = response.status
            self.assertEquals('HTTP/1.1 200 OK', status)    
            self.assertEquals('text/html; charset=UTF-8', response.get_header('Content-Type'))
            self.assertEquals('12', response.get_header('Content-Length'))
            self.assertEquals("Hello World!", ''.join(response).decode('UTF-8'))
        finally:
            if cnn: cnn.close()

    def testWebJSON(self):

        cnn = None
        try:           
            cnn = HTTPConnection()
            cnn.connect(('localhost', 8080))
            response = cnn.perform(cnn.get('/json'))
            status = response.status
            self.assertEquals('HTTP/1.1 200 OK', status)    
            self.assertEquals('application/json; charset=UTF-8', response.get_header('Content-Type'))
            self.assertEquals('9', response.get_header('Content-Length'))
            self.assertEquals("[1,2,3,4]", response.body)
        finally:
            if cnn: cnn.close()

class TestRedis(unittest.TestCase):

    def testRedis(self):

        r = None
        try:           
            r = redis.Redis(host='localhost', port=6379, db=0)
            r.set('foo', 'bar')
            val = r.get('foo')
            self.assertEquals('bar', val)    
        finally:
            if r: r.flushall()

if __name__ == '__main__':
    unittest.main(timeout=60)



