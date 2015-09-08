#!/usr/bin/env python
"""
Basic template for gevent web server
"""

import gevent
from gevent import monkey
monkey.patch_all()

from gevent.pywsgi import WSGIServer
from cgi import parse_qs, escape

import argparse, pymysql, redis, json, logging.handlers, signal, sys

LOG_LEVEL = logging.DEBUG
LOG_FORMAT = '[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s'

SYSLOG = logging.handlers.SysLogHandler(address='/dev/log')
SYSLOG.setFormatter(logging.Formatter(LOG_FORMAT))

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


def mysql_exec():
    """
    retrieve mysql hosts
    """
    dbase = pymysql.connect(host='127.0.0.1', port=3306,
                            user='root', passwd='mysql', db='mysql')
    result = dbase.cursor()
    result.execute("SELECT Host FROM user WHERE User = 'root' LIMIT 1")
    res = []
    for host in result:
        res.append(host[0])
    result.close()
    dbase.close()
    return res


def application(environ, start_response):
    """
    application handler
    """
    status = '200 OK'
    headers = [('Content-Type', 'application/json; charset=utf-8')]

    data = parse_qs(environ['QUERY_STRING'])
    time = int(escape(data.get('t', ['0'])[0]))

    if time > 0:
        gevent.sleep(int(time))

    gev1 = gevent.spawn(redis_exec)
    gev2 = gevent.spawn(mysql_exec)

    gevent.joinall([gev1, gev2])

    if gev1.value == None or gev2.value == None:
        start_response("503", headers)
        yield ("%s\n" % json.dumps(
            {"error": "Sorry, service unavailable."})[:1024]).encode('utf-8')
    else:
        start_response(status, headers)
        yield ("%s\n" % json.dumps({"redis": gev1.value["redis_version"],
                                    "mysql":gev2.value, "t":time})[:1024]).encode('utf-8')


def graceful_shutdown(gexc=None):
    if gexc:
        logging.getLogger().info('%s Exiting and closing connections...' % (gexc.__class__,))
    sys.exit(0)


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-s', '--syslog',
                        dest="syslog",
                        action='store_true',
                        help="enable syslog (default: disabled)")
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
    if ARGS.syslog:
        logging.getLogger().addHandler(SYSLOG)
    logging.info('Listening on %s:%d...' % (ARGS.bind, ARGS.port))

    gevent.signal(signal.SIGTERM, graceful_shutdown)

    try:
        WSGIServer((ARGS.bind, ARGS.port), application).serve_forever()
    except (KeyboardInterrupt, SystemExit) as err:
        graceful_shutdown(err)

