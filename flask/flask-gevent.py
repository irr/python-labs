from flask import Flask
from gevent.wsgi import WSGIServer
from gevent import monkey

monkey.patch_all()

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()