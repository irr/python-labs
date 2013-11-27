import tornadoredis
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.gen

import json

from torndb import Connection

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        self.c = tornadoredis.Client()        
        self.c.connect()
        self.db = Connection('127.0.0.1:3306', 'mysql', user='root', password='mysql')
        handlers = [(r"/", IndexHandler)]
        tornado.web.Application.__init__(self, handlers, debug=True)

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):      
        o = yield tornado.gen.Task(self.application.c.get, self.get_argument('k'))
        h = self.application.db.get("SELECT * FROM user LIMIT 1")
        if o == None:
            self.set_status(404)
        else:
            self.write(o)
            self.write("\n")
            self.write(json.dumps(h))
        self.finish()

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self): 
        yield tornado.gen.Task(self.application.c.set, 
            self.get_argument('k'), self.get_argument('v'))
        self.finish()

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
