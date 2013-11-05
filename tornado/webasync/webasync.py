import tornado.web
import tornado.ioloop
import tornado.httpclient

class MyHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        def __callback(response):
            self.write(response.body)
            self.finish()

        async_client = tornado.httpclient.AsyncHTTPClient()
        request = tornado.httpclient.HTTPRequest("http://localhost:8085/")
        async_client.fetch(request, __callback) 

application = tornado.web.Application([
    (r"/", MyHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
