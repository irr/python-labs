from werkzeug.wrappers import Request, Response

@Request.application
def application(request):
    return Response('Simple Test OK!')

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('127.0.0.1', 1972, application)

# uwsgi --log-format '%(addr) - %(user) [%(ltime)] "%(method) %(uri) %(proto)" status) %(size) "%(referer)"%(uagent)' -p 4 --http-socket :1972 --enable-threads --wsgi-file simple.py

# ab -n 10000 -c 100 http://127.0.0.1:1972/

# uwsgi --log-format '%(addr) - %(user) [%(ltime)] "%(method) %(uri) %(proto)" status) %(size) "%(referer)"%(uagent)' -p 4 --http-socket :1972 --enable-threads --http-socket :1972 --plugins python --module=simple

# uwsgi --socket :1972 --enable-threads --plugins python --module=simple
# ab -n 10000 -c 100 http://127.0.0.1:8888/

