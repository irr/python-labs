import time
from BaseHTTPServer   import BaseHTTPRequestHandler, HTTPServer, test as _test
from SocketServer     import ThreadingMixIn

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

class SlowHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

        self.wfile.write("Entered GET request handler")
        #time.sleep(3)
        self.wfile.write("\nSending response!")

def test(HandlerClass = SlowHandler,
         ServerClass = ThreadedHTTPServer):
    _test(HandlerClass, ServerClass)


if __name__ == '__main__':
    test()
