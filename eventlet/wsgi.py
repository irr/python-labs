import eventlet, json, types
from eventlet import wsgi
from urlparse import parse_qs

pool = eventlet.GreenPool()

def info(env):
    if env['REQUEST_METHOD'] in ['POST', 'PUT']:
        request_body = env['wsgi.input'].read(int(env.get('CONTENT_LENGTH', 0)))
        data = parse_qs(request_body)
    else:
        data = env.has_key('QUERY_STRING') and parse_qs(env['QUERY_STRING']) or {}
    vars = dict((k, v) for (k, v) in env.items() if isinstance(v, str))
    return json.dumps({'status': '200 OK', 
                       'headers': [('Content-Type', 'application/json'),
                                   ('Server', 'IRR-WSGI')],
                       'vars': vars,
                       'data': data})

def application(env, start_response):
    pile = eventlet.GreenPile(pool)
    pile.spawn(info, env)
    res = json.loads(''.join(pile))
    start_response(res['status'], res['headers'])
    return [json.dumps({'vars': res['vars'], 'data': res['data']})]
        
# openssl genrsa -des3 -out ca.key 1024
# openssl req -new -key ca.key -out ca.csr
# openssl x509 -days 3650 -signkey ca.key -in ca.csr -req -out ca.crt

# openssl genrsa -out server.key 1024
# openssl req -new -key server.key -out server.csr
# openssl x509 -days 3650 -CA ca.crt -CAkey ca.key -set_serial 01 -in server.csr -req -out server.crt


# http http://localhost:8000/?name=ivan+nossl
# http --verify=no https://localhost:8443/?name=ivan+ssl

# httperf --server localhost --port 8000 --uri / --num-call 100 --num-conn 100
# httperf --ssl --server localhost --port 8443 --uri / --num-call 100 --num-conn 100

def ssl():
  wsgi.server(eventlet.wrap_ssl(eventlet.listen(('', 8443)),
                                certfile='ssl/server.crt',
                                keyfile='ssl/server.key',
                                server_side=True), application)

def nossl():
  wsgi.server(eventlet.listen(('', 8000)), application)

pool.spawn_n(nossl)
pool.spawn_n(ssl)

pool.waitall()