from werkzeug.wrappers import Request, Response

@Request.application
def application(request):
    return Response('Simple Test OK!')

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 1972, application)

# uwsgi --log-format '%(addr) - %(user) [%(ltime)] "%(method) %(uri) %(proto)" status) %(size) "%(referer)"%(uagent)' -p 4 --http-socket :1972 --enable-threads --wsgi-file simple.py
