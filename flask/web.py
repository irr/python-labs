"""
Basic template for gevent+flask web server
Author: Ivan Ribeiro Rocha (ivan.ribeiro@gmail.com)
"""

import gevent
from gevent import monkey

monkey.patch_all()
from gevent.pywsgi import WSGIServer

from flask import Flask, Response, request, abort, jsonify
from functools import wraps

import argparse, json, pymysql, redis
import logging.handlers

import requests
import requests.packages

requests.packages.urllib3.disable_warnings()

LOG_LEVEL = logging.DEBUG
LOG_FORMAT = '[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s'

SYSLOG = logging.handlers.SysLogHandler(address='/dev/log')
SYSLOG.setFormatter(logging.Formatter(LOG_FORMAT))

logging.basicConfig(format=LOG_FORMAT)
logging.getLogger().setLevel(LOG_LEVEL)

app = Flask(__name__)

def returns_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        r = f(*args, **kwargs)
        return Response(json.dumps(r).encode('utf-8'), content_type='application/json; charset=utf-8')
    return decorated_function

@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error=404, text=str(e)), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error=500, text=str(e)), 500

@app.errorhandler(503)
def internal_server_error(e):
    return jsonify(error=503, text=str(e)), 503


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

@app.route('/myroute', methods=['POST', 'GET'])
@app.route('/myroute/<name>', methods=['GET'])
@returns_json
def myroute(name=None):
    gev1 = gevent.spawn(redis_exec)
    gev2 = gevent.spawn(mysql_exec)

    gevent.joinall([gev1, gev2])

    if gev1.value == None or gev2.value == None:
        abort(503)
    else:
        return {"redis": gev1.value["redis_version"],
                "mysql":gev2.value,
                "name":name}


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
    ARGS = PARSER.parse_args()

    if ARGS.syslog:
        logging.getLogger().addHandler(SYSLOG)

    logging.info('ACICTL started on %s:%d...' % (ARGS.bind, ARGS.port))
    app.debug = True
    WSGIServer((ARGS.bind, ARGS.port), app).serve_forever()
