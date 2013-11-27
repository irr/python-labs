from gevent import monkey
monkey.patch_all()

import gevent, redis, umysql, json, logging, logging.handlers
from gevent.pywsgi import WSGIServer

LOG_LEVEL = logging.DEBUG
LOG_FORMAT = '[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s'
SYSLOG = logging.handlers.SysLogHandler(address='/dev/log')
SYSLOG.setFormatter(logging.Formatter(LOG_FORMAT))

logging.basicConfig(format=LOG_FORMAT)
#logging.getLogger().addHandler(SYSLOG)
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

def application(env, start_response):
    if env["PATH_INFO"] == '/':  
        response = {}
        g1 = gevent.spawn(redis_exec, response)
        g2 = gevent.spawn(mysql_exec, response)
        gevent.joinall([g1, g2])
        response["redis"], response["mysql"] = g1.value["run_id"], g2.value
        if g1.value == None or g2.value == None:
            start_response("503 Service Unavailable", [("Content-Type", "application/json")])
            return []
        start_response("200 OK", [("Content-Type", "application/json")])
        return [json.dumps(response)[:1024]]
    else:
        start_response("404 Not Found", [("Content-Type", "application/json")])
        return []

if __name__ == "__main__":
    logging.info('Listening on 8000...')
    gevent.pywsgi.WSGIServer(('', 8000), application).serve_forever()
