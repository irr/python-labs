import sys
sys.path.append("/usr/lib/python2.7/site-packages")

import web
import redis
_r = redis.Redis(host='localhost', port=6379, db=0)

urls = (
    '/(.*)', 'test',
)

class test:
    def GET(self, name):
        if not name:
            name = '/'

        _r.incr(name)

        web.header('Content-Type', 'text/html; charset=UTF-8')
        return 'OK!'

app = web.application(urls, globals())

if __name__ == '__main__':
    import logging
    from syncless import wsgi
    if len(sys.argv) > 1:
        logging.root.setLevel(logging.DEBUG)
    else:
        logging.root.setLevel(logging.INFO)
    wsgi.RunHttpServer(app, ('localhost', 8080))
