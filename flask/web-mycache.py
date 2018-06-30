import redis
import simplejson as json
import sys

from datetime import datetime

# pip install flask redis simplejson
from flask import Flask, jsonify, g, request, current_app

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_TIMEOUT = 2000
REDIS_TTL = 300

app = Flask(__name__)

client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0, socket_timeout=REDIS_TIMEOUT)


@app.before_request
def before_request():
    g.ruser = request.args.get("user", "anonymous")
    g.rkey = f"{g.ruser}:cache"


@app.route('/clear')
def clear():
    client.delete("flask_cache_/now")
    return "OK"


@app.route('/now')
def current_time():
    pipe, now = None, None
    try:
        now = client.hget(g.rkey, request.path)
    except:
        print("Unexpected error(1):", sys.exc_info()[0])
    try:
        if now is not None:
            return now
        now = str(datetime.now())
        pipe = client.pipeline()
        pipe.hset(g.rkey, request.path, now)
        pipe.expire(g.rkey, REDIS_TTL)
        pipe.execute()
    except:
        if pipe is not None:
            pipe.reset()
        print("Unexpected error(2):", sys.exc_info()[0])
    finally:
        return now


if __name__ == '__main__':
    app.run()