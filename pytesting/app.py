import aiohttp
import asyncio
import bjoern
import click
import functools
import json_logging
import logging
import multiprocessing
import os
import signal
import sys
import uuid

from datetime import datetime
from flask import Flask, jsonify, request, g
from types import SimpleNamespace

ASYNC_LOOP = asyncio.new_event_loop()
asyncio.set_event_loop(ASYNC_LOOP)

json_logging.ENABLE_JSON_LOGGING = True
json_logging.init_flask()

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

application = Flask(__name__)

WEBSITES = [
    "https://flaner.com/",
    "https://www.gympass.com/",
    "https://www.uol.com.br/",
]

def ms(st):
    dt = datetime.now() - st
    return round((dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0)


def async_timer(func):
    @functools.wraps(func)
    async def wrapper_timer(*args, **kwargs):
        start_time = datetime.now()
        value = await func(*args, **kwargs)
        return (ms(start_time), value)
    return wrapper_timer


@application.before_request
def before_request():
    g.start_time = datetime.now()
    g.request_id = str(uuid.uuid4())


@application.after_request
def after_request(response):
    response.headers['X-Profile'] = str(ms(g.start_time))
    response.headers['X-Req'] = g.request_id
    return response


@async_timer
async def _fetch(session, url):
    async with session.get(url) as response:
        status = response.status
        content = await response.text()
        return SimpleNamespace(**{"status": status, "content": content})


@async_timer
async def fetch(url):
    async with aiohttp.ClientSession() as session:
        content, status, error = None, -1, None
        try:
            (ms, response) = await _fetch(session, url)
            status, content = response.status, response.content
        except Exception as ex:
            error = ex
        return {"url": url, "content": content, "status": status, "error": error}


@async_timer
async def batch_fetch(urls):
    return await asyncio.gather(*[fetch(u) for u in urls])


@application.route('/', methods=['GET'])
def index():
    reqs = ASYNC_LOOP.run_until_complete(
        batch_fetch(WEBSITES)
    )

    mapping = {}
    for res in reqs[1]:
        mapping[res[1]["url"]] = {"ms": res[0], "status": res[1]["status"], "size": len(res[1]["content"]) if res[1]["content"] is not None else None}

    logger.info(f"[pid={os.getpid()}] index called [{request.url}]", extra={"props": {"mapping": mapping, "ms": reqs[0]}})
    return jsonify(mapping)


@click.command()
@click.option('--workers', default=1, help='Number of processes.')
def main(workers):
    worker_pids = []
    if workers <= 0:
        workers = multiprocessing.cpu_count()
    if workers == 1:
        print(f"Server started with pid={os.getpid()}")
        bjoern.run(application, 'localhost', 8080)
    else:
        print(f"Starting {workers} worker(s)...")
        bjoern.listen(application, 'localhost', 8080)
        print(f"Master started with pid={os.getpid()}")
        for _ in range(workers):
            pid = os.fork()
            if pid > 0:
                worker_pids.append(pid)
            elif pid == 0:
                try:
                    print(f"Worker started with pid={os.getpid()}")
                    bjoern.run()
                except KeyboardInterrupt:
                    pass
                exit()
        try:
            for _ in range(workers):
                os.wait()
        except KeyboardInterrupt:
            for pid in worker_pids:
                os.kill(pid, signal.SIGINT)


if __name__ == "__main__":
    main()
