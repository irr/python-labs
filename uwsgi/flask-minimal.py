import logging
import requests
import threading
import uuid

from datetime import datetime
from flask import Flask, jsonify, g

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = Flask(__name__)

URL = "https://www.uol.com.br"

LOCK = threading.Lock()

@app.before_request
def before_request():
    g.start_time = datetime.now()
    g.request_id = str(uuid.uuid4())


@app.after_request
def after_request(response):
    dt = datetime.now() - g.start_time
    ms = str(round((dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0))
    response.headers['X-Profile'] = ms
    response.headers['X-Req'] = g.request_id
    return response


@app.route("/")
def hello():
    with LOCK:
        r = requests.get(URL)
        return jsonify({"status": r.status_code, "content": r.text[:80]})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)


# ab -n 100 -c 100 http://localhost:5000/

# uwsgi (master)]$ uwsgi --http :5000 --wsgi-file flask-minimal.py --callable app --processes 1
