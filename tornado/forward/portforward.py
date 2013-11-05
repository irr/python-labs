#!/usr/bin/env python
# coding:utf-8

import sys, os, re, time
import logging
import socket

from tornado.ioloop import IOLoop
from tornado.iostream import IOStream
from tornado.netutil import TCPServer

logging.basicConfig(level=logging.INFO, format='%(levelname)s - - %(asctime)s %(message)s', datefmt='[%d/%b/%Y %H:%M:%S]')

class ForwardServer(TCPServer):

    def __init__(self, remote_address, io_loop=None, ssl_options=None, **kwargs):
        TCPServer.__init__(self, io_loop, ssl_options, **kwargs)
        self.remote_address = remote_address

    def handle_stream(self, stream, address):
        ForwardConnection(self.remote_address, stream, address)

class ForwardConnection(object):

    def __init__(self, remote_address, stream, address):
        self.remote_address = remote_address
        self.stream = stream
        self.address = address
        sock = socket.socket()
        self.remote_stream = IOStream(sock)
        self.remote_stream.connect(self.remote_address, self._on_remote_connected)

    def _on_remote_connected(self):
        logging.info('forward %r to %r', self.address, self.remote_address)
        self.remote_stream.read_until_close(self._on_remote_read_close, self.stream.write)
        self.stream.read_until_close(self._on_read_close, self.remote_stream.write)

    def _on_remote_read_close(self, data):
        if self.stream.writing():
            self.stream.write(data, self.stream.close)
        else:
            self.stream.close()

    def _on_read_close(self, data):
        if self.remote_stream.writing():
            self.remote_stream.write(data, self.remote_stream.close)
        else:
            self.remote_stream.close()

def main():
    server = ForwardServer(('127.0.0.1', 8888))
    server.listen(7777)
    IOLoop.instance().start()

if __name__ == '__main__':
    main()
