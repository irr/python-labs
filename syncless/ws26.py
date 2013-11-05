import cgi
import BaseHTTPServer

import sys
sys.path.append("/usr/lib/python2.7/site-packages")

import redis
_r = redis.Redis(host='localhost', port=6379, db=0)

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        path = cgi.escape(self.path)

        n = _r.incr(path)

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        self.wfile.write('<html><head><title>Stackless WSGI</title></head>')
        self.wfile.write('<body><p>You accessed path: %s</p>\n' % path)

        if self.command in ('POST', 'PUT'):
            data = cgi.escape(repr(self.rfile.read(int(self.headers['Content-Length']))))
            self.wfile.write('<p>You submitted: %s</p>\n' % data)

        self.wfile.write('<form method=post><input name=q><input type=submit></form></body></html>\n')

    do_POST = do_GET
    do_PUT = do_GET

def start(host = "localhost", port = 8080):
    import logging
    import sys
    from syncless import wsgi
    if len(sys.argv) > 1:
        logging.root.setLevel(logging.DEBUG)
    else:
        logging.root.setLevel(logging.INFO)
    wsgi.RunHttpServer(MyHandler, ('localhost', 8080))

if __name__ == '__main__':
    start()
