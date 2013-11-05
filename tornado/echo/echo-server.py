#!/usr/bin/env python
#coding:utf-8

import sys, os, re
import logging

from tornado.ioloop import IOLoop
from tornado.iostream import IOStream
from tornado.netutil import TCPServer

logging.basicConfig(level=logging.INFO, format='%(levelname)s - - %(asctime)s %(message)s', datefmt='[%d/%b/%Y %H:%M:%S]')

class EchoServer(TCPServer):

    def __init__(self, io_loop=None, ssl_options=None, **kwargs):
        logging.info('a echo tcp server is started')
        TCPServer.__init__(self, io_loop=io_loop, ssl_options=ssl_options, **kwargs)

    def handle_stream(self, stream, address):
        EchoConnection(stream, address)

class EchoConnection(object):

    stream_set = set([])

    def __init__(self, stream, address):
        logging.info('receive a new connection from %s', address)
        self.stream = stream
        self.address = address
        self.stream_set.add(self.stream)
        self.stream.set_close_callback(self._on_close)
        self.stream.read_until('\n', self._on_read_line)

    def _on_read_line(self, data):
        logging.info('read a new line from %s', self.address)
        for stream in self.stream_set:
            stream.write(data, self._on_write_complete)

    def _on_write_complete(self):
        logging.info('write a line to %s', self.address)
        if not self.stream.reading():
            self.stream.read_until('\n', self._on_read_line)

    def _on_close(self):
        logging.info('client quit %s', self.address)
        self.stream_set.remove(self.stream)

def main():
    echo_server = EchoServer()
    echo_server.listen(8888)
    IOLoop.instance().start()

if __name__ == '__main__':
    main()
