import gevent
from gevent import monkey
from gevent.lock import BoundedSemaphore
monkey.patch_all()

import requests
import time

from functools import wraps

counter = 0


class Nonlocals(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def rate_limited(max_per_second):
    lock = BoundedSemaphore(1)
    min_interval = 1.0 / max_per_second

    def decorate(func):
        nonlocals = Nonlocals(last_time_called=time.clock())

        @wraps(func)
        def rate_limited_function(*args, **kwargs):
            lock.acquire()
            elapsed = time.clock() - nonlocals.last_time_called
            left_to_wait = min_interval - elapsed

            if left_to_wait > 0:
                gevent.sleep(left_to_wait)

            ret = func(*args, **kwargs)
            nonlocals.last_time_called = time.clock()
            lock.release()
            return ret

        return rate_limited_function

    return decorate


@rate_limited(2)
def call_api(url, n):
    global counter
    print(counter, n, url)
    counter += 1
    return requests.get(url).json()


# star another process with: python -m SimpleHTTPServer
jobs = [gevent.spawn(call_api, "http://localhost:8000/test.json", n) for n in range(10)]
gevent.joinall(jobs)

for n, job in enumerate(jobs):
    print(n, job.value)
