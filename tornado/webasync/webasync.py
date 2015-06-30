import tornado.web
import tornado.ioloop
import tornado.httpclient
import json

class MyHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        def __callback(response):
            data = { 'body': response.body[:20] + '...', 'length' : len(response.body) }
            self.set_header('Content-Type', 'application/json; charset="utf-8"')
            self.write(json.dumps(data))
            self.finish()

        async_client = tornado.httpclient.AsyncHTTPClient()
        request = tornado.httpclient.HTTPRequest("http://www.uol.com.br/")
        async_client.fetch(request, __callback) 

application = tornado.web.Application([
    (r"/", MyHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
