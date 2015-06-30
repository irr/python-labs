from tornado import gen
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import parse_command_line
from tornado import web

import psycopg2
import momoko
import json

class BaseHandler(web.RequestHandler):
    @property
    def db(self):
        return self.application.db


class MyHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        try:
            f1 = self.db.execute('select 1;')
            f2 = self.db.execute('select 2;')
            f3 = self.db.execute('select 3;')
            yield [f1, f2, f3]

            cursor1 = f1.result()
            cursor2 = f2.result()
            cursor3 = f3.result()

        except (psycopg2.Warning, psycopg2.Error) as error:
            self.write(str(error))
        else:
            self.set_header('Content-Type', 'application/json; charset="utf-8"')
            results = { 'Q1': cursor1.fetchall(),
                        'Q3': cursor2.fetchall(),
                        'Q2': cursor3.fetchall() }
            self.write(json.dumps(results))

        self.finish()


if __name__ == '__main__':
    parse_command_line()
    application = web.Application([
        (r'/', MyHandler)
    ], debug=True)

    ioloop = IOLoop.instance()

    application.db = momoko.Pool(
        dsn='dbname=postgis user=postgres password=postgres host=localhost',
        size=1,
        ioloop=ioloop,
    )

    # this is a one way to run ioloop in sync
    future = application.db.connect()
    ioloop.add_future(future, lambda f: ioloop.stop())
    ioloop.start()

    http_server = HTTPServer(application)
    http_server.listen(8888, 'localhost')
    ioloop.start()
