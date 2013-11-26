import bottle
import bottle_mysql

app = bottle.Bottle()
plugin = bottle_mysql.Plugin(dbhost='localhost', dbuser='root', dbpass='mysql', dbname='mysql')
app.install(plugin)

@app.route('/')
def show(db):
    db.execute('SELECT Host, User from user;')
    row = db.fetchone()
    if row:
        return "host=%s and user=%s" % (row["Host"], row["User"])
    bottle.response.status = 404
    return None

app.run(host='localhost', port=8080, debug=True, reloader=True)
