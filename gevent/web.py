import gevent
from gevent import monkey
from gevent.pywsgi import WSGIServer

import redis, umysql, json, logging, logging.handlers

monkey.patch_all()

G = { "mysql_ptr": None, 
      "mysql_fun": "mysql_init", 
      "redis_ptr": None, 
      "redis_fun": "redis_init" }

def redis_init():
    try:
        globals()["G"]["redis_ptr"] = redis.StrictRedis(host='localhost', port=6379, db=0)
    except Exception as ex:
        res = str(ex)
        logging.error(ex)

def mysql_init():
    try:
        globals()["G"]["mysql_ptr"] = umysql.Connection()  
        globals()["G"]["mysql_ptr"].connect("127.0.0.1", 3306, "root", "mysql", "mysql")
    except Exception as ex:
        res = str(ex)
        logging.error(ex)
        globals()["G"]["mysql_ptr"] = None        


LOG_LEVEL = logging.DEBUG
LOG_FORMAT = '[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s'
SYSLOG = logging.handlers.SysLogHandler(address='/dev/log')
SYSLOG.setFormatter(logging.Formatter(LOG_FORMAT))

logging.basicConfig(format=LOG_FORMAT)
#logging.getLogger().addHandler(SYSLOG)
logging.getLogger().setLevel(LOG_LEVEL)

redis_init()
mysql_init()


def pools(names):
    while True:
        try:        
            for name in names:
                if globals()["G"]["%s_ptr" % name] == None:
                    globals()[globals()["G"]["%s_fun" % name]]()
        except Exception as ex:
            logging.error(str(ex))
        finally:
            gevent.sleep(10)


def task(name, response):
    res = None
    try:
        res = globals()[name](response)
    except Exception as ex:
        logging.error(str(ex))
    finally:
        return res


def redis(response):
    ptr = globals()["G"]["redis_ptr"]
    return ptr.info()


def mysql(response):
    ptr = globals()["G"]["mysql_ptr"]
    if ptr == None:
        return None
    try:
        rs = ptr.query("SELECT Host FROM user WHERE User = 'root'")
        res = []
        for h in rs.rows:
            res.append(h[0])
        return res
    except Exception as ex:
        try:
            ptr.close()
        finally:
            globals()["G"]["mysql_ptr"] = None
            raise ex


def application(env, start_response):
    if env["PATH_INFO"] == '/':  
        response = {}
        g1 = gevent.spawn(task, "redis", response)
        g2 = gevent.spawn(task, "mysql", response)
        gevent.joinall([g1, g2])
        response["redis"], response["mysql"] = g1.value, g2.value
        if g1.value == None or g2.value == None:
            start_response("503 Service Unavailable", [("Content-Type", "application/json")])
            return []
        start_response("200 OK", [("Content-Type", "application/json")])
        return [json.dumps(response)]
    else:
        start_response("404 Not Found", [("Content-Type", "application/json")])
        return []


if __name__ == "__main__":
    logging.info('Listening on 8000...')
    gevent.spawn(pools, ["redis", "mysql"])
    WSGIServer(('', 8000), application).serve_forever()
