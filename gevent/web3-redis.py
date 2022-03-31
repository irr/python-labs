#!/usr/bin/env python
"""
Basic template for gevent web server
"""

import gevent
from gevent import monkey
monkey.patch_all()

from gevent.lock import BoundedSemaphore
from gevent.pywsgi import WSGIServer
from urllib.parse import parse_qs
from http.cookies import SimpleCookie

import argparse, redis, json, logging.handlers, signal, sys, uuid, datetime

SEM = BoundedSemaphore(100)

LOG_LEVEL = logging.DEBUG
LOG_FORMAT = ('%(levelname)s %(asctime)s %(name)s:%(funcName)s:%(lineno)d %(message)s')
LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

POOL = redis.ConnectionPool(host='localhost', port=6379,
                            db=0, max_connections=100)


def redis_exec():
    """
    retrieve redis info array
    """
    connection = redis.Redis(connection_pool=POOL)
    return connection.info()


def application(environ, start_response):
    with SEM:
        """
        application handler
        """
        status = '200 OK'
        headers = [('Content-Type', 'application/json; charset=utf-8')]

        if 'HTTP_COOKIE' not in environ:
            ck = SimpleCookie()
            ck['session'] = str(uuid.uuid4())
            ck['session']['domain'] = '' # localhost
            ck['session']['path'] = '/'
            expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
            ck['session']['expires'] = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")
            ck['session']['httponly'] = True
            LOGGER.info('cookie generated [{0}]={1}'.format(json.dumps(ck), ck['session'].value))
            headers.append(('Set-Cookie', ck['session'].OutputString()))
        else:
            ck = SimpleCookie(environ['HTTP_COOKIE'])
            LOGGER.info('cookie received: [{0}]={1}'.format(json.dumps(ck), ck['session'].value))

        data = parse_qs(environ['QUERY_STRING'])
        time = int((data.get('t', ['0'])[0]))

        if time > 0:
            gevent.sleep(int(time))

        gev1 = gevent.spawn(redis_exec)

        gevent.joinall([gev1])

        if gev1.value == None:
            start_response("503", headers)
            yield ("%s\n" % json.dumps(
                {"error": "Sorry, service unavailable."})[:1024]).encode('utf-8')
        else:
            start_response(status, headers)
            yield ("%s\n" % json.dumps({"redis": gev1.value["redis_version"],
                                        "t":time})[:1024]).encode('utf-8')


def graceful_shutdown(gexc=None):
    if gexc:
        LOGGER.info('%s Exiting and closing connections...' % (gexc.__class__,))
    sys.exit(0)


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
    PARSER.add_argument('-i', '--instances',
                        dest="instances",
                        type=int,
                        default=0,
                        help="instances number (supervisor only, default:<cpu-count>)")

    ARGS = PARSER.parse_args()
    logging.info('Listening on %s:%d...' % (ARGS.bind, ARGS.port))

    try:
        WSGIServer((ARGS.bind, ARGS.port), application).serve_forever()
    except (KeyboardInterrupt, SystemExit) as err:
        graceful_shutdown(err)

