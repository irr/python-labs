# http localhost:8080/https%3A%2F%2Fnews.ycombinator.com

import asyncio
import functools
import json
import os
import signal

from aiohttp import request, web
from bs4 import BeautifulSoup
from textblob import TextBlob

HOST = '127.0.0.1'
PORT = 8080

def term_handler(signame):
    print("got signal %s: exit" % signame)
    loop.stop()


def strip(content):
    soup = BeautifulSoup(content, "html.parser")
    [s.extract() for s in soup(['style', 'script'])]
    text = soup.getText()
    return str.encode(text, encoding='utf-8')


@asyncio.coroutine
def fetch_page(url):
    response = yield from request('GET', url)
    assert response.status == 200
    return (yield from response.read())


@asyncio.coroutine
def handle(request):
    page = request.match_info.get('page')
    content = yield from fetch_page(page)
    text = strip(content)
    blob = TextBlob(text.decode('utf-8'))
    words = list({ w for w in blob.words if len(w) > 4})
    words.sort()
    body = { 'sentences': len(blob.sentences),
             'words': len(words),
             'language': blob.detect_language(),
             'blob': words }
    return web.Response(body=json.dumps(body).encode('utf-8'),
                        content_type="application/json; charset=utf-8")


@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/{page}', handle)

    srv = yield from loop.create_server(app.make_handler(),
                                        HOST, PORT)
    print("Server started at http://%s:%d" % (HOST, PORT))


loop = asyncio.get_event_loop()
for signame in ('SIGINT', 'SIGTERM'):
    loop.add_signal_handler(getattr(signal, signame),
                            functools.partial(term_handler, signame))

loop.run_until_complete(init(loop))

print("pid %s: send SIGINT or SIGTERM to exit." % os.getpid())
loop.run_forever()
