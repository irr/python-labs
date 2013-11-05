# http://scrollingtext.org/first-flask-web-app
from __future__ import with_statement
from gevent.wsgi import WSGIServer
from urllib2 import urlopen
from contextlib import closing
from flask import Flask, request, g, jsonify
#from lru_cache import lru_cache
import sqlite3
import sha

DATABASE = '/tmp/challenge.db'
DEBUG = True
SECRET_KEY = 'c29tZXRoaW5nY2xldmVyaGVyZQ==\n'
USERNAME = 'challenge'
PASSWORD = 'chang3m3'

app = Flask(__name__)
app.config.from_object(__name__)
 
app.config.from_envvar('CHALLENGE_SETTINGS', silent=True)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('flask-sqlite-schema.sql') as f:
            db.cursor().executescript(f.read())
            db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/fib/<number>')
def fib(number):
    try:
        return jsonify({'response' : real_fib(int(number))})
    except ValueError:
        return jsonify({'response' : 'ERROR: Input not a number'})
 
#@lru_cache()
def real_fib(n):
    """
    This code was modified from the fib code in the python3 functools
    documentation.
    """
    if n < 2:
        return n
    return real_fib(n-1) + real_fib(n-2)
 
@app.route('/google-body')
def google_body():
    try:
        sh = sha.new(urlopen('http://www.google.com').read())
        return jsonify({'response' : sh.hexdigest()})
    except Exception as e:
        return jsonify({'response' : 'ERROR: %s' % str(e)})

@app.route('/store', methods=['GET', 'POST'])
def store():
    if request.method == 'POST':
        try:
            g.db.execute('insert into entries (value) values (?)',
                [request.form['value']])
            g.db.commit()
            resp = jsonify()
            resp.status_code = 200
            return resp
        except Exception as e:
            return jsonify({"response" : "ERROR: %s" % str(e)})
    else:
        try:
            cur = g.db.execute('select value from entries order by id desc')
            #fetchone returns a list. To better meet the requirements,
            #just slicing the head of the list and output that.
            return jsonify({'response' : cur.fetchone()[0]})
        except IndexError:
            return jsonify({'response' : 'NOTHING IN THE DATABASE'})
 
if __name__ == "__main__":
    init_db()
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()

# http http://localhost:5000/google-body
# http --form POST http://localhost:5000/store value=ivan
# http --form POST http://localhost:5000/store value=alessandra
# http http://localhost:5000/store