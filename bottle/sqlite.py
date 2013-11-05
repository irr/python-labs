import bottle
from bottle.ext import sqlite

# pip install -v bottle bottle-sqlite bottle-redis bottle-memcache bottle-mongodb
# CREATE TABLE items(id INTEGER PRIMARY KEY ASC, name);
# httperf --server=localhost --port=8080 --uri=/show/irr --num-calls=1 --num-conns=1000

app = bottle.Bottle()
plugin = sqlite.Plugin(dbfile='/tmp/test.db')
app.install(plugin)

@app.route('/show/:item')
def show(item, db):
    row = db.execute('SELECT * from items where name=?', (item,)).fetchone()
    if row:
        return "id=%s and name=%s" % (row[0], row[1])
    bottle.response.status = 404
    return None

app.run(host='localhost', port=8080, debug=True, reloader=True)
