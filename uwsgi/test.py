import gevent
import gevent.socket

def application(e, sr):
    sr('200 OK', [('Content-Type','text/html')])
    yield "Test OK!"

# uwsgi --gevent-monkey-patch --gevent 4 --http-socket :8888 --enable-threads --wsgi-file test.py