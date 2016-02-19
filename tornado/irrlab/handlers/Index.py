from tornado.web import RequestHandler
from tornado.template import Template
from tornado.escape import json_encode, json_decode

import tornado.web
import tornado.gen

import tornadoredis

import shlex, subprocess

import time

from utils import *

class AsyncProcessMixIn(RequestHandler):
    def call_subprocess(self, command, callback=None):
        self.ioloop = tornado.ioloop.IOLoop.instance()
        self.pipe = subprocess.Popen(shlex.split(command),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=True)

        self.fd = self.pipe.stdout.fileno()

        def recv(*args):
            data = self.pipe.stdout.readline()
            if data: callback(data)
            elif self.pipe.poll() is not None:
                self.ioloop.remove_handler(self.fd)
                callback(None)

        # read handler
        self.ioloop.add_handler(self.fd, recv, self.ioloop.READ)

    def on_subprocess_result(self, callback, fd, result):
        try:
            if callback:
                callback(self.pipe.stdout, self.pipe.stderr)
        except Exception as ex:
            logging.error(ex)
        finally:
            self.ioloop.remove_handler(fd)


class IndexHandler(RequestHandler):
    def initialize(self, **kwargs):
        self.logger = kwargs["logger"]
        self.redis = tornadoredis.Client(connection_pool=kwargs["redis"])
        self.cfg = kwargs["cfg"]
        self.template = Template("op -cmd {{ cmd }} -value {{ value }}")

    @staticmethod
    def _customize(self):
        self.set_header("Server", "IRR")
        self.set_header("Content-Type", "application/json; charset=UTF-8")

    @tornado.gen.coroutine
    def _redis(self):
        info = yield tornado.gen.Task(self.redis.info)
        yield tornado.gen.Task(self.redis.disconnect)
        raise tornado.gen.Return(info)

    @tornado.gen.coroutine
    def _handle(self, **kwargs):
        IndexHandler._customize(self)
        db = None
        try:
            info = yield tornado.gen.Task(self._redis)
            data = { 'cmd': "any", 'value': str(int(time.time())) }
            response = { 'status': 200,
                         'msg': self.template.generate(**data),
                         'redis': info['redis_version'],
                         'cfg': self.cfg }
        except Exception as ex:
            response = { 'status': 500, 'msg': str(ex) }
        finally:
            if db:
                db.close()
        if response['status'] != 200:
            self.set_status(response['status'])
        self.write(json_encode(response))
        self.finish()

    @tornado.web.asynchronous
    def get(self):
        self._handle()


class CmdHandler(AsyncProcessMixIn):
    @tornado.web.asynchronous
    def get(self):
        cmd = 'ls /'

        def send(data):
            if data:
                self.write(data)
                self.flush()
            else:
                self.finish()

        self.subprocess(cmd, send)

    def subprocess(self, cmd, callback):
        ioloop = tornado.ioloop.IOLoop.instance()
        pipe = subprocess.Popen(cmd, shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                close_fds=True)

        fd = pipe.stdout.fileno()

        def recv(*args):
            data = pipe.stdout.readline()
            if data: callback(data)
            elif pipe.poll() is not None:
                ioloop.remove_handler(fd)
                callback(None)

        # read handler
        ioloop.add_handler(fd, recv, ioloop.READ)
