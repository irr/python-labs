import gevent
from gevent import monkey
from gevent.pywsgi import WSGIServer

import redis, umysql, json, logging, logging.handlers

monkey.patch_all()

LOG_LEVEL = logging.DEBUG
LOG_FORMAT = '[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s'
SYSLOG = logging.handlers.SysLogHandler(address='/dev/log')
SYSLOG.setFormatter(logging.Formatter(LOG_FORMAT))

logging.basicConfig(format=LOG_FORMAT)
#logging.getLogger().addHandler(SYSLOG)
logging.getLogger().setLevel(LOG_LEVEL)

global r

r = redis.StrictRedis(host="127.0.0.1", port=6379, db=0)

def redis(response):
    global r
    response["redis"] = r.info()

def mysql(response):
    c = umysql.Connection()  
    c.connect("127.0.0.1", 3306, "root", "mysql", "mysql")
    rs = c.query("SELECT Host FROM user WHERE User = 'root'")
    response["mysql"] = []
    for h in rs.rows:
        response["mysql"].append(h[0])
    c.close()

def application(env, start_response):
    if env["PATH_INFO"] == '/':  
        response = {}
        g1 = gevent.spawn(redis, response)
        g2 = gevent.spawn(mysql, response)
        gevent.joinall([g1, g2])
        start_response("200 OK", [("Content-Type", "application/json")])
        return [json.dumps(response)]
    else:
        start_response("404 Not Found", [("Content-Type", "application/json")])
        return ["Not Found"]


if __name__ == "__main__":
    logging.info('Listening on 8000...')
    WSGIServer(('', 8000), application).serve_forever()
