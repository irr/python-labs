import time
from BaseHTTPServer   import BaseHTTPRequestHandler, HTTPServer, test as _test
from SocketServer     import ThreadingMixIn

from concurrent.futures import ThreadPoolExecutor # pip install futures

class PoolMixIn(ThreadingMixIn):
    def process_request(self, request, client_address):
        self.pool.submit(self.process_request_thread, request, client_address)

class PoolHTTPServer(PoolMixIn, HTTPServer):
    pool = ThreadPoolExecutor(max_workers=40)

class SlowHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

        self.wfile.write("Entered GET request handler")
        time.sleep(3)
        self.wfile.write("\nSending response!")

def test(HandlerClass = SlowHandler,
         ServerClass = PoolHTTPServer):
    _test(HandlerClass, ServerClass)

if __name__ == '__main__':
    test()
