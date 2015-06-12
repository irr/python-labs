import gevent
import gevent.socket

import pymysql, redis, json, urlparse, logging

LOG_LEVEL = logging.DEBUG
LOG_FORMAT = '[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s'

logging.basicConfig(format=LOG_FORMAT)
logging.getLogger().setLevel(LOG_LEVEL)

pool = redis.ConnectionPool(host='localhost', port=6379, db=0, max_connections=100)

def redis_exec():
    global pool
    r = redis.Redis(connection_pool=pool)
    return (str(gevent.getcurrent()), r.info())

def mysql_exec():
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='mysql', db='mysql')
    rs = db.cursor()
    rs.execute("SELECT Host FROM user WHERE User = 'root' LIMIT 1")
    res = []
    for h in rs:
        res.append(h[0])
    rs.close()
    db.close()
    return (str(gevent.getcurrent()), res)

def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-Type', 'application/json; charset=utf-8')]

    d = urlparse.parse_qs(environ['QUERY_STRING'])
    t = d.get('t', ['0'])[0]

    g1 = gevent.spawn(redis_exec)
    g2 = gevent.spawn(mysql_exec)

    if t != None and t.isdigit() and t > 0:
        gevent.sleep(int(t))

    gevent.joinall([g1, g2])

    if g1.value == None or g2.value == None:
        start_response("503", headers)
        yield "%s\n" % json.dumps({"error": "Sorry, service unavailable."})[:1024]
    else:
        start_response(status, headers)
        c1, rh = g1.value
        c2, mh = g2.value
        yield "%s\n" % json.dumps({"redis_ctx": c1, "redis": rh["redis_version"], 
                                   "mysql_ctx": c2, "mysql": mh, "t":t})[:1024]

# see: http://uwsgi-docs.readthedocs.org/en/latest/Logging.html
# sudo apt-get install uwsgi-plugin-python
# uwsgi_python --log-format '%(addr) - %(user) [%(ltime)] "%(method) %(uri) %(proto)" %(status) %(size) "%(referer)"%(uagent)' --http-socket :1972 --enable-threads --wsgi-file web.py
# uwsgi_python --thunder-lock --http-socket :1972 --enable-threads --workers 4 --threads 4 --wsgi-file web.py
