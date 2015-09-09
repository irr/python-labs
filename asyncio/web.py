# http localhost:8080/https%3A%2F%2Fnews.ycombinator.com

import json
import signal
import sys

import asyncio
from aiohttp import request, web
from bs4 import BeautifulSoup
from textblob import TextBlob


def term_handler(signum, frame):
    if signum:
        print('Signal handler called with signal', signum)
    sys.exit(0)


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
    body = { 'sentences': len(blob.sentences),
             'words': len(blob.words),
             'language': blob.detect_language() }
    return web.Response(body=json.dumps(body).encode('utf-8'),
                        content_type="application/json; charset=utf-8")


@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/{page}', handle)

    srv = yield from loop.create_server(app.make_handler(),
                                        '127.0.0.1', 8080)
    print("Server started at http://127.0.0.1:8080")
    return srv


signal.signal(signal.SIGTERM, term_handler)

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))

try:
    loop.run_forever()
except KeyboardInterrupt:
    term_handler(None, None)
