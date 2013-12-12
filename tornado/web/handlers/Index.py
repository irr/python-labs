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
        self.mysql = kwargs.get("mysql")
        self.redis = tornadoredis.Client(connection_pool=kwargs["redis"])
        self.template = Template("op -cmd {{ cmd }} -value {{ value }}")

    def _customize(self):
        self.set_header("Server", "IRR")
        self.set_header("Content-Type", "application/json; charset=UTF-8")

    @tornado.web.asynchronous
    @tornado.gen.engine
    def _handle(self, **kwargs):
        self._customize()
        db = None
        try:   
            db = torndb.Connection(self.mysql['host'], self.mysql['database'], 
                user=self.mysql['user'], password=self.mysql['password'])
            hosts = [host for host in db.query("SELECT Host FROM user WHERE User = 'root'")]
            info = yield tornado.gen.Task(self.redis.info)
            yield tornado.gen.Task(self.redis.disconnect)
            data = { 'cmd': "any", 'value': str(time.time()) }
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

    def get(self):
        self._handle()
