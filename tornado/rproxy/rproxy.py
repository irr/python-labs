import sys, os, re, time
import logging
import socket

from tornado.ioloop import IOLoop
from tornado.iostream import IOStream
from tornado.netutil import TCPServer
from tornado.process import cpu_count

logging.basicConfig(level=logging.INFO, format='%(levelname)s - - %(asctime)s %(message)s', datefmt='[%d/%b/%Y %H:%M:%S]')

class ForwardConnection(object):

    def __init__(self, remote_address, stream, address, headers):
        self.remote_address = remote_address
        self.stream = stream
        self.address = address
        self.headers = headers
        sock = socket.socket()
        self.remote_stream = IOStream(sock)
        self.remote_stream.connect(self.remote_address, self._on_remote_connected)    
        self.remote_stream.set_close_callback(self._on_close)    

    def _on_remote_write_complete(self):
        logging.info('send request to %s', self.remote_address)
        self.remote_stream.read_until_close(self._on_remote_read_close)

    def _on_remote_connected(self):
        logging.info('forward %r to %r', self.address, self.remote_address)
        self.remote_stream.write(self.headers, self._on_remote_write_complete)

    def _on_remote_read_close(self, data):
        self.stream.write(data, self.stream.close)

    def _on_close(self):
        logging.info('remote quit %s', self.remote_address)
        self.remote_stream.close()

class ReverseProxyServer(TCPServer):

    def __init__(self, io_loop=None, ssl_options=None, **kwargs):
        logging.info('a reverse-proxy is started')
        TCPServer.__init__(self, io_loop=io_loop, ssl_options=ssl_options, **kwargs)

    def handle_stream(self, stream, address):
        ReverseProxyConnection(stream, address)


class ReverseProxyConnection(object):

    stream_set = set([])

    def __init__(self, stream, address):
        logging.info('receive a new connection from %s', address)
        self.stream = stream
        self.address = address
        self.stream_set.add(self.stream)
        self.stream.set_close_callback(self._on_close)
        self.stream.read_until('\r\n\r\n', self._on_headers)

    def _on_headers(self, data):
        logging.info('read headers from %s [%s]', self.address, data.splitlines())
        ForwardConnection(("www.uol.com.br", 80), self.stream, self.address, data)

    def _on_close(self):
        logging.info('client quit %s', self.address)
        self.stream_set.remove(self.stream)
        self.stream.close()

def main():
    reverse_proxy_server = ReverseProxyServer()
    reverse_proxy_server.bind(7777)
    reverse_proxy_server.start(cpu_count())
    IOLoop.instance().start()

if __name__ == '__main__':
    main()        

# [irocha@irrlab tornado-server (master)]$ http localhost:7777 
# HTTP/1.1 302 Found
# Connection: close
# Content-Length: 206
# Content-Type: text/html; charset=iso-8859-1
# Date: Tue, 04 Sep 2012 11:14:28 GMT
# Location: http://www.uol.com.br/
# Server: Apache/2.0.63 (Unix) Ganesh/2.2.0

# <!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
# <html><head>
# <title>302 Found</title>
# </head><body>
# <h1>Found</h1>
# <p>The document has moved <a href="http://www.uol.com.br/">here</a>.</p>
# </body></html>
