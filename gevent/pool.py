import random

from gevent import sleep
from gevent.pool import Pool

MAX = 5
RES = [0] * 5

def worker(n):
    global RES
    try:
        print('Worker %i started' % n)
        r = random.random()
        sleep(r)
        print('Worker %i finished' % n)
        RES[n] = r
    except:
        RES[n] = None

pool = Pool()
pool.map(worker, range(0, MAX))

pool.join()

print(RES)
print(sum(RES))
