import random
import redis

from datetime import datetime

# pip install flask flask-caching redis
from flask import Flask, jsonify, request, current_app
from flask_caching import Cache

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_TIMEOUT = 2000

app = Flask(__name__)

cache = Cache(config={"CACHE_TYPE": "redis", "CACHE_REDIS_URL": f"redis://{REDIS_HOST}:{REDIS_PORT}"})
cache.init_app(app)

client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0, socket_timeout=REDIS_TIMEOUT)

def cache_key():
    print(">>> request:", request.args, request.path)
    return f"{request.path}"


@app.route('/clear')
def clear():
    client.delete("flask_cache_/now")
    return "OK"


@app.route('/now')
@cache.cached(timeout=60, key_prefix=cache_key)
def current_time():
    return str(datetime.now())


if __name__ == '__main__':
    app.run()