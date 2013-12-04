import gevent
from gevent import monkey

monkey.patch_all()

import requests
import urllib2

def worker(url, use_urllib2=False):
    if use_urllib2:
        return urllib2.urlopen(url).read().lower()
    else:
        return requests.get(url).text.lower()

urls = ['http://www.github.com']*5

def by_requests():
    jobs = [gevent.spawn(worker, url) for url in urls]
    gevent.joinall(jobs)

def by_urllib2():
    jobs = [gevent.spawn(worker, url, True) for url in urls]
    gevent.joinall(jobs)

if __name__=='__main__':
    from timeit import Timer
    t = Timer(stmt="by_requests()", setup="from __main__ import by_requests")  
    print 'by requests: %s seconds'%t.timeit(number=3)
    t = Timer(stmt="by_urllib2()", setup="from __main__ import by_urllib2")  
    print 'by urllib2: %s seconds'%t.timeit(number=3)
