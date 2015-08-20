import asyncio, json
from aiohttp import web, request

BIND = '127.0.0.1'
PORT = 8080
ENCODING = 'utf-8'

VERSIONS = ['v1']
CONTROLS = ['index']

CONTENT_TYPE = 'application/json'

def auth(request):
    version = request.match_info.get('version', VERSIONS[0])
    control = request.match_info.get('control', None)

    if not (version in VERSIONS and control in CONTROLS):
        return {'status': web.HTTPBadRequest()}

    return {'status': web.HTTPOk,
            'version': version,
            'control': control,
            'request': request}


@asyncio.coroutine
def fetch_page(url):
    response = yield from request('GET', url)
    assert response.status == 200
    return (yield from response.read())


@asyncio.coroutine
def index(bundle):
    page = 'http://python.org'
    content = yield from fetch_page(page)
    body = { 'get': "GET: %s/%s" % (bundle['version'], bundle['control']),
             'size': len(content),
             'page':  page }
    return web.Response(content_type=CONTENT_TYPE,
                        body=json.dumps(body).encode(ENCODING))


@asyncio.coroutine
def controller(request):
    bundle = auth(request)
    if bundle['status'] != web.HTTPOk:
        return bundle['status']
    return index(bundle)


@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/{version}/{control}', controller)

    srv = yield from loop.create_server(app.make_handler(),
                                        BIND, PORT)

    print("Controller started at http://%s:%s" % (BIND, PORT))
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))

try:
    loop.run_forever()
except KeyboardInterrupt:
    print("Controller interrupted.")