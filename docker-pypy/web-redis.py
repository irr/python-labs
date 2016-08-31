import gevent
from gevent import monkey
monkey.patch_all()

from gevent.lock import BoundedSemaphore
from gevent.pywsgi import WSGIServer
from cgi import parse_qs, escape
from Cookie import SimpleCookie

import argparse, redis, json, logging.handlers, signal, sys, uuid, datetime

SEM = BoundedSemaphore(1)

LOG_LEVEL = logging.DEBUG
LOG_FORMAT = '[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s'

logging.basicConfig(format=LOG_FORMAT)
logging.getLogger().setLevel(LOG_LEVEL)

POOL = redis.ConnectionPool(host='localhost', port=6379,
                            db=0, max_connections=100)


def redis_exec():
    """
    retrieve redis info array
    """
    connection = redis.Redis(connection_pool=POOL)
    return connection.info()


def application(environ, start_response):
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
        logging.getLogger().info('cookie generated: [{0}]={1}'.format(json.dumps(ck), ck['session'].value))
        headers.append(('Set-Cookie', ck['session'].OutputString()))
    else:
        ck = SimpleCookie(environ['HTTP_COOKIE'])
        logging.getLogger().info('cookie received: [{0}]={1}'.format(json.dumps(ck), ck['session'].value))

    data = parse_qs(environ['QUERY_STRING'])
    time = int(escape(data.get('t', ['0'])[0]))

    with SEM:
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
        logging.getLogger().info('%s Exiting and closing connections...' % (gexc.__class__,))
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
                        default=8080,
                        help="listen port (default: 8080)")
    PARSER.add_argument('-i', '--instances',
                        dest="instances",
                        type=int,
                        default=0,
                        help="instances number (supervisor only, default:<cpu-count>)")

    ARGS = PARSER.parse_args()
    logging.info('Listening on %s:%d...' % (ARGS.bind, ARGS.port))

    gevent.signal(signal.SIGTERM, graceful_shutdown)

    try:
        WSGIServer((ARGS.bind, ARGS.port), application).serve_forever()
    except (KeyboardInterrupt, SystemExit) as err:
        graceful_shutdown(err)

