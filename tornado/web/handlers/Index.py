from tornado.web import RequestHandler
from tornado.template import Template
from tornado.escape import json_encode, json_decode

import tornado.web
import tornado.gen
import tornadoredis
import torndb

import time

from utils import *

class IndexHandler(RequestHandler):
    def initialize(self, **kwargs):
        self.logger = kwargs.get("logger")
        self.redis = tornadoredis.Client(connection_pool=kwargs["redis"])
        self.mysql = torndb.Connection("localhost", "mysql")
        self.template = Template("op -cmd {{ cmd }} -value {{ value }}")

    def _customize(self):
        self.set_header("Server", "IRR")
        self.set_header("Content-Type", "application/json; charset=UTF-8")

    @tornado.web.asynchronous
    @tornado.gen.engine
    def _redis(self):
        info = yield tornado.gen.Task(self.redis.info)
        yield tornado.gen.Task(self.redis.disconnect)
        return info

    def _handle(self, **kwargs):
        self._customize()
        try:            
            data = { 'cmd': "any", 'value': str(time.time()) }
            response = { 'status': 200,
                         'msg': self.template.generate(**data),
                         'redis': _redis['redis_version'] }
        except Exception as ex:
            response = { 'status': 500, 'msg': str(ex) }
        if response['status'] != 200:
            self.set_status(response['status'])            
        self.write(json_encode(response))
        self.finish()

    def get(self):
        self._handle()
