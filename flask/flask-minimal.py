import gevent
import logging

from logging.handlers import RotatingFileHandler

from flask import Flask

from gevent.wsgi import WSGIServer
from gevent import monkey

monkey.patch_all()

app = Flask(__name__)

@app.route("/")
def hello():
    try:
        g = gevent.spawn(lambda x: x, "Hello World!")
        gevent.joinall([g])
        return g.value
    except Exception as ex:
        return str(ex)

if __name__ == "__main__":
    handler = RotatingFileHandler('flask.minimal.log', maxBytes=100000, backupCount=1)
    handler.setLevel(logging.INFO)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.INFO)
    log.addHandler(handler)
    app.run(port=5000, debug=False)
