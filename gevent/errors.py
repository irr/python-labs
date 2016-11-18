import gevent
from gevent import monkey
monkey.patch_all()

import requests, requests.packages

requests.packages.urllib3.disable_warnings()

def worker(url, use_urllib2=False):
    return len(requests.get(url).text.lower())

urls = ['http://www.github.com', 'http://wwwwwwwwwwwwwww/']

def by_requests():
    jobs = [gevent.spawn(worker, url) for url in urls]
    gevent.joinall(jobs)
    for job in jobs:
        print(job.value)


if __name__=='__main__':
    from timeit import Timer
    print 'starting http requests...'
    t = Timer(stmt="by_requests()", setup="from __main__ import by_requests")  
    print 'by requests: %s seconds'%t.timeit(number=1)
