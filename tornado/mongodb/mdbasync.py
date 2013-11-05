import tornado.ioloop
import asyncmongo
from bson.json_util import dumps, loads

def query(response, error):
	tornado.ioloop.IOLoop.instance().stop()
	print(dumps(response))

db = asyncmongo.Client(pool_id='query', host='127.0.0.1', port=27017, dbname='example', mincached=3)

db.widgets.find({"name": "flibnip"}, callback=query)
tornado.ioloop.IOLoop.instance().start()
