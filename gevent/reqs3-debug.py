import gevent
from gevent import monkey
monkey.patch_all()

import random
import requests
import time
from threading import current_thread

def worker(url, use_urllib2=False):
    print(f"{current_thread().name} starting...")
    t = requests.get(url).text.lower()
    n = random.randint(1, 5)
    print(f"{current_thread().name} retrieved {len(t)} bytes")
    print(f"{current_thread().name} sleeping for {n} secs...")
    time.sleep(n)
    return t

urls = ['http://www.github.com']*5

def by_requests():
    jobs = [gevent.spawn(worker, url) for url in urls]
    gevent.joinall(jobs)

def by_urllib2():
    jobs = [gevent.spawn(worker, url, True) for url in urls]
    gevent.joinall(jobs)

if __name__=='__main__':
    from timeit import Timer
    print('starting http requests...')
    t = Timer(stmt="by_requests()", setup="from __main__ import by_requests")  
    print('by requests: %s seconds'%t.timeit(number=3))
    t = Timer(stmt="by_urllib2()", setup="from __main__ import by_urllib2")  
    print('by urllib2: %s seconds'%t.timeit(number=3))

