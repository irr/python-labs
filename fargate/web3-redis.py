import gevent
from gevent import monkey
monkey.patch_all()

from gevent.lock import BoundedSemaphore
from gevent.pywsgi import WSGIServer
from cgi import parse_qs, escape

import redis, json, sys, logging.handlers, uuid, datetime

SEM = BoundedSemaphore(10)

POOL = redis.ConnectionPool(host='c1.irrlab.cc', port=6379, password='irrlabpasswd',
                            db=0, max_connections=10)

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

        data = parse_qs(environ['QUERY_STRING'])
        time = int(escape(data.get('t', ['0'])[0]))

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



if __name__ == "__main__":
    bind, port = '0.0.0.0', 8080
    print('Listening on %s:%d...' % (bind, port))
    WSGIServer((bind, port), application).serve_forever()
