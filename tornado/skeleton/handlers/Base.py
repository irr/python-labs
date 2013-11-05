import logging, time
import tornado.web

from tornado import gen
from tornado.template import Loader

class BaseHandler(tornado.web.RequestHandler):
    # http://docs.python.org/2/library/functions.html#property
    @property
    def db(self):
        return self.application.db


class OverviewHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render('index.html')

class DynamicOverviewHandler(tornado.web.RequestHandler):
    def initialize(self, **kwargs):
        kwargs.update(dict(time=time.asctime()))
        self.loader = Loader(kwargs.get("template_path"))
        self.kwargs = kwargs

    @tornado.web.asynchronous
    def get(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(self.loader.load("index-json.js").generate(**self.kwargs))
        self.finish()


class SingleQueryHandler(BaseHandler):
    @tornado.web.asynchronous
    @gen.engine
    def get(self):
        # One simple query
        cursor = yield gen.Task(self.db.execute, 'SELECT 42, 12, %s, 11;', (25,))
        self.write('Query results: %s' % cursor.fetchall())
        self.finish()


class BatchQueryHandler(BaseHandler):
    @tornado.web.asynchronous
    @gen.engine
    def get(self):
        # These queries are executed all at once and therefore they need to be
        # stored in an dictionary so you know where the resulting cursors
        # come from, because they won't arrive in the same order.
        cursors = yield gen.Task(self.db.batch, {
            'query1': ['SELECT 42, 12, %s, %s;', (23, 56)],
            'query2': 'SELECT 1, 2, 3, 4, 5;',
            'query3': 'SELECT 465767, 4567, 3454;'
        })

        for key, cursor in cursors.items():
            self.write('Query results: %s = %s<br>' % (key, cursor.fetchall()))
        self.finish()


class QueryChainHandler(BaseHandler):
    @tornado.web.asynchronous
    @gen.engine
    def get(self):
        # Execute a list of queries in the order you specified
        cursors = yield gen.Task(self.db.chain, (
            ['SELECT 42, 12, %s, 11;', (23,)],
            'SELECT 1, 2, 3, 4, 5;'
        ))

        for cursor in cursors:
            self.write('Query results: %s<br>' % cursor.fetchall())
        self.finish()


class MultiQueryHandler(BaseHandler):
    @tornado.web.asynchronous
    @gen.engine
    def get(self):
        cursor1, cursor2, cursor3 = yield [
            gen.Task(self.db.execute, 'SELECT 42, 12, %s, 11;', (25,)),
            gen.Task(self.db.execute, 'SELECT 42, 12, %s, %s;', (23, 56)),
            gen.Task(self.db.execute, 'SELECT 465767, 4567, 3454;')
        ]

        self.write('Query 1 results: %s<br>' % cursor1.fetchall())
        self.write('Query 2 results: %s<br>' % cursor2.fetchall())
        self.write('Query 3 results: %s' % cursor3.fetchall())

        self.finish()


class CallbackWaitHandler(BaseHandler):
    @tornado.web.asynchronous
    @gen.engine
    def get(self):

        self.db.execute('SELECT 42, 12, %s, 11;', (25,),
            callback=(yield gen.Callback('q1')))
        self.db.execute('SELECT 42, 12, %s, %s;', (23, 56),
            callback=(yield gen.Callback('q2')))
        self.db.execute('SELECT 465767, 4567, 3454;',
            callback=(yield gen.Callback('q3')))

        cursor1 = yield gen.Wait('q1')
        cursor2 = yield gen.Wait('q2')
        cursor3 = yield gen.Wait('q3')

        self.write('Query 1 results: %s<br>' % cursor1.fetchall())
        self.write('Query 2 results: %s<br>' % cursor2.fetchall())
        self.write('Query 3 results: %s' % cursor3.fetchall())

        self.finish()
