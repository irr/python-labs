from gevent import monkey; monkey.patch_all()

from time import sleep
from bottle import route, run

@route('/stream/:secs')
def stream(secs):
    n = int(secs)
    yield 'START\n'
    sleep(n)
    yield 'MIDDLE\n'
    sleep(n)
    yield 'END\n'

run(host='0.0.0.0', port=8080, server='gevent', reload=True, debug=True)