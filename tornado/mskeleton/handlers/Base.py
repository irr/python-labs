import logging, time

import tornado.web
from tornado.template import Loader

import asyncmongo

import json    
from bson import json_util

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

class OverviewHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render('index.html')

class DynamicOverviewHandler(tornado.web.RequestHandler):
    def initialize(self, **kwargs):
        kwargs.update(dict(time=time.asctime()))
        self.loader = Loader(kwargs.get("template_path"))
        self.kwargs = kwargs

    @tornado.web.asynchronous
    def get(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(self.loader.load("index-json.js").generate(**self.kwargs))
        self.finish()

class MongoHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        self.db.symbols.find({'S': "UOLL4"}, limit = 2, callback = self._on_response)

    def _on_response(self, response, error):
        if error:
            raise tornado.web.HTTPError(500)
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        # mongo_object = json.loads(js, object_hook=json_util.object_hook)
        self.write(json.dumps(response, default=json_util.default))
        self.finish()