import monocle
from monocle import _o, Return
monocle.init("tornado")

from monocle.stack import eventloop
from monocle.stack.network import add_service
from monocle.stack.network.http import HttpHeaders, HttpServer

@_o
def hello_http(req):
    content = "Hello, World!"
    headers = HttpHeaders()
    headers['Content-Length'] = len(content)
    headers['Content-Type'] = 'text/plain'
    yield Return(200, headers, content)

add_service(HttpServer(hello_http, 8088))
eventloop.run()
