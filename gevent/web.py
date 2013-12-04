from gevent import monkey; monkey.patch_all()
from bottle import route, run, response, abort

import sys, argparse, logging, logging.handlers, gevent, redis, umysql, json

LOG_LEVEL = logging.DEBUG
LOG_FORMAT = '[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s'

SYSLOG = logging.handlers.SysLogHandler(address='/dev/log')
SYSLOG.setFormatter(logging.Formatter(LOG_FORMAT))

logging.basicConfig(format=LOG_FORMAT)
logging.getLogger().setLevel(LOG_LEVEL)

def redis_exec(response):
    r = redis.Redis(host='localhost', port=6379, db=0)
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
def application():
    response.content_type = 'application/json; charset=utf-8'
    g1 = gevent.spawn(redis_exec, response)
    g2 = gevent.spawn(mysql_exec, response)
    gevent.joinall([g1, g2])
    if g1.value == None or g2.value == None:
        abort(503, "Sorry, service unavailable.")
    return "%s\n" % json.dumps({"redis": g1.value["run_id"], "mysql":g2.value})[:1024]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--syslog', 
                        dest="syslog", 
                        action='store_true', 
                        help="enable syslog")
    parser.add_argument('-p', '--port', 
                        dest="port", 
                        type=int,
                        default=8000,
                        help="listen port")
    args = parser.parse_args()
    if args.syslog:
        logging.getLogger().addHandler(SYSLOG)
    logging.info('Listening on %d...' % args.port)
    run(host='localhost', port=args.port, server='gevent')
