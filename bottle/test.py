from bottle import route, run, hook, response

@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'

@route('/hello')
def hello():
    return "Hello World!"

run(host='localhost', port=8080, debug=True, reloader=True)
