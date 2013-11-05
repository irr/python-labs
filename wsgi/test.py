from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server
from cgi import parse_qs, escape

import json

# http GET "http://localhost:8888/map?u=ivan+rocha"

def simple_app(environ, start_response):
    status = '404 NOT FOUND'
    headers = [('Content-type', 'application/json; charset=UTF8')]
    body = '{}'

    parameters = parse_qs(environ.get('QUERY_STRING', ''))

    if 'u' in parameters: 
        status = '200 OK'
        user = escape(parameters['u'][0])
        body = json.dumps({"user":user,"key":"testing","server":"ss2","mode":"RW"})
        
    start_response(status, headers)
        
    return [body]

httpd = make_server('', 8888, simple_app)
print "Serving on port 8888..."
httpd.serve_forever()
