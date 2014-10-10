from gevent import monkey; monkey.patch_all()
from bottle import route, run, get, post, response, request, abort

import sys, time, argparse, logging, logging.handlers, gevent, redis, umysql, json

LOG_LEVEL = logging.DEBUG
LOG_FORMAT = '[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s'

SYSLOG = logging.handlers.SysLogHandler(address='/dev/log')
SYSLOG.setFormatter(logging.Formatter(LOG_FORMAT))

logging.basicConfig(format=LOG_FORMAT)
logging.getLogger().setLevel(LOG_LEVEL)

pool = redis.ConnectionPool(host='localhost', port=6379, db=0, max_connections=100)

def redis_exec(response):
    global pool
    r = redis.Redis(connection_pool=pool)
    return r.info()

def mysql_exec(response):
    db = umysql.Connection()  
    db.connect("127.0.0.1", 3306, "root", "mysql", "mysql")
    rs = db.query("SELECT Host FROM user WHERE User = 'root' LIMIT 1")
    res = []
    for h in rs.rows:
        res.append(h[0])
    db.close()
    return res

@route('/')
@get('/')
@post('/')
def application():
    response.content_type = 'application/json; charset=utf-8'
    g1 = gevent.spawn(redis_exec, response)
    g2 = gevent.spawn(mysql_exec, response)
    t = 0
    if 't' in request.query:
        t = request.query['t'] 
    else:
        t = request.forms.get('t')
    if t != None and t.isdigit() and t > 0:
        time.sleep(int(t))
    gevent.joinall([g1, g2])
    if g1.value == None or g2.value == None:
        abort(503, "Sorry, service unavailable.")
    return "%s\n" % json.dumps({"redis": g1.value["redis_version"], "mysql":g2.value})[:1024]


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
    run(host=args.bind, port=args.port, server='gevent')
