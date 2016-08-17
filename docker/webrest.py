"""
http POST "http://localhost:8000/test/check?n=10&t=ivan%20rocha" Content-Type:application/json name=irr timeout=10

echo -n '{"name": "irr", "timeout": "10"}' > /tmp/post.json
ab -p /tmp/post.json -T application/json -n 1 -c 1 http://localhost:8000/test/check

tcpkali -em "GET /test HTTP/1.1\r\nHost: localhost\r\n\r\n" -r 10 --latency-marker "HTTP/1.1" localhost:8000
"""

import gevent
from gevent import monkey

monkey.patch_all()
from gevent.pywsgi import WSGIServer

import argparse
import json
import logging.handlers
import re

from cgi import escape
from urlparse import parse_qs

import requests
import requests.packages

requests.packages.urllib3.disable_warnings()

STATUS = '200 OK'
HEADERS = [('Content-Type', 'application/json; charset=utf-8')]

LOG_LEVEL = logging.DEBUG
LOG_FORMAT = '[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s'

logging.basicConfig(format=LOG_FORMAT)
logging.getLogger().setLevel(LOG_LEVEL)

def get_body(environ):
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except ValueError:
        return None

    return environ['wsgi.input'].read(request_body_size)

# Routes (BEGIN)

def test(environ):
    """
    test handler
    """
    return True, {'message': "OK!",
                  'url.args': environ['web.url_args'],
                  'url.qs': environ['web.qs'],
                  'body': get_body(environ)}

# Routes (END)

ROUTES = [
    (r'test/?$', test),
    (r'test/(.+)$', test)
]


def application(environ, start_response):
    """
    application handler
    """
    gev = None
    path = environ.get('PATH_INFO', '').lstrip('/')

    for regex, callback in ROUTES:
        match = re.search(regex, path)
        if match is not None:
            environ['web.url_args'] = match.groups()
            qs = parse_qs(environ['QUERY_STRING'])
            environ['web.qs'] = {k: [escape(v) for v in qs[k]] for k in qs}
            gev = gevent.spawn(callback, environ)
            gevent.joinall([gev])
            break

    if gev is None:
        start_response('404 NOT FOUND', HEADERS)
        yield ("%s\n" % json.dumps({"error": "Not Found"})).encode('utf-8')
        return

    if gev.value[0]:
        start_response(STATUS, HEADERS)
        yield ("%s\n" % json.dumps(gev.value[1])).encode('utf-8')
        return
    else:
        start_response(500, HEADERS)
        yield ("%s\n" % json.dumps({"error": gev.value[1]})).encode('utf-8')
        return


if __name__ == "__main__":

    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-b', '--bind',
                        dest="bind",
                        default="0.0.0.0",
                        help="bind address (default: 0.0.0.0)")
    PARSER.add_argument('-p', '--port',
                        dest="port",
                        type=int,
                        default=8000,
                        help="listen port (default: 8000)")
    ARGS = PARSER.parse_args()

    logging.info('Server started on %s:%d...' % (ARGS.bind, ARGS.port))
    WSGIServer((ARGS.bind, ARGS.port), application).serve_forever()
