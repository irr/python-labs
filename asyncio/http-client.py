import asyncio
import aiohttp

@asyncio.coroutine
def fetch_page(url):
    response = yield from aiohttp.request('GET', url)
    assert response.status == 200
    return (yield from response.read())

content = asyncio.get_event_loop().run_until_complete(
    fetch_page('http://python.org'))
print(content)
