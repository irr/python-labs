from time import sleep
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, asynchronous, RequestHandler
from multiprocessing.pool import ThreadPool

_workers = ThreadPool(10)

def run_background(func, callback, args=(), kwds={}):
    def _callback(result):
        IOLoop.instance().add_callback(lambda: callback(result))
    _workers.apply_async(func, args, kwds, _callback)

# blocking task like querying to MySQL
# http GET localhost:8888/?t=1
def blocking_task(n):
    sleep(n)
    return n

class Handler(RequestHandler):
    @asynchronous
    def get(self):
        t = int(self.get_argument("t", "1"))        
        run_background(blocking_task, self.on_complete, (t,))

    def on_complete(self, res):
        self.write("Test {0}<br/>".format(res))
        self.finish()

HTTPServer(Application([("/", Handler)],debug=True)).listen(8888)
IOLoop.instance().start()
