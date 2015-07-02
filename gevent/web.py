from gevent.pywsgi import WSGIServer
from cgi import parse_qs, escape

import argparse, gevent, pymysql, redis, json, logging, logging.handlers

LOG_LEVEL = logging.DEBUG
LOG_FORMAT = '[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s'

SYSLOG = logging.handlers.SysLogHandler(address='/dev/log')
SYSLOG.setFormatter(logging.Formatter(LOG_FORMAT))

logging.basicConfig(format=LOG_FORMAT)
logging.getLogger().setLevel(LOG_LEVEL)

pool = redis.ConnectionPool(host='localhost', port=6379, db=0, max_connections=100)

def redis_exec():
    global pool
    r = redis.Redis(connection_pool=pool)
    return r.info()

def mysql_exec():
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='mysql', db='mysql')
    rs = db.cursor()
    rs.execute("SELECT Host FROM user WHERE User = 'root' LIMIT 1")
    res = []
    for h in rs:
        res.append(h[0])
    rs.close()
    db.close()
    return res

def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-Type', 'application/json; charset=utf-8')]

    d = parse_qs(environ['QUERY_STRING'])
    t = int(escape(d.get('t', ['0'])[0]))

    if t > 0:
        gevent.sleep(int(t))

    g1 = gevent.spawn(redis_exec)
    g2 = gevent.spawn(mysql_exec)

    gevent.joinall([g1, g2])

    if g1.value == None or g2.value == None:
        start_response("503", headers)
        yield ("%s\n" % json.dumps({"error": "Sorry, service unavailable."})[:1024]).encode('utf-8')
    else:
        start_response(status, headers)
        yield ("%s\n" % json.dumps({"redis": g1.value["redis_version"], "mysql":g2.value, "t":t})[:1024]).encode('utf-8')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--syslog', 
                        dest="syslog", 
                        action='store_true', 
                        help="enable syslog (default: disabled)")
    parser.add_argument('-b', '--bind', 
                        dest="bind", 
                        default="0.0.0.0",
                        help="bind address (default: 0.0.0.0)")
    parser.add_argument('-p', '--port', 
                        dest="port", 
                        type=int,
                        default=8000,
                        help="listen port (default: 8000)")
    args = parser.parse_args()
    if args.syslog:
        logging.getLogger().addHandler(SYSLOG)
    logging.info('Listening on %s:%d...' % (args.bind, args.port))
    WSGIServer((args.bind, args.port), application).serve_forever()
