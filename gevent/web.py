import gevent
from gevent import monkey
from gevent.pywsgi import WSGIServer

import umysql, json, logging, logging.handlers

import redis
redis.connection.socket = gevent.socket

LOG_LEVEL = logging.DEBUG
LOG_FORMAT = '[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s'
SYSLOG = logging.handlers.SysLogHandler(address='/dev/log')
SYSLOG.setFormatter(logging.Formatter(LOG_FORMAT))

logging.basicConfig(format=LOG_FORMAT)
#logging.getLogger().addHandler(SYSLOG)
logging.getLogger().setLevel(LOG_LEVEL)

r = redis.StrictRedis(host='localhost', port=6379, db=0)

def redis(response):
    global r
    return r.info()


def mysql(response):
    c = umysql.Connection()  
    c.connect("127.0.0.1", 3306, "root", "mysql", "mysql")
    rs = c.query("SELECT Host FROM user WHERE User = 'root'")
    res = []
    for h in rs.rows:
        res.append(h[0])
    c.close()
    return res


def application(env, start_response):
    if env["PATH_INFO"] == '/':  
        response = {}
        g1 = gevent.spawn(redis, response)
        g2 = gevent.spawn(mysql, response)
        gevent.joinall([g1, g2])
        if g1.value == None or g2.value == None:
            import sys
            sys.exit(1)
            start_response("503 Service Unavailable", [("Content-Type", "application/json")])
            return []
        response["2.mysql"], response["1.redis"] = g2.value, g1.value
        start_response("200 OK", [("Content-Type", "application/json")])
        return [json.dumps(response)]
    else:
        start_response("404 Not Found", [("Content-Type", "application/json")])
        return []


if __name__ == "__main__":
    logging.info('Listening on 8000...')
    WSGIServer(('', 8000), application).serve_forever()

# httperf --server localhost --port 8000 --num-calls 1000 --rate 100 --num-conns 100