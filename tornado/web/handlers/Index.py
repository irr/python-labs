from tornado.web import RequestHandler
from tornado.template import Template
from tornado.escape import json_encode, json_decode

import tornado.web
import tornado.gen

import tornadoredis
import torndb

import shlex, subprocess

import time

from utils import *

class AsyncProcessMixIn(RequestHandler):
    def call_subprocess(self, command, callback=None):
        self.ioloop = tornado.ioloop.IOLoop.instance()
        self.pipe = p = subprocess.Popen(shlex.split(command), 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            close_fds=True)
        self.ioloop.add_handler(p.stdout.fileno(), 
            self.async_callback(self.on_subprocess_result, callback), 
            self.ioloop.READ)

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
        self.logger = kwargs.get("logger")
        self.mysql = kwargs.get("mysql")
        self.redis = tornadoredis.Client(connection_pool=kwargs["redis"])
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
            db = torndb.Connection(self.mysql['host'], self.mysql['database'], 
                                   user=self.mysql['user'], password=self.mysql['password'])
            hosts = [host for host in db.query("SELECT Host FROM user WHERE User = 'root'")]
            info = yield tornado.gen.Task(self._redis)
            data = { 'cmd': "any", 'value': str(int(time.time())) }
            response = { 'status': 200,
                         'msg': self.template.generate(**data),
                         'redis': info['redis_version'],
                         'mysql': hosts }
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
        self.call_subprocess('ls /', self.on_ls)
    
    def on_ls(self, out, err):
        IndexHandler._customize(self)
        response = { 'stdout': out.read(), 'stderr': err.read() }
        self.write(json_encode(response))
        self.finish()
