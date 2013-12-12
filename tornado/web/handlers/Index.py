import time

try:
    from tornado.web import RequestHandler
    from tornado.template import Template, ParseError
    from tornado.escape import json_encode, json_decode
except ImportError as ierror:
    import sys
    sys.exit('Tornado required: http://www.tornadoweb.org/')

from utils import *

class IndexHandler(RequestHandler):
    def initialize(self, **kwargs):
        self.logger = kwargs.get("logger")
        self.template = Template("op -cmd {{ cmd }} -value {{ value }}")

    def _customize(self):
        self.set_header("Server", "IRR")
        self.set_header("Content-Type", "application/json; charset=UTF-8")

    def _handle(self, **kwargs):
        self._customize()
        try:            
            kwargs['value'] = str(time.time())
            data = { 'cmd': "any", 'value': kwargs.get("value") }
            response = { 'status': 200,
                         'msg': self.template.generate(**data) }
        except Exception as ex:
            response = { 'status': 500, 'msg': str(ex) }
        self.write(json_encode(response))

    # curl -v http://localhost:8888/;echo
    def get(self):
        self._handle()
