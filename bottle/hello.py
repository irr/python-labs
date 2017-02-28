# -*- coding: utf-8 -*-

from bottle import route, run, template

@route('/')
def index():
    t = "одобрение за"
    return 'this is a test ({})!'.format(t)

run(host='localhost', port=8080)
